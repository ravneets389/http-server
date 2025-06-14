import os
from urllib.parse import parse_qs
from .utils import guess_content_type
from .utils import render_template

def handle_route(method, path, headers, body):
    if method == "GET":
        file_path = os.path.join("public", (path + ".html").lstrip("/"))
        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()
            return content, 200, guess_content_type(file_path)
        else:
            return b"404 Not Found", 404, "text/plain"

    elif method == "POST":
        if path == "/echo":
            return f"You sent: {body}".encode(), 200, "text/plain"
        elif path == "/greet":
            parsed_data = parse_qs(body)
            name = parsed_data.get('name',[''])[0]
            content = render_template("greet.html", {"name":name})
            return content, 200, "text/html"
        else:
            return b"404 Not Found", 404, "text/plain"

    return b"405 Method Not Allowed", 405, "text/plain"
