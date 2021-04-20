# -*- coding: utf-8 -*-
"""
dame.

:license: Apache 2.0
"""
import logging
from pathlib import Path

import click
import semver
from modelcatalog import ApiException, Configuration

import dame
from dame import _utils
from dame.cli_methods import verify_input_parameters, run_method_setup, show_model_configuration_details, \
    print_table_list, edit_parameters, show_model_configuration_details_dt
from dame.configuration import configure_credentials, get_credentials, DEFAULT_PROFILE
from dame.modelcatalogapi import get_setup, get_model_configuration, list_model_configuration, list_setup, \
    get_data_transformation, get_transformation_dataset
from urllib.parse import urlparse

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
            f"""WARNING: You are using dame-cli version {dame.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade dame-cli' command.""",
            fg="yellow",
        )


@cli.command(help="Configure credentials")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
@click.option('--server', prompt='Model Catalog API',
              help='The Model Catalog API', required=True, default=Configuration().host, show_default=True)
@click.option('--username', prompt='Username',
              help='Your email.', required=True, default="mint@isi.edu", show_default=True)
def credentials(server, username, profile="default"):
    try:
        configure_credentials(server, username, profile)
    except Exception:
        click.secho(f"Failed", fg="red")
    click.secho(f"Success", fg="green")


@cli.command(help="Show dame-cli version.")
def version():
    click.echo(f"DAME: v{dame.__version__}")


@cli.command(help="Open the Model Catalog in your browser")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def browse(profile):
    credentials = get_credentials(profile)
    server = ''
    if "server" in credentials:
        click.secho(f"""Looking User Interface {credentials['server']}""")
        server = credentials['server']
    else:
        click.secho("Unable to find the model catalog", fg="red")
    domain = urlparse(server).netloc
    mapping = {
        "api.models.mint.isi.edu": "https://models.mint.isi.edu",
        "api.models.wildfire.mint.isi.edu" : "https://wildfire.models.mint.isi.edu"
    }
    if not domain or domain not in mapping:
        click.secho("Unable to find the model catalog", fg="red")

    click.launch(mapping[domain])


@cli.command(help="Run a model configuration or model configuration setup")
@click.argument(
    "name",
    type=click.STRING
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    metavar="<profile-name>",
    default="default",
)
@click.option(
    "--data",
    "-d",
    type=click.Path(exists=False, dir_okay=True, resolve_path=True),
)
@click.option('--interactive/--non-interactive', default=True)
def run(name, interactive, profile, data):
    if not data or not Path(data).exists():
        data = None
    else:
        data = Path(data)

    try:
        config = get_model_configuration(name, profile=profile)
    except ApiException as e:
        click.secho("{}".format(e.reason))
        exit(0)
    click.clear()
    if "ModelConfigurationSetup" in config.type:
        resource = get_setup(name, profile=profile)
    elif "ModelConfiguration" in config.type or "DataTransformation":
        resource = get_model_configuration(name, profile=profile)
    try:
        show_model_configuration_details(resource)
    except AttributeError as e:
        click.secho("Unable to run it: {}".format(str(e)), fg="red")
        exit(1)


    try:
        verify_input_parameters(resource, interactive, data, profile)
    except ValueError as e:
        click.secho("Unable to run. Please use interactive mode", fg="yellow")
        exit(1)
    try:
        if interactive and click.confirm("Do you want to edit the parameters?"):
            edit_parameters(resource, interactive)
    except ValueError as e:
        click.secho("Unable to run. Please use interactive mode", fg="yellow")
        exit(1)
    run_method_setup(resource, interactive, data)


"""
Run a modelconfiguration or modelconfiguration
"""


@cli.group()
def model_configuration():
    """Manages model configurations"""


@model_configuration.command(name="list", help="List configurations")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=DEFAULT_PROFILE,
    metavar="<profile-name>",
)
def model_configuration_list(profile):
    items = list_model_configuration(label=None, profile=profile)
    print_table_list(items)


@click.argument(
    "name",
    type=click.STRING
)
@model_configuration.command(name="show", help="Show model configuration")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=DEFAULT_PROFILE,
    metavar="<profile-name>",
)
def model_configuration_show(name, profile):
    try:
        _setup = get_model_configuration(name, profile=profile)
    except ApiException as e:
        click.secho("{}".format(e.reason))
        exit(1)
    try:
        show_model_configuration_details(_setup)
    except AttributeError as e:
        click.secho("This setup is not executable.\n".format(e), fg="red")
        exit(1)

@cli.group()
def setup():
    """Manages model configuration setup"""


@setup.command(name="list", help="List model configuration setups")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=DEFAULT_PROFILE,
    metavar="<profile-name>",
)
def setup_list(profile):
    items = list_setup(label=None, profile=profile)
    print_table_list(items)


@click.argument(
    "name",
    type=click.STRING
)
@setup.command(name="show", help="Show model configuration setups")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=DEFAULT_PROFILE,
    metavar="<profile-name>",
)
def setup_show(name, profile):
    try:
        _setup = get_setup(name, profile=profile)
    except ApiException as e:
        click.secho("{}".format(e.reason))
        exit(1)
    try:
        show_model_configuration_details(_setup)
    except AttributeError as e:
        click.secho("This setup is not executable.\n".format(e), fg="red")


@setup.command(name="list", help="List model configuration setups")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default=DEFAULT_PROFILE,
    metavar="<profile-name>",
)
def setup_list(profile):
    items = list_setup(label=None, profile=profile)
    print_table_list(items)


@cli.group()
def transformation():
    """Manages Data transformation"""


@transformation.command(name="list")
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
@click.argument(
    "dataset_id",
    type=click.STRING,
    required=False
)
def transformation_list(dataset_id, profile):
    """
    List the transformations available. For example:

    $ dame transformation list

    You can see the transformation available for a DataSetSpecification using

    $ dame transformation list topoflow36_2.1.0_rainRates
    """
    if dataset_id:
        items = get_transformation_dataset(dataset_id, profile=profile)
    else:
        items = get_data_transformation(profile=profile)
    print_table_list(items)


@transformation.command(name="run")
@click.argument(
    "data_transformation_id",
    type=click.STRING
)
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
def transformation_run(data_transformation_id, profile):
    """
    You must pass the argument ID (ID of the transformation)

    For example:

    dame transformation run topoflow_climate
    """
    resource = get_model_configuration(data_transformation_id, profile=profile)
    interactive = True
    data = Path('.')
    try:
        show_model_configuration_details(resource)
    except AttributeError as e:
        click.secho("This setup is not executable.\n".format(e), fg="red")
    run_method_setup(resource, interactive, data)
