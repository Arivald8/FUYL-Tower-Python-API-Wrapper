import requests
from pylock.config import CFG

class BaseWrapper:
    def __init__(
        self,
        url: str = CFG["URL"], 
        client_id: str = CFG["CLIENT_ID"],
        client_secret: str = CFG["CLIENT_SECRET"],
        username: str = CFG["USERNAME"],
        password: str = CFG["PASSWORD"], 
        grant_type: str = CFG["GRANT_TYPE"],
        access_token: str = CFG["ACCESS_TOKEN"]

    ):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.access_token = access_token


    def get_jwt(self, only_access_token: bool) -> requests.Response.json:
        """
        Generates JWT token for API authentication. 

        Each API command must include a JWT authentication token. 

        Example of a response after Token command;

        {
            "access_token":"eyJ0eXAiOiJKV1QiLCJ...",
            "expires_in":86400,
            "token_type":"bearer",
            "scope":null,
            "refresh_token":"305837308432fe0086..."
        }

        """

        jwt = requests.post(
            f"{self.url}/token",
            data = {
                "grant_type": self.grant_type,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password
            },
            headers={'Accept-Encoding': None}
        ).json()
        return jwt['access_token'] if only_access_token else jwt


    def auth_header(self, jwt_access_token: str) -> dict:
        """
        Returns a dictionary containing the correct Authorization header. 
        This header must be present in all calls, except when fetching a JWT token.
        """
        return {"Authorization": f"Bearer {jwt_access_token}"}


    def door_access(self, pin: list, door_number: int, lock_status: int
    ) -> requests.Response:
        """
        Locks or unlocks the door specified.

        pin --> ["0", "1", "2", "3"]

        lock_status expects to receive an integer, either 0 to open a locker
        door or 1 to close it. 
        """
        return requests.put(
            url = f"{self.url}/door/{door_number}",
            headers = self.auth_header(self.access_token),
            data = {
                "code_digit1": pin[0],
                "code_digit2": pin[1],
                "code_digit3": pin[2],
                "code_digit4": pin[3],
                "locked": lock_status
            }
        ).json()

    
    def set_door_pin(
        self, door_number: int, pin: list) -> requests.Response.json:
        """
        pin parameter expects to receive an argument of -> ["0", "1", "2", "3"]
        """
        return requests.put(
            url = f"{self.url}/door/{door_number}",
            headers = self.auth_header(self.access_token),
            data = {
                "code_digit1": pin[0],
                "code_digit2": pin[1],
                "code_digit3": pin[2],
                "code_digit4": pin[3],
            }
        ).json()


    def get_door_status(
        self, status_type: str, door_number: int) -> requests.Response.json:
        """
        status_type can be either "door" or "tower"
        
        Example response after door status

        {
            "locker_id":1,
            "code_digit1":-1,
            "code_digit2":-1,
            "code_digit3":-1,
            "code_digit4":-1,
            "retry_attempts":4,
            "locked":1,
            "quarantined":0,
            "inspect_opened":0,
            "alarm":0
        }

        Example response after tower status

        [
            {
                "locker_id":0,
                "code_digit1": 1,
                "code_digit2": 1,
                "code_digit3": 1,
                "code_digit4": 1,
                "retry_attempts":3,
                "locked":1,
                "quarantined":0,
                "inspect_opened":0,
                "alarm":0
            },
            {
                ...
            }
        ]

        """

        return requests.put(
            url = f"{self.url}/status/{status_type}/{door_number}",
            headers = self.auth_header(self.access_token)
        ).json()


    def display_message(
        self, line: int, 
        startup_or_live: str, message: str) -> requests.Response.json:

        """
        Example of a response after Message live command;

        {"id":1,"key":"live_message_line0","value":"Live Message Line 1"}
        """

        return requests.put(
            url = f"{self.url}/message/{startup_or_live}/line/{line}",
            headers = self.auth_header(self.access_token),
            data = message
        ).json()


    def read_keypad(self, action_type: str, entry: str) -> requests.Response.json:

        """
        Either updates or views the current keypad buffer. 
        The keypad buffer will store all the keys pressed on the physical keypad until cleared.

        entry	
                    This will be used as the value of the keypad buffer. 
                    This parameter is only required when updating the buffer.

        action_type 	
                    This can be either update or view. 
                    Update will set everything 
                    in the keypad buffer to be 
                    equal to the parameter sent. 
                    View will return everything stored in the buffer.

        Keys are saved as integer values which represent keypad digits or control
        keys and separated with a space delimiter:

            Digits: 0..9 
            CANCEL control key: C
            OK (Enter) control key: E

        For example, entering the keypad sequence: 
        1234567890[CANCEL][OK] 
        would result in a response string of 
        “1 2 3 4 5 6 7 8 9 0 C E”

        Example of a response after keypad view command;

        {
            "id":1,
            "parameter":"api_keypad_entry",
            "entry":"| 0 1 2 3 4 5 6 7 8 9 C E"
        }
        """

        return requests.put(
            url = f"{self.url}/keypad/{action_type}",
            headers = self.auth_header(self.access_token),
            data = entry
        ).json()
