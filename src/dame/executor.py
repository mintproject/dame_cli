import os
import platform
import subprocess
import uuid
from pathlib import Path

import click
import docker
from yaml import load, Loader

from dame.utils import download_data_file, download_extract_zip, obtain_id, convert_object_to_dict, find_executor
from dame._utils import log

KEYS_REQUIRED_PARAMETER = {"has_default_value", "position"}
KEYS_REQUIRED_OUTPUT = {"label", "has_format", "position"}
KEYS_REQUIRED_INPUT = {"has_fixed_resource"}

if platform.system() == "Linux":
    SINGULARITY_CWD_LINE = "/usr/bin/singularity exec docker://{}"
elif platform.system() == "Darwin":
    SINGULARITY_CWD_LINE = "/usr/local/bin/singularity exec docker://{}"

EXECUTION_DIRECTORY = "executions"

DOCKER_ENGINE = "DOCKER"
SINGULARITY_ENGINE = "SINGULARITY"


def get_engine():
    if platform.system() == "Linux" or platform.system() == "Darwin":
        return SINGULARITY_ENGINE
    elif platform.system() == "Darwin" or platform.system() == "Windows":
        return DOCKER_ENGINE


def build_input(inputs, _dir):
    line = ""
    for _input in inputs:
        _input = convert_object_to_dict(_input)
        if not _input.keys() >= KEYS_REQUIRED_INPUT:
            raise ValueError(f'{_input["id"]} has not a fixedResource')
        url = _input["has_fixed_resource"][0]["value"][0]
        format = _input["has_format"][0]
        file_path, file_name = download_data_file(url, _dir, format)
        position = _input["position"][0]
        line += " -i{} {}".format(position, file_name)
    return line


def build_output(outputs):
    line = ""
    for _output in outputs:
        _output = convert_object_to_dict(_output)
        if not _output.keys() >= KEYS_REQUIRED_OUTPUT:
            raise ValueError(f'{_output["id"]}  has not the required information')
        label = _output["label"][0]
        extension = _output["has_format"][0]
        position = _output["position"][0]
        line += " -o{} {}.{}".format(position, label, extension)
    return line


def build_parameter(parameters):
    line = ""
    for _parameter in parameters:
        _parameter = convert_object_to_dict(_parameter)
        if not _parameter.keys() >= KEYS_REQUIRED_PARAMETER:
            raise ValueError(f'{_parameter["id"]} has not the required information ')
        if "has_fixed_resource" in _parameter:
            value = _parameter["has_fixed_resource"][0]
        else:
            value = _parameter["has_default_value"][0]
        position = _parameter["position"][0]
        line += " -p{} {}".format(position, value)
    return line


def build_command_line(resource, _dir):
    line = './run '
    setup_name = obtain_id(resource.id)
    inputs = resource.has_input
    try:
        parameters = resource.has_parameter
    except:
        parameters = None
    outputs = resource.has_output
    component_url = resource.has_component_location[0]
    software_image = resource.has_software_image
    if software_image:
        has_software_image = software_image[0].label[0]
    else:
        raise ValueError("Software is not available")
    component_dir = download_extract_zip(component_url, _dir, setup_name)
    path = Path(component_dir)
    src_path = path / "src"
    if inputs:
        l = build_input(inputs, src_path)
        line += " {}".format(l)
    if outputs:
        l = build_output(outputs)
        line += " {}".format(l)
    if parameters is not None:
        l = build_parameter(parameters)
        line += " {}".format(l)
    return has_software_image, line, src_path


def prepare_execution(setup_path):
    """
    Create the execution directory and call the method to get the inputs and execution line
    :param setup_path: the path of the YAML file
    :type setup_path: Path
    :return:
        - src_path: (:py:class:`Path`) - Path component source directory
        - execution_dir: (:py:class:`Path`) - Path execution directory
        - setup_cmd_line: (:py:class:`Path`) - The execution line (./run)
        - setup_name: (:py:class:`Path`) - The name of setup
        - image: (:py:class:`Path`) - The name of the image
    """
    _dir = Path("%s/" % EXECUTION_DIRECTORY)
    _dir.mkdir(parents=True, exist_ok=True)
    setup_dict = load(setup_path.open(), Loader=Loader)
    setup_name = obtain_id(setup_dict.id)
    execution_dir = "{}/{}_{}".format(_dir, setup_name, uuid.uuid1())
    execution_dir_path = Path(execution_dir)
    execution_dir_path.mkdir(parents=True, exist_ok=True)
    try:
        image, setup_cmd_line, src_path = build_command_line(setup_dict, execution_dir_path)
    except Exception as e:
        raise e
    return src_path, execution_dir, setup_cmd_line, setup_name, image


def run_docker(cwd_path, execution_dir, setup_cmd_line, setup_name, image):
    client = docker.from_env()
    item = {
        "cmd": setup_cmd_line.split(' '),
        "directory": cwd_path,
        "name": setup_name
    }
    _ = subprocess.Popen(["chmod", "+x", "run"], cwd=item["directory"])
    res = client.containers.run(command=item["cmd"],
                                image=image,
                                volumes={str(Path(item["directory"]).absolute()): {'bind': '/tmp/mint', 'mode': 'rw'}},
                                working_dir='/tmp/mint',
                                detach=True,
                                stream=True
                                )

    for chunk in res.logs(stream=True):
        print(chunk)

    exit(0)
    status = {
        "exitcode": 0,
        "name": setup_name
    }
    return status


def run_singularity(singularity_cmd, execution_dir, component_dir, setup_name):
    log_file_path = "{}/output.log".format(execution_dir)
    item = {
        "log": open(log_file_path, 'wb'),
        "name": setup_name
    }
    with open(log_file_path, 'wb') as log_file:
        log.info(f'Execution {setup_name} running,  check the logs on {log_file_path}')
        _ = subprocess.Popen(["chmod", "+x", "run"], stdout=log_file, stderr=log_file, cwd=component_dir)
        proc = subprocess.Popen(singularity_cmd, stdout=log_file, stderr=log_file, cwd=component_dir)
        proc.wait()
        status = {
            "exitcode": proc.returncode,
            "name": item["name"]
        }
    return status


def get_singularity_cmd(image, setup_cmd_line):
    setup_singularity_line = SINGULARITY_CWD_LINE.format(image)
    setup_cmd_line = "{} {}".format(setup_singularity_line, setup_cmd_line)
    return setup_cmd_line.split(' ')
