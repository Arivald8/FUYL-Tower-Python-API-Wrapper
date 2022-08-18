from curses.ascii import isdigit
from random import random
from re import L
from pylock import __version__
import unittest
from pylock.base_wrapper import BaseWrapper
from pylock.pylocker import Pylock
from random import randint

class TestPylockCfg(unittest.TestCase):
    def setUp(self) -> None:
        self.base_wrapper = BaseWrapper(
            url="http://127.0.0.1:8000",
            client_id="test_id",
            client_secret="test_secret",
            username = "test_username",
            password = "test_password",
            grant_type = "password",
            access_token = "eyJ0eXAiOiJKV1QiLCJ..."
        )

        self.convenience_wrapper = Pylock()
        self.convenience_wrapper.url="http://127.0.0.1:8000"
        self.convenience_wrapper.client_id="test_id"
        self.convenience_wrapper.client_secret="test_secret"
        self.convenience_wrapper.username = "test_username"
        self.convenience_wrapper.password = "test_password"
        self.convenience_wrapper.grant_type = "password"
        self.convenience_wrapper.access_token = "eyJ0eXAiOiJKV1QiLCJ..."

        return super().setUp()

    def test_pylock_version(self):
        self.assertEqual(__version__, "0.1.0")


    def test_get_jwt_full_token(self):
        self.assertDictEqual(
            self.base_wrapper.get_jwt(False),
            {
                "access_token": "eyJ0eXAiOiJKV1QiLCJ...",
                "expires_in": "86400",
                "token_type": "bearer",
                "scope": "null",
                "refresh_token": "305837308432fe0086..."
            }
        )


    def test_get_jwt_access_only_token(self):
        self.assertEqual(
            self.base_wrapper.get_jwt(True),
            "eyJ0eXAiOiJKV1QiLCJ..."
        )


    def test_auth_header(self):
        self.assertDictEqual(
            self.base_wrapper.auth_header("eyJ0eXAiOiJKV1QiLCJ..."),
            {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJ..."}
        )


    def test_door_access(self):
        self.assertDictEqual(
            self.base_wrapper.door_access(pin=["0", "0", "0", "0"], door_number=0, lock_status=0),
            {
                "Locker_id": "0",
                "code_digit1": "0",
                "code_digit2": "0",
                "code_digit3": "0",
                "code_digit4": "0",
                "open_status": "0",
                "retry_atempts": "0",
                "locked": "0",
                "quarantined": "0",
                "Inspect_opened": "0",
                "alarm": "0"
            }
        )


    def test_set_door_pin(self):
        self.assertDictEqual(
            self.base_wrapper.set_door_pin(-1, ["0", "0", "0", "0"]),
            {
                "Locker_id": "0",
                "code_digit1": "0",
                "code_digit2": "0",
                "code_digit3": "0",
                "code_digit4": "0",
                "open_status": "0",
                "retry_atempts": "0",
                "locked": "0",
                "quarantined": "0",
                "Inspect_opened": "0",
                "alarm": "0"
            }
        )

    
    def test_get_door_status_specific_door(self):
        self.assertDictEqual(
            self.base_wrapper.get_door_status("door", -1),
            {
                "locker_id": "2",
                "code_digit1": "-1",
                "code_digit2": "-1",
                "code_digit3": "-1",
                "code_digit4": "-1",
                "retry_attempts": "4",
                "locked": "1",
                "quarantined": "0",
                "inspect_opened": "0",
                "alarm": "0"
            }
        )

    
    def test_get_door_status_full_tower(self):
        self.assertListEqual(
            self.base_wrapper.get_door_status("tower", ""),
            [
                {"locker_id":0,"code_digit1": 1,"code_digit2": 1,"code_digit3": 1,"code_digit4": 1,"retry_attempts":3,"locked":1,"quarantined":0,"inspect_opened":0,"alarm":0},

                {"locker_id":1,"code_digit1": 1,"code_digit2": 1,"code_digit3": 1,"code_digit4": 1,"retry_attempts":3,"locked":1,"quarantined":0,"inspect_opened":0,"alarm":0},
            ]
        )


    def test_display_message_top_line_startup(self):
        self.assertEqual(
            self.base_wrapper.display_message(0, "startup", "message"),
            {"id":1,"key":"live_message_line0","value":"Live Message Line 1"}
        )


    def test_display_message_bottom_line_startup(self):
        self.assertEqual(
            self.base_wrapper.display_message(1, "startup", "message"),
            {"id":1,"key":"live_message_line0","value":"Live Message Line 1"}
        )


    def test_display_message_top_line_live(self):
        self.assertEqual(
            self.base_wrapper.display_message(0, "live", "message"),
            {"id":1,"key":"live_message_line0","value":"Live Message Line 1"}
        )

    
    def test_display_message_bottom_line_live(self):
        self.assertEqual(
            self.base_wrapper.display_message(1, "live", "message"),
            {"id":1,"key":"live_message_line0","value":"Live Message Line 1"}
        )


    def test_read_keypad_default_buffer(self):
        self.assertDictEqual(
            self.base_wrapper.read_keypad(action_type="view", entry=""),
            {
                "id": 1,
                "parameter": "api_keypad_entry",
                "entry": "| 0 1 2 3 4 5 6 7 8 9 C E"
            }
        )

    
    def test_conv_wrapper_random_pins_one_locker(self):
        pin = self.convenience_wrapper.random_pins(False)

        self.assertEqual(len(pin), 4)

        for digit in pin:
            self.assertTrue(isdigit(digit))


    def test_conv_wrapper_random_pins_all_lockers(self):
        pins = self.convenience_wrapper.random_pins(True)
        dummy_pins = {locker: ["0", "0", "0", "0"] for locker in pins.keys()}

        self.assertEqual(len(pins), len(dummy_pins))

    
    def test_conv_wrapper_random_pins_single_locker(self):
        pin = self.convenience_wrapper.random_pins(False)
        dummy_pin = ["0", "0", "0", "0"]

        self.assertEqual(len(pin), len(dummy_pin))
        
        for _ in pin:
            self.assertEqual(
                type(_), str
            )


    def test_conv_wrapper_default_pins(self):
        self.assertTrue(
            self.convenience_wrapper.default_pins(["0", "0", "0", "0"])
        )
        

