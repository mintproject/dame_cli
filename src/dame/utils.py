import pathlib
import requests
import os
import tempfile
from zipfile import ZipFile
import validators
import yaml
import platform

DOC_LINK = "https://dame-cli.readthedocs.io/en/latest/"
ignore_dirs = ["__MACOSX"]
SERVER = "https://dev.mint.isi.edu"


def find_singularity():
    if platform.system() == "Linux":
        SINGULARITY_CWD_LINE = "/usr/bin/singularity"
    elif platform.system() == "Darwin":
        SINGULARITY_CWD_LINE = "/usr/local/bin/singularity"

    if pathlib.Path(SINGULARITY_CWD_LINE).exists():
        return True
    return False


def convert_object_to_dict(o):
    if isinstance(o, object):
        return o.to_dict()
    return o


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
    headers = {'Cache-Control': 'no-cache'}
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


def download_data_file(url, _dir, format):
    headers = {'Cache-Control': 'no-cache'}
    r = requests.get(url, allow_redirects=True, headers=headers)
    filename = url.split('/')[-1]
    filepath = pathlib.Path(_dir / filename)
    if filepath.suffix == "" and format:
        filepath = filepath.with_suffix(validate_suffix(format))
    with requests.get(url, stream=True, headers=headers) as r:
        r.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    return filepath, filename


suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']


def humansize(nbytes):
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.
        i += 1
    f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
    return '%s %s' % (f, suffixes[i])
