from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
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
        expected_request_data = {
            "code_digit1": "0",
            "code_digit2": "0",
            "code_digit3": "0",
            "code_digit4": "0",
            "locked": "0"
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
            if self.path == "/status/door/2":
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
            if self.length == 7:
                parsed = str(self.rfile.read(self.length))
            else:
                parsed = None
        
        if self.path == "/door/0":
            response = json.dumps(self.handle_door_access(request=parsed))

        elif self.path == "/door/1":
            response = json.dumps(self.handle_set_door_pin(request=parsed))

        elif self.path == "/status/door/2":
            response = json.dumps(self.handle_get_door_status_specific_door())

        elif self.path == "/status/tower/":
            response = json.dumps(self.handle_get_door_status_full_tower())

        elif self.path == "/message/startup/line/0":
            response = json.dumps(self.handle_display_message(request=parsed))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            self.wfile.write(response.encode(encoding='utf_8'))
        except UnboundLocalError as no_response:
            response = {"err": no_response}
            self.wfile.write(response.encode(encoding="utf_8"))


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server")
    print("Server listening...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
