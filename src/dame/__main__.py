# -*- coding: utf-8 -*-
"""
dame.

:license: Apache 2.0
"""
from pathlib import Path

import click
import semver
from modelcatalog import ApiException, Configuration

import dame
from dame import _utils
from dame.cli_methods import verify_input_parameters, run_method_setup, show_model_configuration_details, \
    print_table_list
from dame.configuration import configure_credentials, DEFAULT_PROFILE
from dame.modelcatalogapi import get_setup, get_model_configuration, list_model_configuration, list_setup
from dame.transformations import list_data_transformation, show_data_transformation, run_data_transformation

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
def configure(server, username, profile="default"):
    try:
        configure_credentials(server, username, profile)
    except Exception:
        click.secho(f"Failed", fg="red")
    click.secho(f"Success", fg="green")


@cli.command(help="Show dame-cli version.")
def version():
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
@click.option(
    "--profile",
    "-p",
    envvar="MINT_PROFILE",
    type=str,
    default="default",
    metavar="<profile-name>",
)
@click.option(
    "--data",
    "-d",
    type=click.Path(exists=False, dir_okay=True, resolve_path=True),
    default="data",
)
@click.option('--interactive/--non-interactive', default=True)
def run(name, interactive, profile, data):
    if not Path(data).exists():
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
    elif "ModelConfiguration" in config.type:
        resource = get_model_configuration(name, profile=profile)
    try:
        show_model_configuration_details(resource)
    except AttributeError as e:
        click.secho("Unable to run it: {}".format(str(e)), fg="red")
        exit(1)
    try:
        verify_input_parameters(resource, interactive, data)
    except ValueError as e:
        click.secho("Unable to run. Please use interactive mode", fg="yellow")
        exit(1)
    run_method_setup(resource, interactive, data)


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


@transformation.command(name="list", help="List transformations")
def transformation_list():
    items = list_data_transformation()


# @transformation.command(name="show", help="Show transformation")
# @click.argument(
#     "name",
#     type=click.STRING
# )
# def transformation_show(name):
#     items = show_data_transformation(name)

@transformation.command(name="run")
@click.argument(
    "id",
    type=click.STRING
)
@click.option(
    "--input_dir",
    "-i",
    type=click.Path(exists=False, dir_okay=True, resolve_path=True),
    required=True
)
def transformation_run(id, input_dir):
    """
    You must pass the argument ID (ID of the transformation)

    And the directory using the option -i/--input_dir

    For example:

    dame transformation run topoflow_climate -i data/
    """
    run_data_transformation(id, Path(input_dir))
