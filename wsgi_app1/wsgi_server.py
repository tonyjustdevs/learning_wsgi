import socket
from wsgi_apps import wsgi_app_v1_echo

from typing import List, Any, Tuple
# pep3333: The server or gateway invokes the application callable once for each request 
# it receives from an HTTP client, that is directed at the application.

def simple_wsgi_server(simple_wsgi_app: function):
    HOST = "localhost"
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        
        client_socket, addr = s.accept()
        print(addr)
        # environ_dict is created from client request (from client_socket)
        # i.e. data_bytes (client request) from client_socket
        # data_bytes is just byte_string, follows certain format if connected via
        # - browser, or curl, or simple byte_string like from client.py
        # handle_request(): to parse() data_bytes -> something meaningful...
        # create a dict with request and set defaults as well
        # e.g. METHOD requested: 'GET','POST', ...
        # e.g. PATH requested: '/','/hello','
        # ref: https://peps.python.org/pep-3333/#environ-variables
        environ = handle_request_v1_echo(client_socket) 
        
        print(f"[internal]: {environ} from simple_wsgi_server()")
        # {'wsgi.input': b"hello from tony's client\npsg-arsenal tonight lads!\nbye\n"} from simple_wsgi_server()
        def start_response(status: str, headers: List[(Tuple[Any,Any])]):
            # wsgi_app provides arguments: 'status' & 'headers' arguments 
            # e.g. status "200 OK" 
            # e.g. header [(Content-type,"text/plain")]
            # create dict from these arguments and whatever server response we want
            # wsgi_app calls start_response(status, headers)
            # server send status and headers responses to client via socket?
            pass
        # req_v1: environ["wsgi.input"] = buffer
        # body_resp_iterable = wsgi_app_v1_echo(environ, start_response)
        body_resp_iterable = simple_wsgi_app(environ, start_response)
        
        for body_byte in body_resp_iterable:
            body_byte = body_byte+ b'\n'
            client_socket.sendall(body_byte)


def handle_request_v1_echo(conn: socket.socket) -> dict[str, bytes]:
    '''for parsing non-http byte string from client_v1.py'''
    buffer: bytes = b""
    print(f"handle_request_v1: building buffer until client disconnects...")
    while True:
        data_bytes: bytes = conn.recv(1024)
        if not data_bytes:
            break
        buffer += data_bytes # after each timeout, buffet appends more bytes
        print(f"current_buffer: {buffer}")
    # gonna just add response to wsgi.input because this app is echoing only
    environ_dict: dict[str, bytes] = {}
    environ_dict["wsgi.input"] = buffer
    return environ_dict

    # okay i think this is supposed to be used by data from POST but since this first version echos the
    # exact bytes then its fine for now...
    
    # wsgi.input (https://peps.python.org/pep-3333/#environ-variables)
    # An input stream (file-like object) from which the HTTP request body bytes can be read. 
    # (The server or gateway may perform reads on-demand as requested by the application, 
    # or it may pre-read the client’s request body and buffer it in-memory or on disk, 
    # or use any other technique for providing such an input stream,  according to its preference.)


simple_wsgi_server(wsgi_app_v1_echo)
