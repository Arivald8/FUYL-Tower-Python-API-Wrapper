# **Pylock**
## **FUYL Lock&Charge Tower Python API Wrapper**
### Applicable for firmware releases v1.12 and later

***

## **Developing your applications with Pylock**

Pre-requisite configuration:

    1. Enable External API Control mode.
    2. Receive client ID and secret.

Both pre-requisite configuration actions can be 
performed in the FUYL Tower Management Portal. 

The portal can be accessed via http and https on ports 
9898 and/or 9899.

The state of the configuration will be stored in non-volatile
storage and so it will be retained in case of a tower power cycle.

Further information regarding the FUYL Tower is available online at:
* LocknCharge - https://www.lockncharge.com/support/fuyl-tower/
* PC Locs - https://www.pclocs.com.au/products/fuyl-tower/

***

**DISCLAIMER:**

**PC LOCS AND LOCKNCHARGE IS NOT RESPONSIBLE FOR THE PYLOCK WRAPPER. THE WRAPPER HAS BEEN DEVELOPED AS AN OPEN SOURCE SOLUTION FOR PYTHON ORIENTED DEVELOPMENT PROJECTS.**

**THE DEVELOPER OF THE WRAPPER IS IN NOT AFFILIATED WITH THE ABOVE MENTIONED IN ANY CAPACITY.**

***

## **Getting started**


###
Create an instance of Pylock and you are ready to go:
```
pylock = Pylock()
```

For example, opening all of the lockers is as simple as:
```
pylock.all_door_access(locked=False)
```

#
### **Notes on config.py**
To make the devlopment process easier, you can specify various 
configuration constants in `config.py`.  

Alternatively, you can set them after instantiation.

The following constants must be defined:
* URL
* CLIENT_ID
* CLIENT_SECRET
* USERNAME
* PASSWORD
* GRANT_TYPE
* ACCESS_TOKEN

All information, except for `GRANT_TYPE` and `ACCESS_TOKEN`
can be found within the FUYL Tower Management Portal. 

Unless otherwise specified, `GRANT_TYPE` should be set to "password". 

`ACCESS_TOKEN` must be a string of the access_token only, 
not the full JWT containing expiry and a refresh_token.

You can also specify each constant directly on an instance of Pylock:

```
from Pylock import Pylock

pylock = Pylock()

pylock.url = "localhost:9899/"
pylock.username = "admin"
...
```
***

### **Notes on responsiveness**
A latency of no more than 1 second is anticipated from the issue of an API command to the opening of a locker door. Note, the user must physically push a locker door closed before the door can be locked.

The client developer must ensure that their application allows commands to complete before issuing the next command.

Locker status should be periodically polled after the issuing of a command to ensure the command has been performed.
#
### **Available endpoints**
The FUYL Lock&Charge Tower provides 5 API endpoints:
1. Obtain a JWT Token
2. Lock/Unlock Door
3. Get Door or Tower status
4. Display Message
5. Read Keypad

The `BaseWrapper` class provides an abstraction layer for the five API calls available. 

Pylock includes some convenience methods both in `BaseWrapper` and in `Pylock`. 

The convenience methods provide abstracted logic for common usage calls to the API. 

For example, randomizing pins for each locker and automatically setting them at the Tower.

#

## **Wrapper methods**

The following methods are provided by Pylock for you application development:

* Generate JWT token for API authentication
* Return an Authorization header (Must be present in all calls to the API).
* Lock or unlock a specific locker door.
* Set a new pin for one of the locker doors.
* Retrieve door status.
* Display a message.
* Read or update keypad buffer.
* Generate a pseudo-random 4 digit pin for a single locker or for all lockers at once.
* Set a default pin for all locker doors.
* Lock or unlock all tower doors.

#


## **Classes and methods**

Below you can find a more detailed explanation of available methods.

### **`class BaseWrapper`**
Provides an abstraction layer of the API calls.

Methods:

Return type specified as JSON == `requests.Response.json`

* `get_jwt -> JSON:`

