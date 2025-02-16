import socket
import json
import os
import threading

# File paths
USER_FILE = "users.json"
DB_FOLDER = "databases"


# Load users from JSON
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as f:
            json.dump({}, f)
    with open(USER_FILE, "r") as f:
        return json.load(f)


# Save users to JSON
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)


# Authenticate user
def authenticate(username, password):
    users = load_users()
    return users.get(username) == password  # Plain text check


# Global dictionary to store current database for each client
client_dbs = {}


# Process database commands
def process_command(client_id, command):
    if client_id not in client_dbs:
        client_dbs[client_id] = None  # Initialize client database

    parts = command.strip().split(" ", 2)
    action = parts[0].upper()

    if action == "CREATE":
        if parts[1].upper() == "DATABASE":
            db_name = parts[2].strip()
            db_path = os.path.join(DB_FOLDER, f"{db_name}.json")
            if not os.path.exists(DB_FOLDER):
                os.makedirs(DB_FOLDER)
            if not os.path.exists(db_path):
                with open(db_path, "w") as f:
                    json.dump({}, f)
                return f"Database '{db_name}' created."
            else:
                return f"Database '{db_name}' already exists."

        elif parts[1].upper() == "TABLE":
            if not client_dbs[client_id]:
                return "No database selected. Use USE DATABASE <db_name> first."
            table_name, schema = parts[2].split("(", 1)
            table_name = table_name.strip()
            schema = schema.strip(")").split(", ")
            db_path = os.path.join(DB_FOLDER, f"{client_dbs[client_id]}.json")

            with open(db_path, "r") as f:
                db_data = json.load(f)
            if table_name not in db_data:
                db_data[table_name] = {"schema": schema, "entries": {}}
                with open(db_path, "w") as f:
                    json.dump(db_data, f, indent=4)
                return f"Table '{table_name}' created with schema {schema}."
            else:
                return f"Table '{table_name}' already exists."

    elif action == "USE":
        if parts[1].upper() == "DATABASE":
            db_name = parts[2].strip()
            db_path = os.path.join(DB_FOLDER, f"{db_name}.json")
            if os.path.exists(db_path):
                client_dbs[client_id] = db_name
                return f"Switched to database '{db_name}'."
            else:
                return f"Database '{db_name}' does not exist."

    elif action == "INSERT":
        if not client_dbs[client_id]:
            return "No database selected. Use USE DATABASE <db_name> first."
        parts = command.split("VALUES")
        table_name = parts[0].split("INTO")[1].strip()
        values = parts[1].strip(" ()").split(", ")
        db_path = os.path.join(DB_FOLDER, f"{client_dbs[client_id]}.json")

        with open(db_path, "r") as f:
            db_data = json.load(f)
        if table_name in db_data:
            entry_id = values[0]
            db_data[table_name]["entries"][entry_id] = values
            with open(db_path, "w") as f:
                json.dump(db_data, f, indent=4)
            return f"Inserted {values} into '{table_name}'."
        else:
            return f"Table '{table_name}' does not exist."

    elif action == "GET":
        if not client_dbs[client_id]:
            return "No database selected. Use USE DATABASE <db_name> first."
        parts = command.split("WHERE")
        if len(parts) < 2:
            return "Invalid query format."

        table_name, condition = parts[0].split("FROM")[1].strip(), parts[1].strip()
        db_path = os.path.join(DB_FOLDER, f"{client_dbs[client_id]}.json")

        with open(db_path, "r") as f:
            db_data = json.load(f)
        if table_name in db_data:
            entries = db_data[table_name]["entries"]
            if "key =" in condition:
                key_value = condition.split("=")[1].strip()
                if key_value in entries:
                    return f"Entry: {entries[key_value]}"
                else:
                    return "No matching entry found."
            return f"Entries in '{table_name}': {entries}"
        else:
            return f"Table '{table_name}' does not exist."

    return "Invalid command."


# Handle client connections
def handle_client(client_socket, addr, client_id):
    print(f"New connection from {addr}")

    authenticated = False
    while not authenticated:
        auth_data = client_socket.recv(1024).decode("utf-8").strip()
        if auth_data.startswith("AUTH"):
            _, username, password = auth_data.split(" ", 2)
            if authenticate(username, password):
                client_socket.send("Authentication successful".encode("utf-8"))
                authenticated = True
            else:
                client_socket.send("Authentication failed. Try again.".encode("utf-8"))

    client_dbs[client_id] = None  # Reset current database for this client

    while True:
        command = client_socket.recv(1024).decode("utf-8").strip()
        if not command or command.lower() == "exit":
            break
        response = process_command(client_id, command)
        client_socket.send(response.encode("utf-8"))

    client_socket.close()
    print(f"Client {addr} disconnected.")
    del client_dbs[client_id]  # Remove client-specific data when they disconnect


# Start server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 9999))
    server.listen(5)
    print("Server is running on port 9999...")

    client_id = 0
    while True:
        client_socket, addr = server.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr, client_id))
        client_thread.start()
        client_id += 1


if __name__ == "__main__":
    start_server()