import socket

def start_server(host='localhost', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind((host, port))

    server_socket.listen(1)
    print(f"Server listening on {host}:{port}...")

    connection, client_address = server_socket.accept()
    print(f"Connection established with {client_address}")

    try:
        data = connection.recv(1024)
        print(f"Received message: {data.decode()}")

        response = "Message received successfully!"
        connection.sendall(response.encode())

    finally:
        connection.close()

if __name__ == "__main__":
    start_server()