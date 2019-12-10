# -*- coding: utf-8 -*-
"""
mint.

:license: Apache 2.0
"""

import configparser
import logging
import os
import sys
from pathlib import Path
import yaml
import click

import semver
import mint
from core.executor import read_setup
from mint import _utils, _makeyaml
from mint._utils import log


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

@cli.command(help="Run a setup_name.")
@click.option("--debug/--no-debug", "-d/-nd", default=False)
@click.option("--dry-run", "-n", is_flag=True)
@click.option("--ignore-data/--no-ignore-data", "-i/-ni", default=False)
@click.option("--overwrite", "-f", is_flag=True, help="Replace existing components")
@click.argument(
    "setup",
    type=click.Path(file_okay=True, dir_okay=True, writable=True, exists=True),
)
def run(setup, debug=False, dry_run=False, ignore_data=False, overwrite=False):
    setup_files = []
    if os.path.isdir(setup):
        path = Path(setup)
        for file in os.listdir(path):
            if file.endswith(".yaml") or file.endswith(".yml"):
                setup_files.append(path/file)
    elif os.path.isfile(setup):
        path = Path('.')
        setup_files.append(path/setup)
    try:
        status = read_setup(setup_files)
    except Exception as e:
        log.error(e)
        exit(1)
    for setup in status:
        if setup["exitcode"] == 0:
            click.secho("{} ok".format(setup["name"]), fg="green")
        else:
            click.secho("{} failed".format(setup["name"]), fg="red")
