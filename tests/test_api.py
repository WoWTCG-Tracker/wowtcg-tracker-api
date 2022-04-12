"""Unit tests for API functions"""
import unittest

from api import read_root


class TestRoot(unittest.TestCase):
    """
    Test the root of the API

    Root is set to return "Hello world!" string.
    """

    def test_root(self):
        """Test the root of the API"""
        self.assertEqual(read_root(), "Hello world!")


if __name__ == "__main__":
    unittest.main()
