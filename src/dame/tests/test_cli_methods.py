from unittest import TestCase

from dame.cli_methods import verify_input_parameters, print_data_property_table, show_model_configuration_details, \
    convert_setup_file
from dame.modelcatalogapi import get_setup, list_setup, list_model_configuration, get_model_configuration

from click.testing import CliRunner

from dame.utils import obtain_id

SETUP_PARTIAL_INFO = "dsi_1.0_cfg"
SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"


class Test(TestCase):
    def test_verify_input_parameters(self):
        runner = CliRunner()
        partial_setup = get_setup(SETUP_FULL_INFO)
        assert verify_input_parameters(partial_setup) == partial_setup

    def test_print_data_property_table(self):
        for setup in list_setup():
            print_data_property_table(get_setup(obtain_id(setup.id)))
        for model_configuration in list_model_configuration():
            print_data_property_table(get_model_configuration(obtain_id(model_configuration.id)))

    def test_show_model_configuration_details(self):
        full = get_setup(SETUP_FULL_INFO)
        partial = get_setup(SETUP_PARTIAL_INFO)
        show_model_configuration_details(full)
        show_model_configuration_details(partial)
        for setup in list_setup():
            show_model_configuration_details(get_setup(obtain_id(setup.id)))
        for model_configuration in list_model_configuration():
            show_model_configuration_details(get_model_configuration(obtain_id(model_configuration.id)))
    #
    # def test_convert_setup_file(self):
    #     for setup in list_setup():
    #         convert_setup_file(setup)
