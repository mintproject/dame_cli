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
from core.emulatorapi import list_threads, get_thread
from core.utils import obtain_id, download_file, download_setup
from core.modelcatalogapi import get_setup, list_setup, get_model
from core.executor import execute_setup
from mint import _utils, _makeyaml
from mint._utils import log
import texttable as tt
from tabulate import tabulate
import pandas as pd
import urllib3
http = urllib3.PoolManager()
chunk_size = 65536

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


@cli.group()
def inputs():
    """Manages the inputs of the executions"""


@inputs.command(name='list',
                help="List the inputs")
@click.argument(
    "thread_id",
    required=True,
    type=str
)
def _list(thread_id):
    thread = get_thread(thread_id)
    for model in thread.models:
        print(tabulate(parse_inputs(model, thread), tablefmt="pipe", headers="keys"))


def download_files(files):
    size = 0
    for file in files:
        size += int(check_size(file['download_url']))
    click.secho("Files size: {}".format(size), fg="green")
    if not click.confirm('Do you want to continue?'):
        return
    for file in files:
        file_name = download_file(file['download_url'])
        click.secho("Ready: {}".format(file_name), fg="green")


def check_size(url):
    r = http.request('GET', url, preload_content=False)
    content_bytes = r.headers.get("Content-Length")
    r.release_conn()
    return content_bytes


def download_file(url):
    file_name = url.split('/')[-1]
    r = http.request('GET', url, preload_content=False)
    with open(file_name, 'wb') as out:
        while True:
            data = r.read(chunk_size)
            if not data:
                break
            out.write(data)
    r.release_conn()
    out.close()
    return file_name

def parse_inputs(model, thread):
    inputs = []
    for input in thread.models[model]['input_files']:
        id = check_is_none(input, 'id')
        name = check_is_none(input, 'name')
        available_resources = check_is_none(check_is_none(input, 'value'), 'resources')
        for r in available_resources:
            if check_is_none(r, "selected"):
                download_url = check_is_none(r, 'url')
        inputs.append({'id': id, 'name': name, 'download_url': download_url})
    return inputs

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
def download(thread_id):
    thread = get_thread(thread_id)
    for model in thread.models:
        inputs = parse_inputs(model, thread)
        download_files(inputs)

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


def check_is_none(item, key):
    return item[key] if key in item else ''


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
