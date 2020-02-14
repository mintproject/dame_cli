# -*- coding: utf-8 -*-
"""
mint.

:license: Apache 2.0
"""
import json
import os
import re
from pathlib import Path

import click

import semver
import mint
from mint.cli_methods import run_method, edit_inputs_model_configuration, edit_parameter_config_or_setup, \
    edit_inputs_setup, run_method_setup
from mint.downloader import check_size, parse_inputs, parse_outputs
from mint.emulatorapi import get_summary, list_summaries, obtain_results
from mint.utils import obtain_id, download_file, download_data_file, humansize, SERVER, check_is_none
from mint.modelcatalogapi import get_setup, list_setup, get_model, list_model_configuration, get_model_configuration
from mint import _utils, _makeyaml
from mint._utils import log
import texttable as tt
from modelcatalog import DatasetSpecification, SampleResource

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = ".".join(_utils.get_latest_version().split(".")[:3])
    cv = ".".join(mint.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using mint version {mint.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade mint' command.""",
            fg="yellow",
        )

"""
Click group: Model Configuration
"""


@cli.group()
def modelconfiguration():
    """Manages model"""


@modelconfiguration.command(name="run",
                            help="Manages model configurations")
@click.argument(
    "name",
    type=click.STRING
)
@click.option(
    "--auto",
    help="Use the default value",
    is_flag=True
)
def run(name, auto):
    setup = get_model_configuration(name)
    edit_inputs_setup(setup)
    run_method_setup(setup)

@modelconfiguration.command(name="list", help="List configurations")
def _list():
    tab = tt.Texttable()
    headings = ['name', 'description']
    tab.header(headings)
    for setup_item in list_model_configuration(label=None):
        name = obtain_id(setup_item.id)
        tab.add_row([name, setup_item.label[0]])
    print(tab.draw())

"""
Click group: Setup
"""


@cli.group()
def setup():
    """Manages setups"""


@setup.command(help="Run a setup_name by name.")
@click.argument(
    "name",
    type=click.STRING
)
@click.option(
    '--edit',
    is_flag=True
)

def run(edit, name):
    setup = get_setup(name)
    edit_inputs_setup(setup)
    run_method_setup(setup)


@setup.command(name="list", help="List configurations")
def _list():
    tab = tt.Texttable()
    headings = ['name', 'description']
    tab.header(headings)
    for setup_item in list_setup(label=None):
        name = obtain_id(setup_item.id)
        tab.add_row([name, setup_item.label[0]])
    print(tab.draw())


"""
Click group: Execution
"""


@cli.group()
def execution():
    """Manages the executions"""


@execution.command(name='download',
                   help="Download the inputs")
@click.argument(
    "thread_id",
    required=True,
    type=str
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, exists=False),
    default='.'
)
def download(thread_id, output):
    summary = get_summary(thread_id)
    results = obtain_results(thread_id)
    model_directory = Path(output)
    for model in summary.thread.models:
        inputs = parse_inputs(model, summary.thread)
        outputs = parse_outputs(model, summary.thread, results)
        model_name = model.split('/')[-1]
        thread_directory = model_directory / model_name / thread_id
        download_files(inputs, outputs, thread_directory)
        with open(thread_directory / "summary.json", 'w', encoding='utf-8') as f:
            json.dump(summary.to_dict(), f, ensure_ascii=False, indent=4)


@execution.command(
    name="search",
    help="Search with regular expression match by name or description.",
)
@click.argument(
    "free_text",
    default="",
    type=str
)
@click.option(
    "--limit",
    "-l",
    default=200,
    help="Maximum number of executions to display. "
         "If limit is bigger than ‘api.max_limit’ option of Ingestion API, "
         "limit 'api.max_limit' will be used instead.",
    type=int,
)
def _list(limit, free_text=""):
    tab = tt.Texttable()
    # headings = ['scenario_id', 'problem_id', 'thread_id', 'model']
    headings = ['thread_id', 'model']
    summaries = list_summaries(limit=limit, page=1, model=free_text)
    for s in summaries:
        tab.add_row([s.thread.id, s.thread.models])
        # tab.add_row([s.scenario.id, s.problem_formulation.id, s.thread.id, s.thread.models])
    tab.header(headings)
    print(tab.draw())
    print("{} results".format(len(summaries)))


@execution.command(help="Show details of execution")
@click.argument(
    "thread_id",
    required=True,
    type=str
)
def show(thread_id):
    summary = get_summary(thread_id)
    region = summary.scenario.region.lower()
    scenario_id = summary.scenario.id
    problem_id = summary.problem_formulation.id
    link = "{}/{}/modeling/scenario/{}/{}/{}".format(SERVER, region, scenario_id, problem_id, thread_id)
    click.secho("Please visit {}".format(link))


def download_files(inputs, outputs, thread_directory):
    model_directory_inputs = thread_directory / 'inputs'
    model_directory_outputs = thread_directory / 'outputs'
    Path.mkdir(model_directory_inputs, parents=True, exist_ok=True)
    Path.mkdir(model_directory_outputs, parents=True, exist_ok=True)

    files = inputs + outputs
    size = 0
    for file in files:
        size += int(check_size(file['download_url']))
    click.secho("You are going to download {}".format(humansize(size)), fg="green")
    if not click.confirm('Do you want to continue?'):
        return

    click.secho("The destination directory is: {}".format(thread_directory.absolute()), fg="yellow")
    for file in outputs:
        data_specification_id = file['id']
        _, filename = download_data_file(file['download_url'], model_directory_outputs, data_specification_id)
        click.secho("Downloaded: {}".format(filename), fg="green")

    for file in inputs:
        _, filename = download_data_file(file['download_url'], model_directory_inputs)
        click.secho("Downloaded: {}".format(filename), fg="green")
