import itertools
import os
import uuid
from pathlib import Path

import click
import texttable as tt
from mint.utils import check_is_none, create_yaml_from_resource, obtain_id
from mint.executor import execute_setup
from mint._utils import log
from mint.modelcatalogapi import get_setup
from modelcatalog import ApiException, SampleResource

def edit_inputs_setup(model_configuration):
    click.secho("The information of the setup is incomplete", fg="yellow")
    for _input in model_configuration.has_input:
        if not "hasFixedResource" in _input:
            print_data_property_table(_input)
            url = click.prompt('Please, enter the url of the previous input', type=click.STRING)
            s = SampleResource(id="https://w3id.org/okn/i/mint/".format(str(uuid.uuid4())),
                               data_catalog_identifier="FFF-3s5c112e-c7ae-4cda-ba23-2e4f2286a18o",
                               value=[url])
            _input["hasFixedResource"] = [s.to_dict()]
    return model_configuration


def edit_parameter_config_or_setup(resource, auto=False):
    for _input in resource.has_parameter:
        print("=======================================================")
        _id = obtain_id(check_is_none(_input, 'id'))
        description = check_is_none(_input, 'description')
        datatype = check_is_none(_input, 'hasDataType')
        click.secho("Name: {}".format(_id), fg="yellow")
        click.secho("Description: {}".format(description), fg="yellow")
        click.secho("Format: {}".format(datatype), fg="yellow")
        default_value = check_is_none(_input, 'hasDefaultValue')

        if not default_value:
            value = click.prompt('Enter the value for the parameter.')
        else:
            default_value = default_value[0]
            if auto:
                value = default_value
                click.echo("Using the default valuer {}".format(default_value))
            else:
                value = click.prompt('Enter the value for the parameter:', default=default_value)


def print_data_property_table(resource):
    tab = tt.Texttable()
    headings = ['Property', 'Value']
    tab.header(headings)
    for key, value in resource.items():
        if isinstance(value, dict) or key == "type":
            continue
        tab.add_row([key,value])
    print(tab.draw())


def edit_parameter_config_setup(resource):
    print_table(resource.to_dict())


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


def edit_setup(setup):
    """
    Edit the inputs and parameters of a setup
    """
    edit_parameter_config_setup(resource=setup)


def run_method(editable, name):
    """
    Call download_setup(): Download the setup(s) as yaml file
    Call execute_setup(): Read the yaml file and execute
    """
    click.secho("Downloading the inputs and parameters", fg="green")
    setup = get_setup(name)
    name = obtain_id(setup.id)
    if editable:
        edit_setup(setup)

    try:
        file_path = create_yaml_from_resource(resource=setup, name=name, output=Path('.'))
        read_and_execute(file_path)
    except ApiException as e:
        click.secho("Unable to download the setup {}".format(e), fg="red")
        exit(1)


def run_method_setup(setup):
    """
    Call download_setup(): Download the setup(s) as yaml file
    Call execute_setup(): Read the yaml file and execute
    """
    name = obtain_id(setup.id)
    try:
        file_path = create_yaml_from_resource(resource=setup, name=name, output=Path('.'))
        read_and_execute(file_path)
    except ApiException as e:
        click.secho("Unable to download the setup {}".format(e), fg="red")
        exit(1)


def read_and_execute(file_path):
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
