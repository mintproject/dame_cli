import itertools
import subprocess
import uuid
from pathlib import Path

from yaml import load, Loader

from core._utils import download_data_file, download_extract_zip
from mint._utils import log


def build_input(inputs, _dir):
    line = ""
    files_inputs = []
    for _input in inputs:
        if not "hasFixedResource" in _input:
            print("fail:")
            exit(1)
        url = _input["hasFixedResource"][0]["value"][0]
        file_path, file_name = download_data_file(url, _dir)
        position = _input["position"][0]
        line += " -i{} {}".format(position, file_name)
    return line


def build_output(outputs):
    line =  ""
    for _output in outputs:
        if not "label" in _output:
            print("fail:")
            exit(1)
        label = _output["label"][0]
        extension = _output["hasFormat"][0]
        position = _output["position"][0]
        line += " -o{} {}.{}".format(position, label, extension)
    return line

def build_parameter(parameters):
    line =  ""
    for _parameter in parameters:
        if not "label" in _parameter:
            print("fail:")
            exit(1)
        if "hasFixedValue" in _parameter:
            value = _parameter["hasFixedValue"][0]
        else:
            value = _parameter["hasDefaultValue"][0]
        position = _parameter["position"][0]
        line += " -p{} {}".format(position, value)
    return line


def build_command_line(resource, _dir):
    setup_name = resource[0]["id"].split('/')[-1]
    inputs = resource[0]["hasInput"]
    parameters = resource[0]["hasParameter"] if "hasParameter" in resource[0] else None
    outputs = resource[0]["hasOutput"]
    component_url = resource[0]["hasComponentLocation"][0]
    has_software_image = resource[0]["hasSoftwareImage"][0]['label'][0]
    line = "singularity exec docker://{} ./run ".format(has_software_image)

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
    return line

def read_setup(setup_paths):
    data = []
    _dir = Path("executions/")
    _dir.mkdir(parents=True, exist_ok=True)

    for setup in setup_paths:
        setup_dict = load((setup).open(), Loader=Loader)
        setup_name = setup_dict[0]["id"].split('/')[-1]
        execution_dir = "{}/{}_{}".format(_dir, setup_name, uuid.uuid1())
        execution_dir_path = Path(execution_dir)
        execution_dir_path.mkdir(parents=True, exist_ok=True)

        setup_cmd_line = build_command_line(setup_dict, execution_dir_path)
        log_file_path = "{}/output.log".format(execution_dir)

        data.append({
            "cmd": setup_cmd_line,
            "log": open(log_file_path,'wb'),
            "directory": execution_dir_path,
            "name": setup_name
        })

        print("Execution {}, check the logs on {}".format(setup_name, log_file_path))

    procs_list = [subprocess.Popen(item["cmd"], stdout=item["log"], stderr=item["log"], cwd=item["directory"]) for item in data]

    for proc in procs_list:
        proc.wait()

    status = []
    for proc, name in zip(procs_list, data):
        status.append({
            "exitcode": proc.returncode,
            "name": data["name"]
        })

    return status
