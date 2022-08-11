from pylock import __version__
import unittest
from pylock.base_wrapper import BaseWrapper

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
            self.base_wrapper.door_access(["0", "0", "0", "0"], 0, 0),
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
            self.base_wrapper.set_door_pin(1, ["0", "0", "0", "0"]),
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
            self.base_wrapper.get_door_status("door", 2),
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
                {
                    "locker_id": "3",
                    "code_digit1": "-1",
                    "code_digit2": "-1",
                    "code_digit3": "-1",
                    "code_digit4": "-1",
                    "retry_attempts": "4",
                    "locked": "1",
                    "quarantined": "0",
                    "inspect_opened": "0",
                    "alarm": "0"
                },
                {
                    "locker_id": "4",
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
            ]
        )


    def test_display_message_top_line_startup(self):
        self.assertDictEqual(
            self.base_wrapper.display_message(0, "startup", "message"),
            {"id":1,"key":"live_message_line0","value":"Live Message Line 1"}
        )