* `auth_header -> dict`

* `door_access -> JSON`

* `set_door_pin -> JSON`

* `get_door_status -> JSON`

* `display_message -> JSON`

* `read_keypad -> JSON`

#

### `get_jwt(only_access_token: bool) -> JSON`

Returns a JWT token for API authentication. 

Each API call must include a JWT authentication token. 

If `only_access_token` is set to True, the method returns only the "access_token" itself:
#

```
"eyJ0eXAiOiJKV1QiLCJ..."
```

 When set to False, the method returns full JWT token, including a refresh_token:



#


```
{
    "access_token":"eyJ0eXAiOiJKV1QiLCJ...",
    "expires_in":86400,
    "token_type":"bearer",
    "scope":null,
    "refresh_token":"305837308432fe0086..."
}
```
#

### `auth_header(jwt_access_token: str) -> dict`
A convenience method, returns a dictionary containing the correct Authorization header.

This header must be present in all calls, except when fetching a JWT token:

```{"Authorization": f"Bearer {jwt_access_token}"}```

#

### `door_access(pin: list, door_number: int, lock_status: int) -> JSON`

Locks or unlocks the door specified.

Expected `pin` value is a list of four strings `--> ["0", "1", "2", "3"]`

Expected `lock_status` value is an integer, either `0` (Opens a locker) or `1` (Closes a locker)

Notes: 

* Door numbers use a zero-based index. Door number 1 is represented with 0, door number 2 = 1, 3 = 2 ...


Example response:

```
{
    "locker_id": 0,
    "code_digit1": -1,
    ...
    "code_digit4": -1,
    "open_status": 0,
    "retry_attempts": 0,
    "locked": 0,
    "quarantined": 0,
    "inspect_opened": 0,
    "alarm": 0
}
```
If a Door is jammed closed but commanded to open, an attempt will be
made to release the lock at increasing time intervals (to limit lock
heating and damage) until a time limit (of approx. 40 seconds) expires,
at which point the alarm condition will be asserted and no further
unlock attempts are made.

#

### `set_door_pin(self, door_number: int, pin: list) -> JSON`
Self explanatory method, sets a specified pin for a given door number.

`pin` parameter expects to receive an argument of -> `["0", "1", "2", "3"]`

#

### `get_door_status(self, status_type: str, door_number: int) -> JSON`
Provides information about the status of an individual locker door, or the entire tower. 

`status_type`:	Can be set to a string of "door" or "tower". This then returns the status of a specified locker or the entire tower. 




`door_number`: Locker number, in range between 0 and 14. 


Example of a response after "door"
```
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
```
Example of a response after "tower"
```
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
        "locker_id":1,
        "code_digit1": 1,
        "code_digit2": 1,
        "code_digit3": 1,
        "code_digit4": 1,
        "retry_attempts":4,
        "locked":1,
        "quarantined":0,
        "inspect_opened":0,
        "alarm":0
    },
    {
        "locker_id":2,
        "code_digit1": 1,
        "code_digit2": 1,
        "code_digit3": 1,
        "code_digit4": 1,
        "retry_attempts":1,
        "locked":1,
        "quarantined":0,
        "inspect_opened":0,
        "alarm":0
    },
    {
        "locker_id":3,
        "code_digit1": 1,
        "code_digit2": 1,
        "code_digit3": 1,
        "code_digit4": 1,
        "retry_attempts":0,
        "locked":1,
        "quarantined":0,
        "inspect_opened":0,
        "alarm":0
    }
]
```

#

### `display_message(self, line: int, startup_of_live: str, message: str) -> JSON`

Live message display on the Tower unit.

`startup_or_live`: A string of "startup" or "live". If set to startup, the tower will display `message` after booting. If set to live, the message gets updated immediately.



`line`: The display allows for 2 lines of 20 characters each. If set to 0, the 20 character `message` will be displayed on the upper line of the display. Setting this to 1, places a `message` on the bottom. 

`message` :A 20 character string.

Notes: 	

