import pytest
from dame.executor import get_file, build_input, get_singularity
from dame.modelcatalogapi import get_setup

testing = "testing"


def test_get_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("")
    url = "https://upload.wikimedia.org/wikipedia/en/0/05/The_Midnight_Gospel_promotional_poster.jpg"
    assert get_file(d, url, "txt")


def test_build_input(tmp_path):
    d = tmp_path / "sub"
    setup = get_setup("hand_v2_raster", profile=testing)
    with pytest.raises(ValueError, match=r".* has not a fixedResource"):
        build_input(setup.has_input, d)


def test_get_singularity():
    with pytest.raises(FileNotFoundError) as e_info:
        get_singularity()
