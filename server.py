import socket
import threading
import json
import datetime
from urllib.parse import urlparse, parse_qs

HOST= '0.0.0.0'
PORT = 8080

database = []
id=1

def date():
    now = datetime.datetime.utcnow()
    return now.strftime('%a, %d %b %Y %H:%M:%S GMT')


def statusline(code):
      return {
        200: "OK",
        201: "Created",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        411: "Length Required",
        413: "Payload Too Large",
        500: "Internal Server Error"
    }.get(code, "OK")


def convert(body):
     
    if isinstance(body,(dict,list)):
          text=json.dumps(body)
          return text.encode('utf-8'), "application/json"
     
    if isinstance(body,bytes):
          return body, "application/octet-stream"
     
    return str(body).encode('utf-8'), "text/plain; charset=utf-8"

def reponse(statuscode, body="",extra_headers="None"):
    bodycontent, content_type = convert(body)

    reason = statusline(statuscode)
    status_line = f"HTTP/1.1 {statuscode} {reason}\r\n"

    headers = {
        "Date": date(),
        "Server": "WebServer/1.0",
        "Content-Type": content_type,
        "Content-Length": str(len(bodycontent)),
        "Connection": "close"
    }

    if extra_headers:
        headers.update(extra_headers)

    header_lines = "".join(f"{k}: {v}\r\n" for k, v in headers.items())

    response = (status_line + header_lines + "\r\n").encode('utf-8') + bodycontent
    return response

     


