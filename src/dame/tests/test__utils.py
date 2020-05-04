from unittest import TestCase

from dame._utils import init_logger, get_latest_version
import dame


class Test(TestCase):
    def test_init_logger(self):
        init_logger()

    def test_get_latest_version(self):
        assert get_latest_version() == f"{dame.__version__}"
