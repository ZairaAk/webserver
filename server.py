import socket
import threading
import json
import datetime
from urllib.parse import urlparse, parse_qs #urlparse: splits url into path and query,parse_qs:query to keyvalue pair

HOST= '0.0.0.0' #this will allow external connections
PORT = 9999

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

def response(statuscode, body="",extra_headers=None): #server->client
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
def parse(request_text):  #parse:client->server
     parts= request_text.split("\r\n\r\n",1) #(separator,maxsplit)
     header=parts[0]
     body=parts[1]



     lines=header.split("\r\n")
     if len(lines) == 0:
        raise ValueError("Empty request")
     
     requestline=lines[0] #METHOD PATH VERSION
     tokens = requestline.split()
     if len(tokens) != 3:
        raise ValueError("Malformed request line")
     
     method=tokens[0]
     path=tokens[1]
     version=tokens[2]

     headers={} #parse header into dict

     for l in lines[1:]: #skipping request line
          if not l: #ignoring empty lines
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
def handle_client(conn, addr):

    try:
        raw = conn.recv(65536)
        if not raw:         
            return
                        
        try:
            request_text =raw.decode("utf-8")

        except UnicodeDecodeError:            
            conn.sendall(response(400, "Cannot decode request"))          
            return
        
        try:
            req=parse(request_text)
        except ValueError as e:
            conn.sendall(response(400,str(e)))         
            return
        
        method= req["method"]
        path= req["path"]
        parsed = urlparse(path)

        if method=="GET" and parsed.path == "/":
            conn.sendall(response(200, "Welcome to my HTTP server"))
        elif method=="GET" and parsed.path=="/echo":
            query=parse_qs(parsed.query)
            message = query.get("message", [""])[0]
            conn.sendall(response(200, message))
        elif method=="POST" and parsed.path=="/data":

            headers=req["headers"]

            if "content-length" not in headers:
                conn.sendall(response(411, "Content-Length required"))
                return

            length = int(headers["content-length"])

            body=req["body"][:length] #avoid extra junk and take upto user defined length

            try:
                payload = json.loads(body) #text → real Python data
            except json.JSONDecodeError:
                conn.sendall(response(400, "Invalid JSON"))
                return

            database.append(payload)

            conn.sendall(response(201, payload))


        else:
            conn.sendall(response(404, "Not Found"))
   
    except Exception:
        conn.sendall(response(500, "Internal Server Error"))

    finally:
        conn.close()   
 

def start_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #1st socket=module,2nd=class
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #1-enable, 0-disable

    server.bind((HOST,PORT)) #why double bracks?? ---> bind accepts 1 arg so passing this as a tuple
    server.listen(5) #can queue upto 5 pending connections

    print(f"Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(
            target=handle_client,
            args=(conn, addr)
        )
        thread.start()     

if __name__ == "__main__": #prevents code from running when file is imported
    start_server()

   
