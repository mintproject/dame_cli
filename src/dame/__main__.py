# -*- coding: utf-8 -*-
"""
dame.

:license: Apache 2.0
"""
import json
import logging
import os
import re
from pathlib import Path

import click

import semver
import dame
from dame.cli_methods import run_method, edit_inputs_model_configuration, edit_parameter_config_or_setup, \
    verify_input_parameters, run_method_setup
from dame.downloader import check_size, parse_inputs, parse_outputs
from dame.emulatorapi import get_summary, list_summaries, obtain_results
from dame.utils import obtain_id, download_file, download_data_file, humansize, SERVER, check_is_none
from dame.modelcatalogapi import get_setup, list_setup, get_model, list_model_configuration, get_model_configuration
from dame import _utils, _makeyaml
from dame._utils import log
import texttable as tt
from modelcatalog import DatasetSpecification, SampleResource, ApiValueError, OpenApiException

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = ".".join(_utils.get_latest_version().split(".")[:3])
    cv = ".".join(dame.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using dame version {dame.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade dame' command.""",
            fg="yellow",
        )


@cli.command(help="Open the Model Catalog in your browser")
def browse():
    click.launch('https://models.mint.isi.edu')

"""
Run a modelconfiguration or modelconfiguration
"""
@cli.command(help="Run a model configuration or model configuration setup")
@click.argument(
    "name",
    type=click.STRING
)
def run(name):
    try:
        config = get_model_configuration(name)
    except OpenApiException as e:
        logging.error(e.reason)
        exit(0)

    if "ModelConfigurationSetup" in config.type:
        resource = get_setup(name)
        verify_input_parameters(resource)
    elif "ModelConfiguration" in config.type:
        resource = get_model_configuration(name)
        verify_input_parameters(resource)
    # setup = get_setup(name)
    # edit_inputs_setup(setup)
    run_method_setup(resource)
