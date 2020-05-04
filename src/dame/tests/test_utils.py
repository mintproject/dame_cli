from unittest import TestCase

from dame.utils import obtain_id, download_extract_zip


class Test(TestCase):
    def test_obtain_id(self):
        url = "https://w3id.org/okn/i/mint/cycles-0.10.2-alpha-collection-oromia-single-point"
        assert obtain_id(url) == "cycles-0.10.2-alpha-collection-oromia-single-point"


def test_download_extract_zip(tmp_path):
    d = tmp_path / "sub"
    zip_file = "https://github.com/mintproject/HAND-TauDEM/raw/v2.1.0/hand_v2_mint_component.zip"
    download_extract_zip(zip_file, d)
