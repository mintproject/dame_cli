from dame.executor import KEYS_REQUIRED_INPUT, convert_object_to_dict, KEYS_REQUIRED_PARAMETER
from dame.utils import download_file
import tempfile
from yaml import load, Loader, dump
from pathlib import Path

def run(setup: dict, file_path: Path):
    component_url = setup.has_component_location[0]
    values_file = create_values_file(setup, file_path)
    spec_file = file_path / "spec.yaml"
    with open(spec_file, 'wb+') as f:
        f.write(download_file(component_url))
        

def create_values_file(resource: dict, file_path: Path):
    try:
        inputs = resource.has_input if resource.has_input else []
    except:
        inputs = []
    try:
        parameters = resource.has_parameter if resource.has_parameter else []
    except:
        parameters = []
    spec = build_input(inputs, parameters)
    temp_values_file = file_path / "values.yml"
    write_to_yaml(temp_values_file, spec)
    return temp_values_file


def write_to_yaml(config_yaml_path: Path, spec):
    """
    This function makes sure that the comments get saved when writing new data to the yaml file
    @param config_yaml_path: path
    @param spec: data for yaml
    """
    with open(config_yaml_path, 'w') as f:
        dump(spec, f, sort_keys=False)


def build_input(inputs, parameters):
    spec = {}
    for _input in inputs:
        _input = convert_object_to_dict(_input)
        if not _input.keys() >= KEYS_REQUIRED_INPUT or _input['has_fixed_resource'] is None:
            raise ValueError(f'{_input["id"]} has not a fixedResource')
        else:
            url = _input["has_fixed_resource"][0]["value"][0]
            label = _input["label"][0]
            spec[label] = {"type": "File", "path": url}


    for _parameter in parameters:
        _parameter = convert_object_to_dict(_parameter)
        if not _parameter.keys() >= KEYS_REQUIRED_PARAMETER:
            raise ValueError(f'{_parameter["id"]} has not the required information ')
        if "has_fixed_resource" in _parameter:
            value = _parameter["has_fixed_resource"][0]
        else:
            value = _parameter["has_default_value"][0]
        label = _parameter["label"][0]
        spec[label] = value
    print(spec)
    return spec