* The FUYL Tower display is a 2-line by 20-character LCD so only line 1 and line 2 will be respected. 

* Any messages longer than 20 characters will be truncated to 20 characters.


Example response:
```
{
    "id":1,
    "key":"
    live_message_line0",
    "value":"Live Message Line 1"
}
```

#

### `read_keypad(self, action_type: str, entry: str) -> JSON`
Either updates or views the current keypad buffer. The keypad buffer will store all the keys pressed on the physical keypad until cleared.

`entry`: This will be used as the value of the keypad buffer. 
This parameter is only required when updating the buffer.

`action_type`: Can be set to "update" or "view". 

If set to update, it will then set keypad buffer equal to parameter sent. If set to view, it will return everything stored in the buffer.

Notes:
* Keypad buffer should initially be set to a known string prior to requesting user entry, for example START or blank.
* If the buffer overruns, update the keypad buffer after viewing. Try to read the buffer frequently enough to keep it below 255 characters at any point. 




Keys are saved as integer values which represent keypad digits or control keys and separated with a space delimiter:

    Digits:				        0..9 
    CANCEL control key:         C
    OK (Enter) control key:	    E


For example, entering the keypad sequence: `1234567890[CANCEL][OK]` would result in a response string of `“1 2 3 4 5 6 7 8 9 0 C E”`

Example of a response after keypad view command;

```
{
    "id":1,
    "parameter":"api_keypad_entry",
    "entry":"| 0 1 2 3 4 5 6 7 8 9 C E"
}
```

#

### **`class Pylock(BaseWrapper)`**
Inherits from the BaseWrapper and adds additional methods for conveient API calls.

Methods:

* `random_pins -> list or dict`

* `default_pins -> bool`

* `all_door_access -> bool`

Pylock provides some additional convenience methods that are not included in the original API. It abstracts the logic from the original endpoints and builds upon them. If you were to add moe convenience methods, this is the place to do so. 

#

### `random_pins(self, all_lockers: bool) -> dict  or list`

Generates a pseudo-random 4 digit pin, that is then stored as a list of strings. 

If `all_lockers` is set to `True`, the method will randomize pins for all lockers and will return a dictionary containing the new pins. This action physically sets a new pin for each locker.

If `all_lockers` is set to `False` or by default `None`, the methods returns a single list of strings representing the new pin. This action **does not** physically override any pins.  

Example return value with `all_lockers` set to `True`:
```
{
    0: ["0", "1", "2", "3"],
    1: ["1", "1", "3", "9"],
    ...
}
```

Example return value with `all_lockers` set to `False`:
```
["0", "0", "0", "0"]
```

#

### `default_pins(self, pin: list) -> bool`
Self explanatory method. Sets a default pin for all lockers.

`pin` expects a list of strings -> ["1", "2", "3", "4"]
#

### `all_door_access(self, locked: bool) -> bool:`
Provides easy access to all lockers at the same time.

First, the method retrieves all current pins by parsing the return value of `BaseWrapper.get_door_status`.

Second, the method calls `BaseWrapper.door_access` to unlock all lockers.

`locked` if set to `True`, locks all of the doors. If `False`, all doors will be unlocked. 
#

## **Notes on Testing**

The physical tower might not be available during the development process to test your API calls. For this reason, Pylock comes with a very basic mock Lock'n'Charge HTTP server written in Python. 

If you wish to test the wrapper in its current state, or if you wish to test your own application against the tower API, you may opt to use mock server.

You can simply launch the server with:

```
python3 mock_lnc_server.py
--------------------------
Starting server
Server listening...

127.0.0.1 - - [24/Aug/2022 18:48:39] "PUT /door/0 HTTP/1.1" 200 -
127.0.0.1 - - [24/Aug/2022 18:48:39] "PUT /status/tower/ HTTP/1.1" 200 -
127.0.0.1 - - [24/Aug/2022 18:48:39] "PUT /status/door/2 HTTP/1.1" 200 -
...
```
Remember to make necessary configuration changes in config.py to utilize the mock HTTP server.
#
