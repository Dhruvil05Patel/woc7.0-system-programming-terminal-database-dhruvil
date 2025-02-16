import os
import json

class KeyValueDatabase:
    def __init__(self, base_dir="databases"):
        self.base_dir = base_dir
        self.current_db = None
        os.makedirs(self.base_dir, exist_ok=True)

    def create_database(self, db_name):
        db_path = os.path.join(self.base_dir, db_name)
        os.makedirs(db_path, exist_ok=True)
        print(f"Database '{db_name}' created.")

    def list_databases(self):
        print("Databases:", os.listdir(self.base_dir))

    def use_database(self, db_name):
        if db_name in os.listdir(self.base_dir):
            self.current_db = db_name
            print(f"Switched to database '{db_name}'.")
        else:
            print("Database does not exist.")

    def create_table(self, table_name):
        if not self.current_db:
            print("No database selected.")
            return
        table_path = os.path.join(self.base_dir, self.current_db, f"{table_name}.json")
        if not os.path.exists(table_path):
            with open(table_path, "w") as f:
                json.dump({}, f)
            print(f"Table '{table_name}' created.")
        else:
            print("Table already exists.")

    def list_tables(self):
        if not self.current_db:
            print("No database selected.")
            return
        print("Tables:", [f[:-5] for f in os.listdir(os.path.join(self.base_dir, self.current_db))])

    def insert_entry(self, table_name, key, value):
        if not self.current_db:
            print("No database selected.")
            return
        table_path = os.path.join(self.base_dir, self.current_db, f"{table_name}.json")
        if not os.path.exists(table_path):
            print("Table does not exist.")
            return
        with open(table_path, "r+") as f:
            data = json.load(f)
            if key in data:
                print("Key already exists.")
                return
            data[key] = json.loads(value)
            f.seek(0)
            json.dump(data, f, indent=4)
        print(f"Entry '{key}' added to table '{table_name}'.")

    def list_entries(self, table_name):
        if not self.current_db:
            print("No database selected.")
            return
        table_path = os.path.join(self.base_dir, self.current_db, f"{table_name}.json")
        if os.path.exists(table_path):
            with open(table_path, "r") as f:
                print(json.dumps(json.load(f), indent=4))
        else:
            print("Table does not exist.")

    def update_entry(self, table_name, key, value):
        if not self.current_db:
            print("No database selected.")
            return
        table_path = os.path.join(self.base_dir, self.current_db, f"{table_name}.json")
        if os.path.exists(table_path):
            with open(table_path, "r+") as f:
                data = json.load(f)
                if key in data:
                    data[key].update(json.loads(value))
                    f.seek(0)
                    json.dump(data, f, indent=4)
                    print(f"Entry '{key}' updated.")
                else:
                    print("Key not found.")
        else:
            print("Table does not exist.")

    def delete_entry(self, table_name, key):
        if not self.current_db:
            print("No database selected.")
            return
        table_path = os.path.join(self.base_dir, self.current_db, f"{table_name}.json")
        if os.path.exists(table_path):
            with open(table_path, "r+") as f:
                data = json.load(f)
                if key in data:
                    del data[key]
                    f.seek(0)
                    f.truncate()
                    json.dump(data, f, indent=4)
                    print(f"Entry '{key}' deleted.")
                else:
                    print("Key not found.")
        else:
            print("Table does not exist.")

if __name__ == "__main__":
    db = KeyValueDatabase()
    db.create_database("test_db")
    db.use_database("test_db")
    db.create_table("users")
    db.insert_entry("users", "user1", '{"name": "Dhruvil", "age": 20}')
    db.list_entries("users")
    # db.delete_entry("users", "user1")  (To delete entries)
    # db.list_entries("users")
