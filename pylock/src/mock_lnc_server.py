from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):

    def url_path_validation(self, parsed_request):
        door_paths = ["/door/" + str(door) for door in range(16)]

        if self.path in door_paths:
            return json.dumps(self.handle_door_access(parsed_request))

    def parse(self, byte_string):
        try:
            return {
                data[0]: data[1] for data in [
                    str_bytes.split("=") for str_bytes in byte_string.decode("utf-8").split("&")
                ]
            }
        except IndexError:
            return byte_string

    
    def handle_get_jwt(self, request):
        expected_request_data = {
            "grant_type": "password",
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test_username",
            "password": "test_password"
        }

        expected_response_data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJ...",
            "expires_in": "86400",
            "token_type": "bearer",
            "scope": "null",
            "refresh_token": "305837308432fe0086..."
        }

        return expected_response_data if request == expected_request_data else {    
            "access_token": "denied",
            "expires_in": "denied",
            "token_type": "denied",
            "scope": "denied",
            "refresh_token": "denied"
        }


    def handle_door_access(self, request):
        expected_response_data = {
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

        failed_response_data = {
            "Locker_id": "denied",
            "code_digit1": "denied",
            "code_digit2": "denied",
            "code_digit3": "denied",
            "code_digit4": "denied",
            "open_status": "denied",
            "retry_atempts": "denied",
            "locked": "denied",
            "quarantined": "denied",
            "Inspect_opened": "denied",
            "alarm": "denied"
        }

        try:
            pin_request = request['locked']
        except KeyError:
            # if keyerror, it means that the request is to change pin
            # not to open or close a locker
            expected_request_data = {
                "code_digit1": request["code_digit1"],
                "code_digit2": request["code_digit2"],
                "code_digit3": request["code_digit3"],
                "code_digit4": request["code_digit4"]
            }

            return expected_response_data if request == expected_request_data else failed_response_data

        expected_request_data = {
            "code_digit1": "0",
            "code_digit2": "0",
            "code_digit3": "0",
            "code_digit4": "0",
            "locked": "0"
        }


        return expected_response_data if request == expected_request_data else failed_response_data


    def handle_set_door_pin(self, request):
        expected_request_data = {
            "code_digit1": "0",
            "code_digit2": "0",
            "code_digit3": "0",
            "code_digit4": "0",
        }

        expected_response_data = {
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

        failed_response_data = {
            "Locker_id": "denied",
            "code_digit1": "denied",
            "code_digit2": "denied",
            "code_digit3": "denied",
            "code_digit4": "denied",
            "open_status": "denied",
            "retry_atempts": "denied",
            "locked": "denied",
            "quarantined": "denied",
            "Inspect_opened": "denied",
            "alarm": "denied"
        }

        return expected_response_data if request == expected_request_data else failed_response_data


    def handle_get_door_status_specific_door(self):
        auth = "Bearer eyJ0eXAiOiJKV1QiLCJ..."
        if self.headers.get('Authorization') == auth:
            if self.path == "/status/door/-1":
                return {
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

    
    def handle_get_door_status_full_tower(self):
        auth = "Bearer eyJ0eXAiOiJKV1QiLCJ..."
        if self.headers.get('Authorization') == auth:
            if self.path == "/status/tower/":
                return [
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

    
    def handle_display_message(self, request):
        expected_request_data = b'message'
        expected_response_data = {
            "id": 1,
            "key": "live_message_line0",
            "value":"Live Message Line 1"
        }
        return expected_response_data if request == expected_request_data else {
            "id": "denied",
            "key": "denied",
            "value": "denied"
        }


    def handle_read_keypad_default_buffer(self, request):
        expected_response_data = {
            "id": 1,
            "parameter": "api_keypad_entry",
            "entry": "| 0 1 2 3 4 5 6 7 8 9 C E"
        }
        return expected_response_data if request == b'' else {
            "id": "denied",
            "parameter": "denied",
            "entry": "denied"
        }


    def handle_conv_wrapper_random_pins(self, request):
        expected_request_data = {
            "code_digit1": request['code_digit1'],
            "code_digit2": request['code_digit2'],
            "code_digit3": request['code_digit3'],
            "code_digit4": request['code_digit4'],
        }

        expected_response_data = {
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

        failed_response_data = {
            "Locker_id": "denied",
            "code_digit1": "denied",
            "code_digit2": "denied",
            "code_digit3": "denied",
            "code_digit4": "denied",
            "open_status": "denied",
            "retry_atempts": "denied",
            "locked": "denied",
            "quarantined": "denied",
            "Inspect_opened": "denied",
            "alarm": "denied"
        }

        return expected_response_data if expected_request_data == request else failed_response_data
        

    def handle_all_door_access(self, request):
        expected_response_data = {
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

        return expected_response_data
    
    def handle_all_door_access_tower(self, request):
        return [
            {"locker_id":0,"code_digit1": 1,"code_digit2": 1,"code_digit3": 1,"code_digit4": 1,"retry_attempts":3,"locked":1,"quarantined":0,"inspect_opened":0,"alarm":0},

            {"locker_id":1,"code_digit1": 1,"code_digit2": 1,"code_digit3": 1,"code_digit4": 1,"retry_attempts":3,"locked":1,"quarantined":0,"inspect_opened":0,"alarm":0},
        ]

    def do_POST(self):
        self.length = int(self.headers.get('Content-Length'))
        parsed = self.parse(self.rfile.read(self.length))

        if self.path == "/token":
            response = json.dumps(self.handle_get_jwt(request=parsed))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode(encoding='utf_8'))

    
    def do_PUT(self):
        self.length = int(self.headers.get('Content-Length'))
        try:
            parsed = self.parse(self.rfile.read(self.length))

        except IndexError:
            # 7 -> str(message)
            if self.length == 7:
                parsed = str(self.rfile.read(self.length))
            else:
                parsed = None
        
        if self.path == "/door/0":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/1":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/2":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/3":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/4":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/5":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/6":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/7":
            response = json.dumps(self.handle_door_access(parsed))
            
        elif self.path == "/door/8":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/9":
            response = json.dumps(self.handle_door_access(parsed))
            
        elif self.path == "/door/10":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/11":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/12":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/13":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/14":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/15":
            response = json.dumps(self.handle_door_access(parsed))

        elif self.path == "/door/-1":
            response = json.dumps(self.handle_set_door_pin(request=parsed))

        elif self.path == "/status/door/-1":
            response = json.dumps(self.handle_get_door_status_specific_door())

        elif self.path == "/message/startup/line/0":
            response = json.dumps(self.handle_display_message(request=parsed))

        elif self.path == "/message/startup/line/1":
            response = json.dumps(self.handle_display_message(request=parsed))

        elif self.path == "/message/live/line/0":
            response = json.dumps(self.handle_display_message(request=parsed))

        elif self.path == "/message/live/line/1":
            response = json.dumps(self.handle_display_message(request=parsed))

        elif self.path == "/keypad/view":
            response = json.dumps(self.handle_read_keypad_default_buffer(request=parsed))

        elif self.path == "/status/door/0":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/1":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/2":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/3":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/4":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/5":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/6":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/6":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/7":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/8":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/9":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/10":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/11":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/12":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/13":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/14":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/door/15":
            response = json.dumps(self.handle_all_door_access(request=parsed))

        elif self.path == "/status/tower/":
            response = json.dumps(self.handle_all_door_access_tower(request=parsed))


        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        if 'response' not in locals():
            response = json.dumps(
                [
                    {"locker_id":0,"code_digit1": 1,"code_digit2": 1,"code_digit3": 1,"code_digit4": 1,"retry_attempts":3,"locked":1,"quarantined":0,"inspect_opened":0,"alarm":0},

                    {"locker_id":1,"code_digit1": 1,"code_digit2": 1,"code_digit3": 1,"code_digit4": 1,"retry_attempts":3,"locked":1,"quarantined":0,"inspect_opened":0,"alarm":0},
                ]
            )
        try:
            self.wfile.write(response.encode(encoding='utf_8'))
        except Exception as no_response:
            response = {"err": no_response}
            try:
                self.wfile.write(response.encode(encoding="utf_8"))
            except AttributeError:
                self.wfile.write(response)


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Server starting.")
    print("Server listening...")
    print("You can now start the tests.")
    httpd.serve_forever()


if __name__ == "__main__":
    run()


"""
elif self.path == "/status/tower/":
    response = json.dumps(self.handle_get_door_status_full_tower())
"""
