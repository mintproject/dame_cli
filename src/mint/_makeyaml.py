import logging
import os
import click
import yaml
from mint import _schema, _utils
#from contextlib import contextmanager

logger = logging.getLogger()
schemaDefinitions = _schema.get_schema()["definitions"]
error_log = ""


def make_yaml(download_path=None):

    # sets path, this determines where the yaml will be made. Default is the current directory
    if download_path is None:
        path = os.getcwd()
    else:
        path = download_path
    path = os.path.join(path, "wings-component-outline.yaml")

    if os.path.isfile(path):
        click.echo("\"" + path + "\" already exists. Do you want to overwrite it? [y/n]")
        ans = input()
        if not(ans.lower() == 'y' or ans.lower() == "yes"):
            logger.info("Aborting YAML Generation")
            exit(0)

    # Checks if directory exists and finds file
    try:
        stream = open(path, 'w+')
    except FileNotFoundError:
        click.echo("\"" + os.path.join(os.getcwd(), download_path) + "\" doesnt exists. Do you want to make it? [y/n]")
        ans = input()
        if ans.lower() == 'y' or ans.lower() == "yes":
            os.mkdir(download_path)
            stream = open(path, 'w+')
        else:
            exit(0)

    yaml_outline = write_properties(_schema.get_schema()["properties"])

    yaml.dump(yaml_outline, stream, sort_keys=False)

def make_yaml_from_dict(download_path=None, dict=None):

    # sets path, this determines where the yaml will be made. Default is the current directory
    if download_path is None:
        path = os.getcwd()
    else:
        path = download_path
    path = os.path.join(path, "setup_name.yaml")

    if os.path.isfile(path):
        click.echo("\"" + path + "\" already exists. Do you want to overwrite it? [y/n]")
        ans = input()
        if not(ans.lower() == 'y' or ans.lower() == "yes"):
            logger.info("Aborting YAML Generation")
            exit(0)

    # Checks if directory exists and finds file
    try:
        stream = open(path, 'w+')
    except FileNotFoundError:
        click.echo("\"" + os.path.join(os.getcwd(), download_path) + "\" doesnt exists. Do you want to make it? [y/n]")
        ans = input()
        if ans.lower() == 'y' or ans.lower() == "yes":
            os.mkdir(download_path)
            stream = open(path, 'w+')
        else:
            exit(0)

    yaml.dump(dict, stream, sort_keys=False)

def write_properties(prop):
    dict = {}

    for i in prop:
        # print(i + ": " + str(type((prop[i])["type"])))
        curr = prop[i]

        try:
            # if there is only one type for the current property
            if type(curr["type"]) is str:
                if curr["type"] == "string":
                    if i == "schemaVersion":
                        dict[i] = _schema.get_schema_version()
                    else:
                        dict[i] = ""
                elif curr["type"] == "array":
                    ci = curr["items"]
                    if "$ref" in list(ci.keys()):
                        ref = ci["$ref"]
                        ref = ref.split('/')
                        ref = ref[-1]
                        dict[i] = [write_properties((schemaDefinitions[ref])["properties"])]
                    elif "type" in list(ci.keys()):
                        dict[i] = []
                    else:
                        logger.warning("unknown type fount in " + i)

                elif curr["type"] == "integer":
                    dict[i] = 0
                elif curr["type"] == "float":
                    dict[i] = 0.0
                elif curr["type"] == "boolean":
                    dict[i] = False
                elif curr["type"] == "object":
                    try:
                        dict[i] = write_properties(curr["properties"])
                    except KeyError as ke:
                        logger.info("In object: \"" + i + "\" couldn't find type: " + str(ke) + "making empty object")
                        dict[i] = {}
            # if there are multiple types for the given property. Favoring in order: objects, arrays, everything else
            elif type(curr["type"]) is list:
                if "object" in curr["type"]:
                    try:
                        dict[i] = write_properties(curr["properties"])
                    except KeyError as ke:
                        logger.info("In object: \"" + i + "\" couldn't find type " + str(ke) + " making empty object")
                        dict[i] = {}
                elif "array" in curr["type"]:
                    dict[i] = []
                else:
                    dict[i] = ""

        except KeyError as err:
            logger.warning("\"KeyError\" in \"" + i + "\" no \"" + str(err) + "\"")

    return dict


def _main():
    make_yaml()


if __name__ == "__main__":
    try:
        _main()
    except Exception as e:
        logger.exception(e)
