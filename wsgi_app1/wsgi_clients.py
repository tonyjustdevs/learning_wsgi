import socket

def wsgi_client_v2_no_timeout():
    HOST = "localhost"
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        def send_messages(client_socket, msgs: list[str]= ["first message", "2nd massage", "bye"]):
            for i,msg in enumerate(msgs):
                byte_prefix = '\r\n'
                if i == len(msgs)-1:
                    print(f"\nReached last msg!")   
                    byte_prefix = '\r\n\r\n'
                    print(f"attaching final prefix: {byte_prefix}")
                
                request_msg_bytes = f"{msg}+{byte_prefix}".encode("utf-8")
                
                client_socket.sendall(request_msg_bytes)
                print(f"\n[clientside] sent: {request_msg_bytes!r}...")
                while True:
                    # send(msg) of msgs: 
                    #   [1] no_response:    wait forever..  
                    #   [2] response:       next send(msg) of msgs
                        data_bytes_received = client_socket.recv(1024)
                        print(f"[clientside] received: {data_bytes_received}")
                        print(f"[clientside] check if ending..")
                        if "\r\n\r\n" in data_bytes_received:
                            break # go next msg
        with client_socket:
            send_messages(client_socket, ["1st message", "2nd massage", "bye"])
wsgi_client_v2_no_timeout()
# wsgi_client_v2_no_timeout()

def non_http_client_v1():
    HOST = "localhost"
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        
        def send_messages(messages: list[str]= ["first message", "2nd massage", "bye"], timeout_secs: int=2):
            client_socket.settimeout(timeout_secs)
            for msg in messages:
                msg = msg+'\n'
                client_socket.sendall(msg.encode("utf-8"))
                print(f"\n[from client] sent {msg!r}, waiting for reply...")
                while True:
                    try:
                        data_bytes_received = client_socket.recv(1024)
                        print(f"[t] server replied: {data_bytes_received}")
                    except socket.timeout:
                        print(f"[t] server didnt reply, sending next message...")
                        break
        
        send_messages(["first message", "2nd massage", "bye"])
        
        # while True:
        #     client_socket.settimeout(60)
            
        #     print(f"[from client] waiting for reply forever...")
        #     data_bytes_received = client_socket.recv(1024)
        #     if not data_bytes_received: 
        #         print(f"Nothing received...ending?")
        #         break
        #     print(f"[t] server replied: {data_bytes_received}")
        #     if b'\n\n' in data_bytes_received:
        #         print(f"Received end of message!...ending!")
#         #         break

        
# non_http_client_v1()