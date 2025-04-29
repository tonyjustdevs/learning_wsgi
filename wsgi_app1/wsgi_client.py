import socket
def wsgi_client_v1():
    HOST = "localhost"
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.settimeout(2.0) # wait up to 2 seconds
        messages = ["hello from tony's client", "psg-arsenal tonight lads!", "bye"]
        for msg in messages:
            msg = msg+'\n'
            print(f"[t] sent {msg!r}")
            client_socket.sendall(msg.encode("utf-8"))
            while True:
                try:
                    data_bytes_received = client_socket.recv(1024)
                    if not data_bytes_received: 
                        break
                    print(f"[t] server replied: {data_bytes_received}")
                    if b'\n' in data_bytes_received:
                        break
                except socket.timeout:
                    print(f"...")
                    break
wsgi_client_v1()