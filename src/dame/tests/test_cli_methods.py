import io

from click.testing import CliRunner

from dame.__main__ import credentials
from dame.cli_methods import verify_input_parameters, print_data_property_table, show_model_configuration_details, \
    print_table_list, edit_parameters
from dame.modelcatalogapi import get_setup, get_model_configuration
from dame.utils import obtain_id

SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"
USERNAME = "mint@isi.edu"
testing = "testing"
SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"
SETUP_PARTIAL_INFO = "dsi_1.0_cfg"
CONFIG_PARTIAL_INFO = "hand_v2"


def test_configure():
    runner = CliRunner()
    result = runner.invoke(credentials,
                           ["--server", "https://api.models.mint.isi.edu/v1.4.0", "--username", USERNAME, "--profile",
                            testing])
    assert result.exit_code == 0


def test_verify_input_parameters():
    runner = CliRunner()
    partial_setup = get_setup(SETUP_FULL_INFO, profile=testing)
    assert verify_input_parameters(partial_setup, False, None) == partial_setup


def test_print_data_property_table():
    setups = [get_setup(obtain_id(SETUP_PARTIAL_INFO), profile=testing), get_setup(SETUP_FULL_INFO, profile=testing)]
    model_configurations = [get_model_configuration(CONFIG_PARTIAL_INFO, profile=testing)]

    for setup in setups:
        print_data_property_table(setup)
    for model_configuration in model_configurations:
        print_data_property_table(model_configuration)


def test_show_model_configuration_details():
    model_configurations = [get_model_configuration(CONFIG_PARTIAL_INFO, profile=testing)]
    setups = [get_setup(obtain_id(SETUP_PARTIAL_INFO), profile=testing), get_setup(SETUP_FULL_INFO, profile=testing)]

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


def test_print_table_list():
    model_configurations = [get_model_configuration(CONFIG_PARTIAL_INFO, profile=testing)]
    setups = [get_setup(obtain_id(SETUP_PARTIAL_INFO), profile=testing), get_setup(SETUP_FULL_INFO, profile=testing)]

    print_table_list(setups)
    print_table_list(model_configurations)


def test_edit_parameters(monkeypatch):
    runner = CliRunner()
    setup = get_setup(SETUP_FULL_INFO, profile=testing)
    monkeypatch.setattr('sys.stdin', io.StringIO("1\n2\n3\n\n\n\n\n\n\n"))
    new_setup = edit_parameters(setup, True)
    assert new_setup.has_parameter[0].has_default_value == ['1']
