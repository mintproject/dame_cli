from unittest import TestCase

from click.testing import CliRunner

from dame.__main__ import version, run
import dame

SETUP_FULL_INFO = "cycles-0.10.2-alpha-collection-oromia-single-point"


class Test(TestCase):
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(version)
        assert result.exit_code == 0
        assert result.output == f"DAME: v{dame.__version__}\n"


    # def test_run(self):
    #     runner = CliRunner()
    #     result = runner.invoke(run, SETUP_FULL_INFO)
    #     assert not result.exception


    # def test_run_partial(self):
    #     runner = CliRunner()
    #     result = runner.invoke(run, SETUP_FULL_INFO)
    #     assert not result.exception
