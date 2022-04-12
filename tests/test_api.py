import unittest

from api import api_root

class TestRoot(unittest.TestCase):
    def test_root(self):
        self.assertEqual(api_root(), "Hello world!")

if __name__ == "__main__":
    unittest.main()
