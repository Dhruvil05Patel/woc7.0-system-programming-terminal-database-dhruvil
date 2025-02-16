import socket


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    # Authentication process without hashing
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        auth_data = f"AUTH {username} {password}"
        client.send(auth_data.encode("utf-8"))
        auth_response = client.recv(1024).decode("utf-8")
        print(auth_response)

        if "Authentication successful" in auth_response:
            break
        else:
            print("Try again.")

    while True:
        command = input("Enter command: ")
        if command.lower() == "exit":
            break

        client.send(command.encode("utf-8"))
        response = client.recv(1024).decode("utf-8")
        print(response)

    client.close()
    print("Client disconnected.")


if __name__ == "__main__":
    start_client()
