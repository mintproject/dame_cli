import json
from pathlib import Path

import pytest

from dame.cli_methods import create_sample_resource
from dame.executor import is_file_or_url, get_file, build_input
from dame.modelcatalogapi import get_setup


def test_is_file_or_url(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("")
    assert is_file_or_url("http://google.com") == False
    assert is_file_or_url(str(d)) == False
    assert is_file_or_url(str(p)) == True


def test_get_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("")
    url = "https://upload.wikimedia.org/wikipedia/en/0/05/The_Midnight_Gospel_promotional_poster.jpg"
    assert get_file(d, url, "txt").exists()


def test_build_input(tmp_path):
    d = tmp_path / "sub"
    setup = get_setup("hand_v2_raster")
    with pytest.raises(ValueError, match=r".* has not a fixedResource"):
        build_input(setup.has_input, d)
