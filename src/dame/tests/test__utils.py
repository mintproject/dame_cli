from dame._utils import init_logger, get_latest_version


def test_init_logger():
    init_logger()


def test_get_latest_version():
    assert get_latest_version()
