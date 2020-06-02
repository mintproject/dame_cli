import os
import stat
import uuid
from pathlib import Path

import click
import texttable as tt
from modelcatalog import ApiException, SampleResource

from dame._utils import log
from dame.executor import prepare_execution, get_engine, DOCKER_ENGINE, \
    SINGULARITY_ENGINE, get_singularity_cmd, run_singularity, run_docker, get_docker_cmd
from dame.local_file_manager import find_file_directory
from dame.utils import create_yaml_from_resource, obtain_id
from dame.utils import url_validation

SCRIPT_FILENAME = "run"

data_set_property = ["id", "label"]
parameter_set_property = ["id", "label", "has_default_value"]


def show_model_configuration_details(model_configuration):
    click.echo(click.style("Information about the model configuration", bold=True))
    if model_configuration and hasattr(model_configuration, "has_input") and getattr(model_configuration, "has_input"):
        click.echo(click.style("Inputs", bold=True))
        for _input in model_configuration.has_input:
            if hasattr(_input, "has_fixed_resource") and _input.has_fixed_resource and hasattr(_input.has_fixed_resource[0], "value"):
                click.echo("- {}: {}".format(_input.label[0], _input.has_fixed_resource[0].value[0]))
            else:
                label = getattr(_input, "label") if hasattr(_input, "label") else getattr(_input, "id")
                click.echo("- {}: {}".format(label[0], "No information"))
    if model_configuration and hasattr(model_configuration, "has_parameter") and getattr(model_configuration, "has_parameter"):
        click.echo(click.style("Parameters", bold=True))
        for _parameter in model_configuration.has_parameter:
            short_value(_parameter, "has_default_value")
    if hasattr(model_configuration, "has_software_image") and getattr(model_configuration, "has_software_image"):
        try:
            click.echo(click.style("Docker Image", bold=True))
            image = getattr(model_configuration, "has_software_image")[0].label[0]
            click.echo("- {}: {} - https://hub.docker.com/r/{} ".format("Name", image, image.split(':')[0]))
        except AttributeError as e:
            raise AttributeError("No information available about the Docker Image.")
    else:
        raise AttributeError("No information available about the Docker Image.")
    if hasattr(model_configuration, "has_component_location") and getattr(model_configuration, "has_component_location"):
        try:
            click.echo(click.style("Component Location", bold=True))
            image = getattr(model_configuration, "has_component_location")[0]
            click.echo("- {}: {}".format("Link", image))
        except AttributeError as e:
            raise AttributeError("No information available about the executable component Location")
    else:
        raise AttributeError("No information available about the executable component Location")


def short_value(resource, prop):
    if hasattr(resource, prop):
        value = getattr(resource, prop)
        click.echo("- {}: {}".format(getattr(resource, "label")[0], value[0]))


def verify_input_parameters(model_configuration, interactive, data_dir):
    for _input in model_configuration.has_input:
        uri = None
        if (not hasattr(_input, "has_fixed_resource") or _input.has_fixed_resource is None) and interactive:
            if hasattr(_input, "label") and hasattr(_input, "has_format"):
                click.secho("To run this model configuration,"
                            "a {} file (.{} file) is required.".format(_input.label[0], _input.has_format[0]),
                            fg="yellow")
            elif hasattr(_input, "label"):
                click.secho("To run this model configuration, a {} file is required.".format(_input.label[0]),
                            fg="yellow")
            else:
                click.secho("To run this model configuration, a {} file is required."
                            .format(_input.id), fg="yellow")
            if data_dir and hasattr(_input, "has_format") and click.confirm(
                    "Do you want to search the file in the directory {}".format(data_dir), default=True):
                uri = find_file_directory(data_dir, _input.has_format[0])

            if uri is None:
                uri = click.prompt('Please enter a url')
                uri = uri.replace(" ", '')
                while not url_validation(uri):
                    uri = click.prompt('Please enter a url')

            create_sample_resource(_input, uri)
        elif not hasattr(_input, "has_fixed_resource") and not interactive:
            raise ValueError("Missing information")
    click.secho("The information needed to run the model is complete, and I can execute the model as follows:",
                fg="green")
    return model_configuration


def create_sample_resource(_input, uri):
    s = SampleResource(id="https://w3id.org/okn/i/mint/".format(str(uuid.uuid4())),
                       data_catalog_identifier="FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o",
                       value=[uri])
    _input.has_fixed_resource = [s.to_dict()]


