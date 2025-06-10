import socket
import os

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
                content_length = int(headers.get('Content-Length',0)) #guard against missing content-length
                while len(body) < content_length:
                    chunk = client_socket.recv(1024)
                    body += chunk.decode()
                
            except Exception as e:
                print("Error:",e)
            

            response_body, status_code, content_type = self.request_actions(method,path,headers,body)
            response_data = self.make_response(response_body, status_code, content_type)
            
            client_socket.sendall(response_data)
        
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
    
    def request_actions(self, method, path, headers, body):
        if method == "GET":
            f_path = path + ".html"
            file_path = os.path.join("public", f_path.lstrip("/"))

            if os.path.isfile(file_path):
                with open(file_path,"rb") as file:
                    content = file.read()
                return content,200,self.guess_content_type(file_path)
            else:
                return b"404 Not Found",404,"text/plain"
            
        elif method == "POST":
            if path == "/echo":
                content = f"You sent: {body}"
                return content.encode(), 200, "text/plain"
            if path == "/greet":
                name = body.strip()
                content = f"Hi there! {name}."
                return content.encode(),200,"text/plain"
            else:
                content = "404 Not Found"
                return content.encode(),404,"text/plain"
            
        else:
            content = b"405 Method Not Allowed"
            return content,405,"text/plain"

    def make_response(self,content, status_code=200, content_type="text/plain"):
        body = content
        status_messages = {200: "OK", 404: "Not Found", 405: "Method Not Allowed"}

        return (
            f"HTTP/1.1 {status_code} {status_messages.get(status_code,"Unknown")}\r\n"
            f"Content-Type: {content_type}\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
        ).encode() + body
    
    def guess_content_type(self, file_path):
        if file_path.endswith(".html"):
            return "text/html"
        elif file_path.endswith(".css"):
            return "text/css"
        elif file_path.endswith(".js"):
            return "application/javascript"
        elif file_path.endswith(".png"):
            return "image/png"
        elif file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
            return "image/jpeg"
        elif file_path.endswith(".json"):
            return "application/json"
        else:
            return "application/octet-stream"

if __name__ == "__main__":
    server = HttpServer()
    server.start()
