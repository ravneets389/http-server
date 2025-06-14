import socket
import threading
from .request_parser import parse_request
from .response_builder import make_response
from .route_handler import handle_route
from .logger import log_info, log_error

class HttpServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.create_server((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server is running on {self.host}:{self.port}")

        while True:
            client_socket, _ = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_request, args= (client_socket), daemon=True)
            thread.start()
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

                log_info(f"Received {method} request for {path}")
                content, status_code, content_type = handle_route(method, path, headers, body)
                log_info(f"Responding with {status_code} for {method} {path}")

                response_data = make_response(content, status_code, content_type)
                client_socket.sendall(response_data)

            except Exception as e:
                log_error(f"Exception while handling request: {e}")
