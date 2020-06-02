import shutil
import uuid
from pathlib import Path

import click
import docker
import yaml

from dame.cli_methods import print_table_list_data

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from dame.executor import EXECUTION_DIRECTORY, docker_pull, get_docker_cmd

TRANSFORMATION_DIR = "transformations"


def list_data_transformation():
    p = Path(__file__).parent / TRANSFORMATION_DIR
    items = []
    for i in list(p.glob('*.yml')):
        spec = yaml.load(i.open(), Loader=Loader)
        items.append({"id": i.stem, "description": "{}".format(spec["adapters"]["tf_climate"]["comment"])})
    print_table_list_data(items)

def show_data_transformation(name):
    config_yaml_path = obtain_data_transformation_file(name)
    spec = yaml.load(config_yaml_path.open(), Loader=Loader)
    for key, adapter in spec["adapters"].items():
        for key, input in adapter["inputs"].items():
            if not ("_dir" in key or "_file" in key):
                print("{}: {}".format(key, input))


def run_data_transformation(name, data):
    config_yaml_path = obtain_data_transformation_file(name)
    run_data_transformation_docker(name, config_yaml_path, data)


def obtain_data_transformation_file(name):
    p = Path(__file__).parent / TRANSFORMATION_DIR
    file_name = "{}.yml".format(name)
    config_yaml_path = p / file_name
    return config_yaml_path


def run_data_transformation_docker(name: str, config_path: Path, input_dir: Path):
    image = "mintproject/mint_dt"
    _dir = Path("%s/" % EXECUTION_DIRECTORY)
    execution_dir = "{}/{}_{}".format(_dir, name, uuid.uuid1())
    execution_dir_path = Path(execution_dir)
    tmp_dir = execution_dir_path / "tmp"
    tmp_dir.mkdir(exist_ok=True, parents=True)
    shutil.copyfile(config_path, tmp_dir / config_path.name)
    shutil.copytree(input_dir, tmp_dir / "inputs")
    output_dir = tmp_dir / "outputs"
    mint_volumes = {str(tmp_dir.absolute()): {'bind': '/tmp/', 'mode': 'rw'}}
    client = docker.from_env()
    docker_pull(client, image)
    res = client.containers.run(command="/tmp/{}".format(config_path.name),
                                image=image,
                                volumes=mint_volumes,
                                working_dir='/tmp/',
                                detach=True,
                                stream=True,
                                remove=True,
                                )
    click.echo("Running transformation")
    for chunk in res.logs(stream=True):
        print(chunk)
    click.secho("The outputs are available: {}".format(output_dir), fg="green")