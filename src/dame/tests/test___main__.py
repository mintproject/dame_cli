from unittest import TestCase

from click.testing import CliRunner

from dame.__main__ import version
import dame


class Test(TestCase):
    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(version)
        assert result.exit_code == 0
        assert result.output == f"DAME: v{dame.__version__}\n"