import socket
def tp_client():
    HOST = "localhost"
    PORT = 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        messages = ["hello from tony's client", "psg-arsenal tonight lads!", "bye"]
        for msg in messages:
            msg = msg+'\n'
            print(f"[t] sent {msg!r}")
            client_socket.sendall(msg.encode("utf-8"))
            while True:
                data_bytes_received = client_socket.recv(1024)
                if not data_bytes_received:
                    break
                
                print(f"[t] server replied: {data_bytes_received}")
                if b'\n' in data_bytes_received:
                    break
tp_client()