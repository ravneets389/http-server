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
                # print(f"Request: {request_data}")
            except Exception as e:
                print("Error:",e)
            
            self.parse_request(request_data)
            response_data = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "Content-Length: 13\r\n"
                "\r\n"
                "Hello, World!"
            )
            client_socket.sendall(response_data.encode())
    
    def parse_request(self, request_data):
        #start line looks like : <method> <request-target> <protocol> ex. POST /index HTTP/1.1
        #typical structure is start lines, headers and (CRLF) then body
        header_part, _, body = request_data.partition("\r\n\r\n")
        req_lines = header_part.splitlines()
        
        method,path,req_protocol = req_lines[0].split()
        headers = {}
        for line in req_lines[1:]:
            key, value = line.split(":",1)
            headers[key.strip()] = value.strip()
        
        # print(headers,body)
        return method, path, headers, body

if __name__ == "__main__":
    server = HttpServer()
    server.start()
