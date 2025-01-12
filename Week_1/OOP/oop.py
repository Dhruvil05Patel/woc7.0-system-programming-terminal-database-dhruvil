class KeyValueStore:
    def __init__(self):
        self.store = {}

    def add(self, key, value):
        self.store[key] = value

    def get(self, key):
        return self.store.get(key, "Key not found")

    def delete(self, key):
        if key in self.store:
            del self.store[key]
        else:
            print("Key not found")

    def display(self):
        for key, value in self.store.items():
            print(f"{key}: {value}")

#usage

kv_store = KeyValueStore()
kv_store.add("name", "dhruvil")
kv_store.add("age", 19)
kv_store.display()

print(kv_store.get("name"))
kv_store.delete("age")
kv_store.display()