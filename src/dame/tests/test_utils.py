from unittest import TestCase

from dame.utils import obtain_id


class Test(TestCase):
    def test_obtain_id(self):
        url = "https://w3id.org/okn/i/mint/cycles-0.10.2-alpha-collection-oromia-single-point"
        assert obtain_id(url) == "cycles-0.10.2-alpha-collection-oromia-single-point"
