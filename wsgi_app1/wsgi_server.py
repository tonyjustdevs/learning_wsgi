import socket
from wsgi_apps import wsgi_app_v1_echo
# from wsgi_clients import wsgi_client_v2_no_timeout # BADDDDDDDDDDDD YOU DONT NEED TO IMPORT CLIENT
#### CLIENT ONLY TO HIT THE SERVER FROM TERMINAL
#### ONLY NEED TO IMPORT APP: BECAUSE SERVER(APP) RUNS THE APP!!!!!

from typing import Callable, List, Any, Tuple
# pep3333: The server or gateway invokes the application callable once for each request 
# it receives from an HTTP client, that is directed at the application.

def simple_wsgi_server(simple_wsgi_app: Callable):
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
        # environ = handle_request_v1_echo(client_socket) 
        environ = handle_request_v2_non_http(client_socket) 
        
        print(f"[wsgi_server] environ: {environ}\n\n")
        # {'wsgi.input': b"hello from tony's client\npsg-arsenal tonight lads!\nbye\n"} from simple_wsgi_server()
        def start_response(status: str, headers: List[Tuple[Any, Any]]) -> None:
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
        print(f"[t] body_response_iterable from app: {body_resp_iterable}, {type(body_resp_iterable)}\n\n")
        body_resp_str = body_resp_iterable[0]
        while b'\n' in body_resp_str:
            buffer_byte, body_resp_str = body_resp_str.split(b'\n',1)
            print(f"splitting by newlines:...\n\n")
            print(f"\nbuffer {buffer_byte}, {type(buffer_byte)} \nbody_rest: {body_resp_str}, {type(body_resp_str)}")
            buffer_byte = buffer_byte+ b'\n'
            client_socket.sendall(buffer_byte)


        # for body_byte in body_resp_iterable:
        #     body_byte = body_byte+ b'\n'
        #     client_socket.sendall(body_byte)

def handle_request_v2_non_http(client_socket):
    '''parsing non-http_string from client_v1.py'''
    buffer: bytes = b""
    print(f"[server][handle_request_v1] building buffer received from client...\n\n")
    i=1
    while True:
        data_bytes: bytes = client_socket.recv(1025)
        print(f"[expected_from_client_1st] b'first message\n'")
        # b"received1st message+b'\\r\\n'"
        print(f"[received_msg_{i}]: {data_bytes}")
        if b"\r\n\r\n" in data_bytes:
            environ_dict: dict[str, bytes] = {}
            environ_dict["wsgi.input"] = buffer
            return environ_dict
        buffer += data_bytes # after each timeout, buffet appends more bytes
        print(f"current_buffer: {buffer}\n\n")
        response_bytes= b"received" + data_bytes
        client_socket.sendall(response_bytes)
        i+=1

def handle_request_v1_echo(conn: socket.socket) -> dict[str, bytes]:
    '''for parsing non-http byte string from client_v1.py'''
    buffer: bytes = b""
    print(f"handle_request_v1: building buffer until client disconnects...\n\n")
    while True:
        data_bytes: bytes = conn.recv(1024)
        if not data_bytes:
            print("[handle_req_v1] server disconn in while break statement?")
            break
        buffer += data_bytes # after each timeout, buffet appends more bytes
        print(f"current_buffer: {buffer}\n\n")
    
    
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
