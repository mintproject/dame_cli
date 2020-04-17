import os
import uuid
from pathlib import Path

import click
import texttable as tt
from dame.utils import create_yaml_from_resource, obtain_id
from dame.executor import prepare_execution, run_execution
from dame._utils import log
from dame.modelcatalogapi import get_setup
from modelcatalog import ApiException, SampleResource


def verify_input_parameters(model_configuration):
    for _input in model_configuration.has_input:
        if not hasattr(_input, "has_fixed_resource"):
            click.secho("The information of the setup is incomplete", fg="yellow")
            print_data_property_table(_input)
            url = click.prompt('Please, enter the url of the previous input', type=click.STRING)
            s = SampleResource(id="https://w3id.org/okn/i/mint/".format(str(uuid.uuid4())),
                               data_catalog_identifier="FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o",
                               value=[url])
            _input.has_fixed_resource = [s.to_dict()]
    click.secho("The information of the setup is complete", fg="green")
    return model_configuration


def print_data_property_table(resource):
    resource_dict = resource.to_dict()
    tab = tt.Texttable(max_width=100)
    headings = ['Property', 'Value']
    tab.header(headings)
    for key, value in resource_dict.items():
        if isinstance(value, dict) or key == "type" or key == "has_presentation":
            continue
        tab.add_row([key, value])
    print(tab.draw())


# def run_method(editable, name):
#     """
#     Call download_setup(): Download the setup(s) as yaml file
#     Call execute_setup(): Read the yaml file and execute
#     """
#     click.secho("Downloading the inputs and parameters", fg="green")
#     setup = get_setup(name)
#     name = obtain_id(setup.id)
#     # if editable:
#     #     edit_setup(setup)
#
#     try:
#         file_path = create_yaml_from_resource(resource=setup, name=name, output=Path('.'))
#         read_and_execute(file_path)
#     except ApiException as e:
#         click.secho("Unable to download the setup {}".format(e), fg="red")
#         exit(1)


def run_method_setup(setup):
    """
    Call download_setup(): Download the setup(s) as yaml file
    Call execute_setup(): Read the yaml file and execute
    """
    try:
        cwd_path, execution_dir, setup_cmd_line, setup_name = convert_setup_file(setup)
        status = execute_setups(cwd_path, execution_dir, setup_cmd_line, setup_name)
        if status["exitcode"] == 0:
            click.secho("[{}] The execution has been successful".format(status["name"]), fg="green")
            click.secho("[{}] Results available at: {} ".format(status["name"], cwd_path), fg="green")
        else:
            click.secho("[{}] The execution has failed".format(status["name"]), fg="red")
    except ApiException as e:
        click.secho("Unable to download the setup {}".format(e), fg="red")
        exit(1)


def convert_setup_file(setup):
    """
    Find the setup files if the path is a directory and execute it
    """
    name = obtain_id(setup.id)
    file_path = create_yaml_from_resource(resource=setup, name=name, output=Path('.'))
    return prepare_execution(file_path)


def execute_setups(cwd_path, execution_dir, setup_cmd_line, setup_name):
    """
    Find the setup files if the path is a directory and execute it
    """
    try:
        click.echo("Execution line \ncd {}\n{}".format(cwd_path, setup_cmd_line))
        click.confirm("Do you want to run the setup?", default=True)
        status = run_execution(cwd_path, execution_dir, setup_cmd_line, setup_name)
    except Exception as e:
        log.error(e, exc_info=True)
        exit(1)
    return status


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

# def edit_inputs_model_configuration(model_configuration):
#     for _input in model_configuration.has_input:
#         print("=======================================================")
#         _id = check_is_none(_input, 'id')
#         description = check_is_none(_input, 'description')
#         label = check_is_none(_input, 'label')
#         _format = check_is_none(_input, 'format')
#         print_data_property_table(_input)
#         url = click.prompt('Please enter the url of the input shown above', type=click.STRING)
#         s = SampleResource(data_catalog_identifier="FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o",
#                            value=url,
#                            description=description,
#                            label=label)
#         _input.has_fixed_resource = [s]

# def edit_setup(setup):
#     """
#     Edit the inputs and parameters of a setup
#     """
#     edit_parameter_config_setup(resource=setup)


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
