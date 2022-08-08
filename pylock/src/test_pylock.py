from pylock import __version__
import unittest
import requests
from pylock.base_wrapper import BaseWrapper

class TestPylockCfg(unittest.TestCase):

    def test_pylock_version(self):
        self.assertEqual(__version__, "0.1.0")


    def test_mock_server_connection(self):
        r = requests.post("http://127.0.0.1:9000", "hello")
        self.assertEqual(r.status_code, 200)


    def test_mock_server_json_data(self):
        base_wrapper = BaseWrapper(url="http://127.0.0.1:9000")
        print("*")
        print("*")
        print("DEBUUUUG")
        print(base_wrapper.get_jwt(False))
        print("DEBUUUUG")
        print("*")
        print("*")

