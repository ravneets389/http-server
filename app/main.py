import socket

class HttpServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        self.server_socket = socket.create_server((self.host, self.port))
        print(f"Server is running on {self.host}:{self.port}")

        while True:
            client_socket, address = self.server_socket.accept()
            self.handle_request(client_socket)

    def handle_request(self, client_socket):
        with client_socket:
            try:    
                request_data = client_socket.recv(1024).decode()
                print(f"Request: {request_data}")
            except Exception as e:
                print("Error:",e)
            
            response_data = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "Hello, World!"
            )
            client_socket.sendall(response_data.encode())

if __name__ == "__main__":
    server = HttpServer()
    server.start()
