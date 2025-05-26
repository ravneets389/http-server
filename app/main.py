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
                # for repeated large concatenations, use a list - append , and copy at last
                chunks = []
                request_data = ""
                while True:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        break
                    request_data += chunk.decode()
                    if '\r\n\r\n' in request_data:
                        break #end of headers (might have some body content too in it)
                
                # print(f"Request: {request_data}")
                method, path, headers, body = self.parse_request(request_data)
                
                #parse remaining body
                content_length = int(headers['Content-Length'])
                while len(body) < content_length:
                    chunk = client_socket.recv(1024)
                    body += chunk.decode()
                
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
