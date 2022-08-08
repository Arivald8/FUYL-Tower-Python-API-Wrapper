from http.server import BaseHTTPRequestHandler
import socketserver

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "GET response"
        self.wfile.write(bytes(message, "utf8"))

    def do_POST(self):
        print("are we ever here")
        print(self.headers.get('Content-Length'))
        print("there we went")
        print(self.responses)
        try:
            content_len = int(self.headers.get('Content-Length'))
        except TypeError:
            content_len = 5
        post_body = self.rfile.read(content_len)
        print("DEBUG")
        print(post_body)
        print("ENDBUG")
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "POST response"
        self.wfile.write(bytes(message, "utf8"))


def run_webserver():
    port = 9000
    busy_conn = True

    while busy_conn:
        try:
            print(f"Starting web server on port {port}")
            httpd = socketserver.TCPServer(('127.0.0.1', port), handler)
            httpd.serve_forever(poll_interval=0.5)
        except OSError:
            print(f"Port {port} is busy. Switching ports.")
            port += 1
    
    return

if __name__ == "__main__":
    run_webserver()