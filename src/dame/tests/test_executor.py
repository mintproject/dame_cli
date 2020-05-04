from pathlib import Path

from dame.executor import is_file_or_url


def test_is_file_or_url(tmp_path):
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("")
    assert is_file_or_url("http://google.com") == False
    assert is_file_or_url(str(d)) == False
    assert is_file_or_url(str(p)) == True
