# -*- coding: utf-8 -*-
"""
mint.

:license: Apache 2.0
"""

import os
from pathlib import Path
from pprint import pprint

import click

import semver
import mint
from core.downloader import check_size, parse_inputs
from core.emulatorapi import list_threads, get_thread
from core.utils import obtain_id, download_file, download_setup, download_data_file, humansize
from core.modelcatalogapi import get_setup, list_setup, get_model
from core.executor import execute_setup
from mint import _utils, _makeyaml
from mint._utils import log
import texttable as tt
from tabulate import tabulate
import pandas as pd


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


def download_files(files, name, thread_id, output_directory):
    output = Path(output_directory)
    model_directory = output / name / thread_id
    Path.mkdir(model_directory, parents=True, exist_ok=True)

    size = 0
    for file in files:
        size += int(check_size(file['download_url']))
    click.secho("You are going to download {}".format(humansize(size)), fg="green")
    if not click.confirm('Do you want to continue?'):
        return

    click.secho("The destination directory is: {}".format(model_directory.absolute()), fg="yellow")
    for file in files:
        _, filename = download_data_file(file['download_url'], model_directory)
        click.secho("Downloaded: {}".format(filename), fg="green")

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
    thread = get_thread(thread_id)
    for model in thread.models:
        inputs = parse_inputs(model, thread)
        download_files(inputs, model.split('/')[-1], thread_id, output)


@execution.command(
    name="search",
    help="List all the execution"
)
@click.option(
    "--model",
    default="",
    help="Search with regular expression match by name or description.",
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
def _list(limit, model=""):
    tab = tt.Texttable()
    headings = ['name', 'models']
    threads = list_threads(limit=limit, page=1, model=model)
    for t in threads:
        tab.add_row([t.id, t.models])
    tab.header(headings)
    print(tab.draw())
    print("{} results".format(len(threads)))


@execution.command(help="Show details of execution")
def detail(thread_id):
    pass


@cli.group()
def setup():
    """Manages a setup of a model."""


@setup.command(help="Create setup file.")
@click.argument(
    "setup_id",
    type=str,
)
@click.option(
    "--output",
    "-o",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, exists=False),
    default='.'
)
def download(setup_id, output):
    path = download_setup(setup_id, output)
    click.secho("{} has been exported. Check {}".format(setup_id, path), fg="green")


@setup.command(help="List configurations")
def lista():
    tab = tt.Texttable()
    headings = ['name', 'description']
    tab.header(headings)
    for setup_item in list_setup(label=None):
        name = obtain_id(setup_item.id)
        tab.add_row([name, setup_item.label[0]])
    print(tab.draw())


@setup.command(help="Run a setup_name by name.")
@click.argument(
    "name",
    type=click.STRING
)
def run(name=None):
    file_path = download_setup(setup_id=name, output=Path('.'))
    status = execute_setups(file_path)
    for setup in status:
        if setup["exitcode"] == 0:
            click.secho("{} ok".format(setup["name"]), fg="green")
        else:
            click.secho("{} failed".format(setup["name"]), fg="red")


def execute_setups(path):
    setup_files = []
    if os.path.isdir(path):
        path = Path(path)
        for file in os.listdir(path):
            if file.endswith(".yaml") or file.endswith(".yml"):
                setup_files.append(path / file)
    elif os.path.isfile(path):
        default_path = Path('.')
        setup_files.append(default_path / path)
    try:
        status = execute_setup(setup_files)
    except Exception as e:
        log.error(e, exc_info=True)
        exit(1)
    return status
