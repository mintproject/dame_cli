import platform
import shutil
import subprocess
import uuid
from pathlib import Path

import docker
import validators
from yaml import load, Loader

from dame._utils import log
from dame.utils import download_extract_zip, obtain_id, convert_object_to_dict, download_data_file

SINGULARITY_BIN = Path("/usr/bin/singularity")
SINGULARITY_LOCAL_BIN = Path("/usr/local/bin/singularity")

KEYS_REQUIRED_PARAMETER = {"has_default_value", "position"}
KEYS_REQUIRED_OUTPUT = {"label", "has_format", "position"}
KEYS_REQUIRED_INPUT = {"has_fixed_resource"}

EXECUTION_DIRECTORY = "executions"

DOCKER_ENGINE = "DOCKER"
SINGULARITY_ENGINE = "SINGULARITY"


def get_singularity():
    try:
        if SINGULARITY_BIN.exists():
            return SINGULARITY_BIN
        elif SINGULARITY_LOCAL_BIN.exists():
            return SINGULARITY_LOCAL_BIN
    except FileNotFoundError:
        raise FileNotFoundError


def get_engine():
    if platform.system() == 'Linux':
        try:
            get_singularity()
            return SINGULARITY_ENGINE
        except FileNotFoundError:
            try:
                client = docker.from_env()
                client.info()
                return DOCKER_ENGINE
            except Exception as e:
                raise e
    elif platform.system() == "Darwin":
        try:
            client = docker.from_env()
            client.info()
            return DOCKER_ENGINE
        except Exception as e:
            raise e
    elif platform.system() == "Windows":
        try:
            client = docker.from_env()
            client.info()
            return DOCKER_ENGINE
        except Exception as e:
            raise e


def get_file(destination_dir, url, _format):
    """
    Get the files from a url or the
    :return: The filename of the file. Must be the filename
    :rtype: str
    :param _format:
    :type _format:  str
    :param url:
    :type url: str
    :param destination_dir: The destination directory
    :type destination_dir: Path
    """
    if validators.url(url):
        file_path, file_name = download_data_file(url, destination_dir, _format)
        return file_path.name
    elif Path(url).is_file():
        return Path(shutil.copy(str(Path(url)), str(destination_dir))).name


def build_input(inputs, destination_dir):
    """
    Download or search the file. Loop the inputs (metadata) of Model Configuration or Model Configuration Setup
    :return:
    :rtype:
    :param inputs: A dictionary following DataSpecificationFile
    :type inputs: dict
    :param destination_dir: The destination directory
    :type destination_dir: Path
    :return: The cmd_line related to the input -i1 file1 -i2 file2
    :param data_dir: The local directory where the files are
    :type data_dir: Path
    :rtype: str
    """
    line = ""
    for _input in inputs:
        print(_input)
        _input = convert_object_to_dict(_input)
        if not _input.keys() >= KEYS_REQUIRED_INPUT or _input['has_fixed_resource'] is None:
            raise ValueError(f'{_input["id"]} has not a fixedResource')
        else:
            url = _input["has_fixed_resource"][0]["value"][0]
            if "has_format" in _input:
                _format = _input["has_fixed_resource"][0]["value"][0]
            else:
                _format = None
            file_name = get_file(destination_dir, url, _format)
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
    component_dir = download_extract_zip(component_url, _dir)
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


def docker_pull(client, image):
    client = docker.APIClient()
    try:
        result_itr = client.pull(image, stream=True, decode=True)
    except docker.errors.APIError as ex:
        raise docker.errors.APIError

    for chunk in result_itr:
        try:
            if "progressDetail" in chunk:
                print("{}: Downloading {}".format(chunk['id'], chunk['progress']))
        except:
            pass


def run_docker(component_cmd, execution_dir, component_dir, setup_name, image, volumes):
    log_file_path = "{}/output.log".format(execution_dir)
    client = docker.from_env()
    docker_pull(client, image)
    res = client.containers.run(command=component_cmd,
                                image=image,
                                volumes=volumes,
                                working_dir='/tmp/mint',
                                detach=True,
                                stream=True,
                                remove=True
                                )
    with open(log_file_path, 'wb') as log_file:
        for chunk in res.logs(stream=True):
            print(chunk)
            log_file.write(chunk)


def run_singularity(singularity_cmd, execution_dir, component_dir, setup_name):
    log_file_path = "{}/output.log".format(execution_dir)
    with open(log_file_path, 'wb') as log_file:
        log.info(f'Execution {setup_name} running,  check the logs on {log_file_path}')
        proc = subprocess.Popen(singularity_cmd, stdout=log_file, stderr=log_file, cwd=component_dir)
        proc.wait()


def get_singularity_cmd(image, setup_cmd_line):
    try:
        setup_singularity_bin = get_singularity()
    except FileNotFoundError as e:
        raise e
    setup_singularity_line = "{} exec docker://{}".format(setup_singularity_bin, image)
    setup_cmd_line = "{} {}".format(setup_singularity_line, setup_cmd_line)
    return setup_cmd_line.split(' ')


def get_docker_cmd(image, setup_cmd_line, mint_volumes):
    volume_line = ""
    for volume in mint_volumes.keys():
        volume_line += "-v {}:{}".format(volume, mint_volumes[volume]["bind"])
    volume_line += " -w {}".format(mint_volumes[volume]["bind"])

    return "docker run -ti {} {} {}".format(volume_line, image, setup_cmd_line)
