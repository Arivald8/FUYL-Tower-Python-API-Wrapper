"""
Pylock.py defines an additional class which inherits from BaseWrapper.

Here you can find all additional methods that are not directly built-into the official API specification. The methods cover common usage tasks such as randomizing pins for all lockers, setting a default pin for all lockers,
locking or unlocking all lockers etc. 
"""
from pylock.base_wrapper import BaseWrapper
from random import randint


class Pylock(BaseWrapper):    
    def __init__(self, tower_id=None, tower_location=None):
        """
        If management of multiple towers is required, please specify the tower_id and tower_location to distingush between towers. Remember to provide the IP address of each tower to each instance separately.  
        """

        self.tower_id = tower_id
        self.tower_location = tower_location


    def random_pins(self, all_lockers: bool) -> dict or list:
        """
        Generates a pseudo-random 4 digit pin, that is then stored as a list of strings. 

        If all_lockers is set to True, the method will randomize pins for all lockers and will return a dictionary containing the new pins. This action sets a new pin for each locker.

        If all_lockers is set to False or None, the methods returns a single list of strings representing the new pin. This action does not override any pins.  
        """
        if all_lockers:
            randomized_pins = {
                _: [f"{randint(0, 9)}" for _ in range(4)] for _ in range(16)
            }
            for locker, pin in randomized_pins.values():
                self.set_door_pin(locker, pin)
            return randomized_pins
        else:
            return [f"{randint(0, 9)}" for _ in range(4)]


    def default_pins(self, pin: list) -> bool:
        """
        Sets a default pin for all lockers.
        pin expects a list of strings -> ["1", "2", "3", "4"]
        """
        return True if [
            self.set_door_pin(locker, pin) for locker in range(15)
        ] else False


    def all_door_access(self, locked: bool) -> bool:
        """
        First, the method retrieves all current pins by parsing the return value of BaseWrapper.get_door_status.

        Second, the method calls BaseWrapper.door_access to unlock all lockers.

        locked: bool if True, all doors will be locked. If False, all doors will be unlocked. 
        """
        pins_dict = {}
        for locker in range(15):
            for key, value in self.get_door_status("door", locker):
                if key == "locker_id":
                    pins_dict[key] = value
                for digit in range(1,5):
                    if key == f"code_digits{digit}":
                        pins_dict[key] = value

            self.door_access(
                pin=pins_dict[locker],
                door_number=locker,
                lock_status=locked
            )
        return True if pins_dict else False


