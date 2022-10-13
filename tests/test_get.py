"""
Database fill script for wowtcg-tracker-api

Script is used to fill database with all cards and extensions details
"""

import unittest

from fastapi.testclient import TestClient
from api import app

server = TestClient(app)


class TestApiGets(unittest.TestCase):

  def test_root(self):
    response = server.get("/")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json(), "Hello world!")


if __name__ == "__main__":
  unittest.main()
