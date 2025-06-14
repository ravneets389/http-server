def make_response(content, status_code=200, content_type="text/plain"):
    status_messages = {
        200: "OK",
        404: "Not Found",
        405: "Method Not Allowed"
    }
    return (
        f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
        f"Content-Type: {content_type}\r\n"
        f"Content-Length: {len(content)}\r\n"
        "\r\n"
    ).encode() + content
