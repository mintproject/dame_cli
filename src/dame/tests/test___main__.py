from unittest import TestCase

from click.testing import CliRunner

import dame
from dame.__main__ import version, setup_show, setup_list, model_configuration_list, model_configuration_show, configure

SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"
USERNAME = "mint@isi.edu"


class Test(TestCase):
    def test_configure(self):
        runner = CliRunner()
        result = runner.invoke(configure,
                      ["--server", "https://api.models.mint.isi.edu/v1.4.0", "--username", USERNAME, "--profile",
                       "testing"])
        assert result.exit_code == 0

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(version)
        assert result.exit_code == 0
        assert result.output == f"DAME: v{dame.__version__}\n"

    def test_setup_show(self):
        runner = CliRunner()
        result = runner.invoke(setup_show, "topoflow_cfg_simple_Shebelle")
        assert result.exit_code == 0

        runner = CliRunner()
        result = runner.invoke(setup_show, "not_found")
        assert result.exit_code == 1

    def test_setup_list(self):
        runner = CliRunner()
        result = runner.invoke(setup_list, ["--profile", "testing"])
        assert result.exit_code == 0

    def test_model_configuration_list(self):
        runner = CliRunner()
        result = runner.invoke(model_configuration_list, ["--profile", "testing"])
        assert result.exit_code == 0

    def test_model_configuration_show(self):
        runner = CliRunner()
        result = runner.invoke(model_configuration_show, ["pihm_flooding", "--profile", "testing"])
        assert result.exit_code == 0
        runner = CliRunner()
        result = runner.invoke(model_configuration_show, ["not_found", "--profile", "testing"])
        assert result.exit_code == 1

