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

import click

import semver

from mint import _utils, _makeyaml

@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = ".".join(_utils.get_latest_version().split(".")[:3])
    cv = ".".join(wcm.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using wcm version {wcm.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade wcm' command.""",
            fg="yellow",
        )

@cli.command(help="Generates a blank YAML from the schema. Useful for creating a new component from scratch. Optional "
                  "parameter --file-path <path> to choose which directory the blank YAML should be created in")
@click.option(
    "--file-path",
    "-f",
    type=str,
    default=None,
)
def make_yaml(file_path=None):
    logging.info("Generating blank YAML")
    _makeyaml.make_yaml(download_path=file_path)
    click.secho(f"Done", fg="green")
