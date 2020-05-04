from unittest import TestCase

from dame.modelcatalogapi import get_setup
from dame.utils import obtain_id

SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"
SETUP_PARTIAL_INFO = "dsi_1.0_cfg"


class Test(TestCase):
    def test_get_setup(self):
        assert obtain_id(get_setup(SETUP_FULL_INFO).id) == SETUP_FULL_INFO
        assert obtain_id(get_setup(SETUP_PARTIAL_INFO).id) == SETUP_PARTIAL_INFO
