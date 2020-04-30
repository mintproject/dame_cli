from unittest import TestCase

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from dame.cli_methods import verify_input_parameters, print_data_property_table, show_model_configuration_details, print_table_list
from dame.modelcatalogapi import get_setup, list_setup, list_model_configuration, get_model_configuration

from click.testing import CliRunner

from dame.utils import obtain_id

SETUP_PARTIAL_INFO = "dsi_1.0_cfg"
SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"

setups = [get_setup(obtain_id(setup.id)) for setup in list_setup()]
model_configurations = [get_model_configuration(obtain_id(setup.id)) for setup in list_model_configuration()]


class Test(TestCase):
    def test_verify_input_parameters(self):
        runner = CliRunner()
        partial_setup = get_setup(SETUP_FULL_INFO)
        assert verify_input_parameters(partial_setup, False) == partial_setup

    def test_print_data_property_table(self):
        for setup in setups:
            print_data_property_table(setup)
        for model_configuration in model_configurations:
            print_data_property_table(model_configuration)

    def test_show_model_configuration_details(self):
        full = get_setup(SETUP_FULL_INFO)
        partial = get_setup(SETUP_PARTIAL_INFO)
        for setup in setups:
            try:
                show_model_configuration_details(setup)
            except AttributeError:
                pass

        for model_configuration in model_configurations:
            try:
                show_model_configuration_details(model_configuration)
            except AttributeError:
                pass

    def test_print_table_list(self):
        print_table_list(setups)
        print_table_list(model_configurations)

