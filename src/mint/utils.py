import pathlib
import requests
import os
import tempfile
from zipfile import ZipFile
import validators
import yaml
from mint.modelcatalogapi import get_setup, datasetspecifications_id_get

ignore_dirs = ["__MACOSX"]
SERVER = "https://dev.mint.isi.edu"

def check_is_none(item, key):
     item[key] if key in item else ''


def create_yaml_from_resource(resource, name, output):
    filename = name + ".yaml"
    path = pathlib.Path.cwd() / output / filename
    with open(path, mode='w+') as fid:
        yaml.dump(resource, fid)
    return path


def obtain_id(url):
    if validators.url(url):
        return url.split('/')[-1]
    return url

def download_extract_zip(url, _dir, setup_name):
    temp = tempfile.NamedTemporaryFile(prefix="component_")
    content = download_file(url)
    temp.write(content)
    with ZipFile(temp.name, 'r') as zip:
        zip.extractall(_dir)
    directories = os.listdir(_dir)
    if isinstance(directories, list):
        try:
            for ignore_dir in ignore_dirs:
                directories.remove(ignore_dir)
        except:
            pass

    if len(directories) == 1:
        return os.path.join(_dir, directories[0])
    else:
        raise ValueError("The zipfile must has one directory.")


def download_file(url):
    headers={'Cache-Control': 'no-cache'}
    r = requests.get(url, allow_redirects=True, headers=headers)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        raise requests.exceptions.HTTPError(r)
    except requests.exceptions.RequestException:
        raise requests.exceptions.RequestException(r)
    return r.content

def validate_suffix(suffix):
    return suffix if suffix.startswith('.') else ".{}".format(suffix)

def download_data_file(url, _dir, data_specification_id=None):
    headers={'Cache-Control': 'no-cache'}
    r = requests.get(url, allow_redirects=True, headers=headers)
    filename = url.split('/')[-1]
    filepath = pathlib.Path(_dir / filename)
    if filepath.suffix == "" and data_specification_id:
        file_extension = datasetspecifications_id_get(obtain_id(data_specification_id)).has_format[0]
        if file_extension:
            filepath = filepath.with_suffix(validate_suffix(file_extension))
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    return filepath, filename


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes)-1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
