from pathlib import Path

from dame.local_file_manager import find_file_directory


def test_create_file(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("")
    assert Path(find_file_directory(d, "txt")) == p
    assert Path(find_file_directory(d, ".txt")) == p
