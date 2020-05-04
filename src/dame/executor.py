import platform
import shutil
import subprocess
import uuid
from pathlib import Path

from yaml import load, Loader

from dame._utils import log
from dame.utils import download_data_file, download_extract_zip, obtain_id, convert_object_to_dict

KEYS_REQUIRED_PARAMETER = {"has_default_value", "position"}
KEYS_REQUIRED_OUTPUT = {"label", "has_format", "position"}
KEYS_REQUIRED_INPUT = {"has_fixed_resource"}

if platform.system() == "Linux":
    SINGULARITY_CWD_LINE = "/usr/bin/singularity exec docker://{} ./run"
elif platform.system() == "Darwin":
    SINGULARITY_CWD_LINE = "/usr/local/bin/singularity exec docker://{} ./run"

EXECUTION_DIRECTORY = "executions"


def is_file_or_url(uri: str) -> bool:
    return Path(uri).is_file()


def get_file(destination_dir, url, _format):
    """
    Get the files from a url or the
    :param _format:
    :type _format:
    :param url:
    :type url:
    :param destination_dir: The destination directory
    :type destination_dir: Path
    """
    if Path(url).is_file():
        file_path = shutil.copy(str(Path(url)), str(destination_dir))
    else:
        file_path, file_name = download_data_file(url, destination_dir, _format)
    return file_path


def build_input(inputs, destination_dir, data_dir):
    """
    Download or search the file. Loop the inputs (metadata) of Model Configuration or Model Configuration Setup
    :param data_dir:
    :type data_dir:
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
        _input = convert_object_to_dict(_input)
        if not _input.keys() >= KEYS_REQUIRED_INPUT:
            raise ValueError(f'{_input["id"]} has not a fixedResource')

        url = _input["has_fixed_resource"][0]["value"][0]
        if "has_format" in _input:
            _format = _input["has_fixed_resource"][0]["value"][0]
        else:
            _format = None
        file_name = get_file(destination_dir, url,  _format)
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


def build_command_line(resource, _dir, data_dir):
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
        line = SINGULARITY_CWD_LINE.format(has_software_image)
    else:
        raise ValueError("Software is not available")
    component_dir = download_extract_zip(component_url, _dir, setup_name)
    path = Path(component_dir)
    src_path = path / "src"
    if inputs:
        l = build_input(inputs, src_path, data_dir)
        line += " {}".format(l)
    if outputs:
        l = build_output(outputs)
        line += " {}".format(l)
    if parameters is not None:
        l = build_parameter(parameters)
        line += " {}".format(l)
    return line, src_path


def prepare_execution(setup_path, data_dir):
    _dir = Path("%s/" % EXECUTION_DIRECTORY)
    _dir.mkdir(parents=True, exist_ok=True)
    setup_dict = load(setup_path.open(), Loader=Loader)
    setup_name = obtain_id(setup_dict.id)
    execution_dir = "{}/{}_{}".format(_dir, setup_name, uuid.uuid1())
    execution_dir_path = Path(execution_dir)
    execution_dir_path.mkdir(parents=True, exist_ok=True)
    try:
        setup_cmd_line, cwd_path = build_command_line(setup_dict, execution_dir_path, data_dir)
    except Exception as e:
        raise e
    return cwd_path, execution_dir, setup_cmd_line, setup_name


def run_execution(cwd_path, execution_dir, setup_cmd_line, setup_name):
    log_file_path = "{}/output.log".format(execution_dir)
    item = {
        "cmd": setup_cmd_line.split(' '),
        "log": open(log_file_path, 'wb'),
        "directory": cwd_path,
        "name": setup_name
    }
    log.info(f'Execution {setup_name} running,  check the logs on {log_file_path}')
    _ = subprocess.Popen(["chmod", "+x", "run"], stdout=item["log"], stderr=item["log"], cwd=item["directory"])
    proc = subprocess.Popen(item["cmd"], stdout=item["log"], stderr=item["log"], cwd=item["directory"])
    proc.wait()
    status = {
        "exitcode": proc.returncode,
        "name": item["name"]
    }
    return status
