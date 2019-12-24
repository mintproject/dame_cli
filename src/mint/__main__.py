# -*- coding: utf-8 -*-
"""
mint.

:license: Apache 2.0
"""

import os
from pathlib import Path
import click

import semver
import mint
from core.utils import obtain_id, download_file, download_setup
from core.api import get_setup, list_setup
from core.executor import execute_setup
from mint import _utils, _makeyaml
from mint._utils import log
import texttable as tt

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
def list():
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
