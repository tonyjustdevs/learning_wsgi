import socket

def tp_server():
    HOST = "localhost"
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        
        client_socket, addr = s.accept()
        buffer = b""
        while True:
            data_bytes = client_socket.recv(1024)
            if not data_bytes:
                break
            print(f"[t] recived: {data_bytes}") #  b'hello from client\nIt'sTony'
            buffer += data_bytes
            while b'\n' in buffer:
                response, buffer = buffer.split(b'\n') # b'hello from client' 
                response = response+ b'\n'
                client_socket.sendall(response)
tp_server()
        
        # def start_response(status, headers):
        #     request_line = "http ..."
        #     header_line = "for header in headers ..."
            
        # body_resp_str_iterable =  tony_wsgi_app(environ, start_response)
        # for body_str in body_resp_str_iterable:
        #     client_socket.sendall(body_str.encode("utf-8"))

            
# def handle_request(conn):
    
            