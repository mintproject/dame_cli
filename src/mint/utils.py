import pathlib
import requests
import os
import tempfile
from zipfile import ZipFile
import validators
import yaml
from mint.modelcatalogapi import get_setup

ignore_dirs = ["__MACOSX"]
SERVER = "https://dev.mint.isi.edu"

def check_is_none(item, key):
    return item[key] if key in item else ''

def download_setup(setup_id, output):
    filename = setup_id + ".yaml"
    path = pathlib.Path.cwd() / output / filename
    with open(path, mode='w+') as fid:
        setup_id = get_setup(setup_id)
        yaml.dump(setup_id, fid)
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


def download_data_file(url, _dir):
    headers={'Cache-Control': 'no-cache'}
    r = requests.get(url, allow_redirects=True, headers=headers)
    filename = url.split('/')[-1]
    filepath = os.path.join(_dir, filename)
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
