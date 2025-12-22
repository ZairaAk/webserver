import socket
import threading
import json
import datetime
from urllib.parse import urlparse, parse_qs

HOST= '0.0.0.0' #this will allow external connections
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
        500: "Internal Server Error"
    }.get(code, "OK")


def convert(body):
     
    if isinstance(body,(dict,list)):
          text=json.dumps(body)
          return text.encode('utf-8'), "application/json"
     
    if isinstance(body,bytes):
          return body, "application/octet-stream"
     
    return str(body).encode('utf-8'), "text/plain; charset=utf-8"

def response(statuscode, body="",extra_headers="None"):
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
#from here,the client has sent the request and now will organise it and work on that
def parse(request_text):
     parts= request_text.split("\r\n\r\n",1)
     header=parts[0]
     body=parts[1]



     lines=header.split("\r\n")
     if len(lines) == 0:
        raise ValueError("Empty request")
     
     requestline=lines[0]
     tokens = requestline.split()
     if len(tokens) != 3:
        raise ValueError("Malformed request line")
     
     method=tokens[0]
     path=tokens[1]
     version=tokens[2]

     headers={}

     for l in lines[1:]:
          if not l:
               continue
          if ":" not in l:
               raise ValueError(f"Malformed header line: {l}")
          name, value = l.split(":", 1)
          headers[name.strip().lower()] = value.strip() 


     return {
        "method": method,
        "path": path,
        "version": version,
        "headers": headers,
        "body": body
     }


   #conn: recieves and sends http requests/responses(unique)-socket connected to client
   #addr: client address

   


    

  
           
              


         
         

          

 


     


