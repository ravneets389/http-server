def parse_request(request_data):
    header_part, _, body = request_data.partition("\r\n\r\n")
    req_lines = header_part.splitlines()
    method, path, _ = req_lines[0].split()
    headers = {}
    for line in req_lines[1:]:
        key, value = line.split(":", 1)
        headers[key.strip()] = value.strip()
    return method, path, headers, body
