import socket

def send_message_to_server(host='localhost', port=12345, message="Hello, Server!"):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((host, port))

    try:
        client_socket.sendall(message.encode())
        data = client_socket.recv(1024)
        print(f"Server response: {data.decode()}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    send_message_to_server(message="Hello, Server!")