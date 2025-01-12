import json

def save_dict_to_json(dictionary, file_path):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(dictionary, json_file, indent=4)
        print(f"Dictionary successfully saved to {file_path}")
    except Exception as e:
        print(f"An error occurred while saving the dictionary: {e}")

def load_dict_from_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            dictionary = json.load(json_file)
        print(f"Dictionary successfully loaded from {file_path}")
        return dictionary
    except Exception as e:
        print(f"An error occurred while loading the dictionary: {e}")
        return None

if __name__ == "__main__":
    my_dict = {
        "name": "Dhruvil",
        "age": 19,
        "hobbies": ["gaming", "coding", "reading"],
        "is_student": True
    }

    file_path = "example.json"

    save_dict_to_json(my_dict, file_path)

    loaded_dict = load_dict_from_json(file_path)

    print("Loaded Dictionary:", loaded_dict)