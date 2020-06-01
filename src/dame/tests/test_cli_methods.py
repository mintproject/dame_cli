from unittest import TestCase

from click.testing import CliRunner

# noinspection PyUnresolvedReferences,PyUnresolvedReferences
from dame.cli_methods import verify_input_parameters, print_data_property_table, show_model_configuration_details, \
    print_table_list
from dame.modelcatalogapi import get_setup, list_setup, list_model_configuration, get_model_configuration
from dame.utils import obtain_id

SETUP_PARTIAL_INFO = "dsi_1.0_cfg"
CONFIG_PARTIAL_INFO = "hand_v2"
SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"
testing = "testing"

setups = [get_setup(obtain_id(SETUP_PARTIAL_INFO), profile=testing), get_setup(SETUP_FULL_INFO, profile=testing)]
model_configurations = [get_model_configuration(CONFIG_PARTIAL_INFO, profile=testing)]


class Test(TestCase):
    def test_verify_input_parameters(self):
        runner = CliRunner()
        partial_setup = get_setup(SETUP_FULL_INFO, profile=testing)
        assert verify_input_parameters(partial_setup, False, None) == partial_setup

    def test_print_data_property_table(self):
        for setup in setups:
            print_data_property_table(setup)
        for model_configuration in model_configurations:
            print_data_property_table(model_configuration)

    def test_show_model_configuration_details(self):
        full = get_setup(SETUP_FULL_INFO, profile=testing)
        partial = get_setup(SETUP_PARTIAL_INFO, profile=testing)
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

    # def test_verify_input_parameters(self):
    #     runner = CliRunner()
    #
    #     result = runner.invoke(verify_input_parameters(get_setup(SETUP_PARTIAL_INFO), True), "http://google.com")
    #     assert result.exit_code == 0
    #     self.fail()
