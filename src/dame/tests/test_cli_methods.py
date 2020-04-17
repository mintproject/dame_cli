from unittest import TestCase

from dame.cli_methods import verify_input_parameters, print_data_property_table
from dame.modelcatalogapi import get_setup

from click.testing import CliRunner

SETUP_PARTIAL_INFO = "dsi_1.0_cfg"
SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"


class Test(TestCase):
    def test_verify_input_parameters(self):
        runner = CliRunner()
        partial_setup = get_setup(SETUP_FULL_INFO)
        assert verify_input_parameters(partial_setup) == partial_setup


    def test_print_data_property_table(self):
        full = get_setup(SETUP_FULL_INFO)
        partial = get_setup(SETUP_PARTIAL_INFO)
        print_data_property_table(full)
        print_data_property_table(partial)

