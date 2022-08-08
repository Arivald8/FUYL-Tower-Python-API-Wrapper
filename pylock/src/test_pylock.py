from re import S
from pylock import __version__
import requests
import unittest
from http.server import HTTPServer
from mock_lnc_server import handler
from multiprocessing import Process


class TestPylockCfg(unittest.TestCase):
    def __setup_server(self):
        with HTTPServer(('', 8000), handler) as server:
            server.serve_forever()

    def setUp(self) -> None:
        p = Process(target=self.__setup_server())
        p.start()
        p.join()
        return super().setUp()

    def test_pylock_version(self):
        self.assertEqual(__version__, "0.1.0")


    def test_mock_server_connection(self):
        r = requests.post("http://127.0.0.1:8000", "hello")
        self.assertEqual(r.status_code, 200)