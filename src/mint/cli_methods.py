import os
from pathlib import Path

import click
from utils import download_setup, check_is_none
from mint.executor import execute_setup
from mint._utils import log

def edit_inputs_setup(model_configuration):
    for _input in model_configuration.has_input:
        print("=======================================================")
        _id = check_is_none(_input, 'id')
        description = check_is_none(_input, 'description')
        label = check_is_none(_input, 'label')
        _format = check_is_none(_input, 'format')
        variables = check_is_none(_input, 'variables')

def edit_parameter_config_or_setup(auto, model_configuration):
    for _input in model_configuration.has_parameter:
        print("=======================================================")
        print(check_is_none(_input, 'id'))
        print(check_is_none(_input, 'description'))
        print(check_is_none(_input, 'hasDataType'))
        default_value = check_is_none(_input, 'hasDefaultValue')
        if default_value and not auto:
            default_value = default_value[0]
            value = click.prompt('Enter the value for the parameter. Default value', default=default_value)
        elif not default_value:
            value = click.prompt('Enter the value for the parameter.')
        elif default_value:
            click.echo("Using the default valuer {}".format(default_value))


def edit_inputs_model_configuration(model_configuration):
    for _input in model_configuration.has_input:
        print("=======================================================")
        _id = check_is_none(_input, 'id')
        description = check_is_none(_input, 'description')
        label = check_is_none(_input, 'label')
        _format = check_is_none(_input, 'format')
        variables = check_is_none(_input, 'variables')
        print(_id)
        print(description)
        print(variables)
        print(_format)
        url = click.prompt('Please enter the url', type=click.STRING)
        s = SampleResource(data_catalog_identifier="FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o",
                           value=url,
                           description=description,
                           label=label)


def run_method(name):
    """
    Call download_setup(): Download the setup(s) as yaml file
    Call execute_setup(): Read the yaml file and execute
    """
    click.secho("Downloading the inputs and parameters", fg="green")
    file_path = download_setup(setup_id=name, output=Path('.'))
    click.secho("Executing the setup", fg="green")
    status = execute_setups(file_path)
    for setup in status:
        if setup["exitcode"] == 0:
            click.secho("{} ok".format(setup["name"]), fg="green")
        else:
            click.secho("{} failed".format(setup["name"]), fg="red")


def execute_setups(path):
    """
    Find the setup files if the path is a directory and execute it
    """
    setup_files = find_setup_files(path)
    try:
        status = execute_setup(setup_files)
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