# def edit_parameter_config_or_setup(resource, auto=False):
#     """not used"""
#     for parameter in resource.has_parameter:
#         logging.info("Checking {}".format(parameter))
#         logging.info("Checking {}".format(check_is_none(parameter, 'id')))
#         _id = obtain_id(check_is_none(parameter, 'id'))
#         default_value = check_is_none(parameter, 'has_default_value')
#         print_data_property_table(parameter)
#         if not default_value:
#             value = click.prompt('Enter the value for the parameter.')
#         else:
#             default_value = default_value[0]
#             if auto:
#                 value = default_value
#                 click.echo("Using the default valuer {}".format(default_value))
#             else:
#                 value = click.prompt('Enter the value for the parameter:', default=default_value)
#         parameter["hasFixedValue"] = [value]


def print_data_property_table(resource, property_selected={}):
    resource_dict = resource.to_dict()
    tab = tt.Texttable(max_width=100)
    headings = ['Property', 'Value']
    tab.header(headings)
    for key, value in resource_dict.items():
        if isinstance(value, dict) or key == "type" or key == "has_presentation":
            continue
        if property_selected:
            if key not in property_selected:
                continue
        tab.add_row([key, value])
    print(tab.draw())


def run_method_setup(setup, interactive, data_dir):
    """
    Call download_setup(): Download the setup(s) as yaml file
    Call execute_setup(): Read the yaml file and execute
    """
    try:
        name = obtain_id(setup.id)
        file_path = create_yaml_from_resource(resource=setup, name=name, output=Path('.'))
        component_src_dir, execution_dir, setup_cmd_line, setup_name, image = prepare_execution(file_path)

    except ApiException as e:
        click.secho("Unable to download the setup {}".format(e), fg="red")
        exit(1)

    try:
        execute_setups(component_src_dir, execution_dir, setup_cmd_line, setup_name, image, interactive)
        click.secho("[{}] The execution has been successful".format(setup_name), fg="green")
        click.secho("[{}] Results available at: {} ".format(setup_name, component_src_dir), fg="green")
    except Exception as e:
        log.error(e, exc_info=True)
        click.secho("[{}] The execution has failed".format(setup_name), fg="red")
        exit(1)


def execute_setups(component_src_dir, execution_dir, setup_cmd_line, setup_name, image, interactive):
    """
    Find the setup files if the path is a directory and execute it
    """
    try:
        engine = get_engine()
    except FileNotFoundError:
        click.secho("Singularity is not installed", fg="red")
        exit(1)
    except Exception as e:
        click.secho("Docker is not running or installed".format(e), fg="red")
        exit(1)

    os.chmod(component_src_dir / SCRIPT_FILENAME, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    if engine == DOCKER_ENGINE:
        try:
            mint_volumes = {str(Path(component_src_dir).absolute()): {'bind': '/tmp/mint', 'mode': 'rw'}}
            docker_cmd_pretty = get_docker_cmd(image, setup_cmd_line, mint_volumes)
            show_execution_info(component_src_dir, interactive, docker_cmd_pretty)
            run_docker(setup_cmd_line, execution_dir, component_src_dir, setup_name, image, mint_volumes)
        except Exception as e:
            raise e

    elif engine == SINGULARITY_ENGINE:
        try:
            singularity_cmd = get_singularity_cmd(image, setup_cmd_line)
            singularity_cmd_pretty = " ".join(singularity_cmd)
            show_execution_info(component_src_dir, interactive, singularity_cmd_pretty)
            run_singularity(singularity_cmd, execution_dir, component_src_dir, setup_name)
        except Exception as e:
            raise e


def show_execution_info(component_src_dir, interactive, singularity_cmd_pretty):
    click.echo("Invocation command \ncd {}\n{}".format(component_src_dir, singularity_cmd_pretty))
    if interactive and not click.confirm("Do you want to proceed and submit it for execution?", default=True):
        exit(0)


def find_setup_files(path):
    setup_files = []
    if os.path.isdir(path):
        path = Path(path)
        for file in os.listdir(path):
            if file.endswith(".yaml") or file.endswith(".yml"):
                setup_files.append(path / file)
    elif os.path.isfile(path):
        default_path = Path('.')
        setup_files.append(default_path / path)
    return setup_files


def print_table_list(items):
    headings = ['Id', 'Description']
    tab = tt.Texttable()
    tab.header(headings)
    for item in items:
        _id = obtain_id(item.id)
        _description = "".join(item.description) if hasattr(item, "description") and getattr(item, "description") else "No information"
        tab.add_row([_id, _description])
    print(tab.draw())

def print_table_list_data(items):
    headings = ['Id', 'Description']
    tab = tt.Texttable(max_width=90)
    tab.header(headings)
    for item in items:
        _id = item["id"]
        _description = "".join(item["description"]) if "description" in item and item["description"] else "No information"
        tab.add_row([_id, _description])
    print(tab.draw())
