# -*- coding: utf-8 -*-
"""
dame.

:license: Apache 2.0
"""
import logging
import click
import semver
from modelcatalog import OpenApiException, ApiException

import dame
from dame import _utils
from dame.cli_methods import verify_input_parameters, run_method_setup, show_model_configuration_details, \
    print_table_list
from dame.modelcatalogapi import get_setup, get_model_configuration, list_model_configuration, list_setup
from dame.utils import obtain_id

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from pathlib import Path

@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = ".".join(_utils.get_latest_version().split(".")[:3])
    cv = ".".join(dame.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using dame-cli version {dame.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade dame-cli' command.""",
            fg="yellow",
        )


@cli.command(help="Show dame-cli version.")
def version(debug=False):
    click.echo(f"DAME: v{dame.__version__}")


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
@click.option('--interactive/--non-interactive', default=True)
def run(name, interactive):
    try:
        config = get_model_configuration(name)
    except ApiException as e:
        click.secho("{}".format(e.reason))
        exit(0)
    click.clear()
    if "ModelConfigurationSetup" in config.type:
        resource = get_setup(name)
    elif "ModelConfiguration" in config.type:
        resource = get_model_configuration(name)
    try:
        show_model_configuration_details(resource)
    except AttributeError as e:
        click.secho("Unable to run it: {}".format(str(e)), fg="red")
        exit(1)
    try:
        verify_input_parameters(resource, interactive)
    except ValueError as e:
        click.secho("Unable to run. Please use interactive mode", fg="yellow")
        exit(1)
    run_method_setup(resource, interactive)

@cli.group()
def model_configuration():
    """Manages model configurations"""
@model_configuration.command(name="list", help="List configurations")
def _list():
    items = list_model_configuration(label=None)
    print_table_list(items)

@click.argument(
    "name",
    type=click.STRING
)
@model_configuration.command(name="show", help="Show model configuration")
def _show(name):
    try:
        _setup = get_model_configuration(name)
    except ApiException as e:
        click.secho("{}".format(e.reason))
        exit(0)
    try:
        show_model_configuration_details(_setup)
    except AttributeError as e:
        click.secho("This setup is not executable.\n".format(e), fg="red")

@cli.group()
def setup():
    """Manages model configuration setup"""
@setup.command(name="list", help="List model configuration setups")
def _list():
    items = list_setup(label=None)
    print_table_list(items)


@click.argument(
    "name",
    type=click.STRING
)
@setup.command(name="show", help="Show model configuration setups")
def _show(name):
    try:
        _setup = get_setup(name)
    except ApiException as e:
        click.secho("{}".format(e.reason))
        exit(0)
    try:
        show_model_configuration_details(_setup)
    except AttributeError as e:
        click.secho("This setup is not executable.\n".format(e), fg="red")
