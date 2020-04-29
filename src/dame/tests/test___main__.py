from unittest import TestCase

from click.testing import CliRunner

from dame.__main__ import version, setup_show, setup_list, model_configuration_list, model_configuration_show
import dame

SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"


class Test(TestCase):
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(version)
        assert result.exit_code == 0
        assert result.output == f"DAME: v{dame.__version__}\n"

    def test_setup_show(self):
        runner = CliRunner()
        result = runner.invoke(setup_show, "topoflow_cfg_simple_Shebelle")
        assert result.exit_code == 0

    def test_setup_list(self):
        runner = CliRunner()
        result = runner.invoke(setup_list)
        assert result.exit_code == 0

    def test_model_configuration_list(self):
        runner = CliRunner()
        result = runner.invoke(model_configuration_list)
        assert result.exit_code == 0

    def test_model_configuration_show(self):
        runner = CliRunner()
        result = runner.invoke(model_configuration_show, "pihm_flooding")
        assert result.exit_code == 0