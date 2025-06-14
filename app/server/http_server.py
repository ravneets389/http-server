import socket
from .request_parser import parse_request
from .response_builder import make_response
from .route_handler import handle_route

class HttpServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.create_server((self.host, self.port))
        print(f"Server is running on {self.host}:{self.port}")

        while True:
            client_socket, _ = self.server_socket.accept()
            self.handle_request(client_socket)

    def handle_request(self, client_socket):
        with client_socket:
            try:
                request_data = ""
                while True:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        break
                    request_data += chunk.decode()
                    if '\r\n\r\n' in request_data:
                        break

                method, path, headers, body = parse_request(request_data)

                content_length = int(headers.get("Content-Length", 0))
                while len(body) < content_length:
                    body += client_socket.recv(1024).decode()

                content, status, content_type = handle_route(method, path, headers, body)
                response_data = make_response(content, status, content_type)
                client_socket.sendall(response_data)

            except Exception as e:
                print("Error:", e)
