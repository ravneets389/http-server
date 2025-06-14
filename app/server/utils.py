import os

def guess_content_type(file_path):
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

def render_template(template_name, context):
    #populate the template and return the content
    template_path = os.path.join("templates",template_name)
    if not os.path.isfile(template_path):
        return f"{template_name} not found".encode()
    
    with open(template_path,"r",encoding="utf-8") as f:
        content = f.read()
    
    for key,value in context.items():
        placeholder = "{{ "+ key+ " }}"
        content = content.replace(placeholder, str(value))
    
    return content.encode()