from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def parse(self, byte_string):
        return {
            data[0]: data[1] for data in [
                str_bytes.split("=") for str_bytes in byte_string.decode("utf-8").split("&")
            ]
        }

    
    def handle_get_jwt(self, request):
        print("handle_get_jwt")
        print(request)
        print("______________________")

        expected_request_data = {
            "grant_type": "password",
            "client_id": "test_id",
            "client_secret": "test_secret",
            "username": "test_username",
            "password": "test_password"
        }
        print(expected_request_data)

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
        print("handle_door_access")
        print(request)
        print("______________________")

        expected_request_data = {
            "code_digit1": "0",
            "code_digit2": "0",
            "code_digit3": "0",
            "code_digit4": "0",
            "locked": "0"
        }

        print(expected_request_data)

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
        print("handle_set_door_pin")
        print(request)
        print("______________________")

        expected_request_data = {
            "code_digit1": "0",
            "code_digit2": "0",
            "code_digit3": "0",
            "code_digit4": "0",
        }

        print(expected_request_data)

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


    def handle_get_door_status(self, request):
        
        


    def do_POST(self):
        self.length = int(self.headers.get('Content-Length'))
        parsed = self.parse(self.rfile.read(self.length))

        print("PATH")
        print(self.path)
        print("_____________")

        if self.path == "/token":
            response = json.dumps(self.handle_get_jwt(request=parsed))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode(encoding='utf_8'))

    
    def do_PUT(self):
        self.length = int(self.headers.get('Content-Length'))
        parsed = self.parse(self.rfile.read(self.length))

        print("PATH")
        print(self.path)
        print("_____________")
        
        if self.path == "/door/0":
            response = json.dumps(self.handle_door_access(request=parsed))

        elif self.path == "/door/1":
            response = json.dumps(self.handle_set_door_pin(request=parsed))

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode(encoding='utf_8'))


def run(server_class=HTTPServer, handler_class=Handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    print("Starting server")
    print("Server listening...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
