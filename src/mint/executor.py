import subprocess
import uuid
from pathlib import Path

from yaml import load, Loader

from mint.utils import download_data_file, download_extract_zip, obtain_id
from mint._utils import log

KEYS_REQUIRED_PARAMETER = {"hasDefaultValue", "position"}
KEYS_REQUIRED_OUTPUT = {"label", "hasFormat", "position"}
KEYS_REQUIRED_INPUT = {"hasFixedResource"}

SINGULARITY_CWD_LINE = "/usr/bin/singularity exec docker://{} ./run"

EXECUTION_DIRECTORY = "executions"

def build_input(inputs, _dir):
    line = ""
    files_inputs = []
    for _input in inputs:
        if not _input.keys() >= KEYS_REQUIRED_INPUT:
            raise ValueError(f'{_input["id"]} has not a fixedResource')
        url = _input["hasFixedResource"][0]["value"][0]
        file_path, file_name = download_data_file(url, _dir)
        position = _input["position"][0]
        line += " -i{} {}".format(position, file_name)
    return line


def build_output(outputs):
    line = ""
    for _output in outputs:
        if not _output.keys() >= KEYS_REQUIRED_OUTPUT:
            raise ValueError(f'{_output["id"]}  has not the required information')
        label = _output["label"][0]
        extension = _output["hasFormat"][0]
        position = _output["position"][0]
        line += " -o{} {}.{}".format(position, label, extension)
    return line


def build_parameter(parameters):
    line = ""
    for _parameter in parameters:
        if not _parameter.keys() >= KEYS_REQUIRED_PARAMETER:
            raise ValueError(f'{_parameter["id"]} has not the required information ')
        if "hasFixedValue" in _parameter:
            value = _parameter["hasFixedValue"][0]
        else:
            value = _parameter["hasDefaultValue"][0]
        position = _parameter["position"][0]
        line += " -p{} {}".format(position, value)
    return line


def build_command_line(resource, _dir):
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
        has_software_image = software_image[0]['label'][0]
        print("Using docker image {}".format(has_software_image))
        line = SINGULARITY_CWD_LINE.format(has_software_image)
    else:
        exit(1)
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
    print(line)
    return line, src_path


def execute_setup(setup_paths):
    data = []
    _dir = Path("%s/" % EXECUTION_DIRECTORY)
    _dir.mkdir(parents=True, exist_ok=True)

    for setup in setup_paths:
        setup_dict = load((setup).open(), Loader=Loader)
        setup_name = obtain_id(setup_dict.id)
        execution_dir = "{}/{}_{}".format(_dir, setup_name, uuid.uuid1())
        execution_dir_path = Path(execution_dir)
        execution_dir_path.mkdir(parents=True, exist_ok=True)
        try:
            setup_cmd_line, cwd_path = build_command_line(setup_dict, execution_dir_path)
        except Exception as e:
            raise e
        log_file_path = "{}/output.log".format(execution_dir)

        data.append({
            "cmd": setup_cmd_line.split(' '),
            "log": open(log_file_path, 'wb'),
            "directory": cwd_path,
            "name": setup_name
        })
        log.info(f'Execution {setup_name} running,  check the logs on {log_file_path}')

    _ = [subprocess.Popen(["chmod", "+x", "run"], stdout=item["log"], stderr=item["log"], cwd=item["directory"]) for item
        in data]
    procs_list = [subprocess.Popen(item["cmd"], stdout=item["log"], stderr=item["log"], cwd=item["directory"]) for item
                  in data]

    for proc in procs_list:
        proc.wait()

    status = []
    for proc, item in zip(procs_list, data):
        status.append({
            "exitcode": proc.returncode,
            "name": item["name"]
        })

    return status
