import os
import json
import hashlib
from os import system as os_system, name as os_name
from time import sleep as delay

# PRINTERS
def clear_console():
    delay(0.1)
    os_system('cls' if os_name == 'nt' else 'clear')

# METHODS
def get_json(filename: str):
    config_path = os.path.join(filename + ".json")
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def set_json(filename: str, data: dict):
    config_path = os.path.join(filename + ".json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def compute_token(**kwargs) -> str:
    data = ":".join([f"{i}" for i in kwargs.values()])
    return hashlib.sha256(data.encode()).hexdigest()
    
def get_dict(filename: str, *args: str) -> dict[str, str]:
    return {key : get_json(filename)[key] for key in args}

def make_token(name: str, **kwargs):
    token = compute_token(**kwargs)
    kwargs["token"] = token
    print(f"Token Create for: {name}")
    return kwargs
    
def update_config_with_token(filename: str, *args: str):
    kwargs = get_dict(filename, *args)
    kwargs = make_token(filename, **kwargs)
    set_json(filename, kwargs)
    
def update_with_token(filename: str, *args: str):
    args = get_json(filename)
    result = [make_token(f"{filename} {i}", **kwargs) for i, kwargs in enumerate(args)]
    set_json(filename, result)

if __name__ == "__main__":
    while True:
        clear_console()
        try:
            print("Prompt the filename first without extension. This automatically detects json.")
            print("Add the field reference to be hashed. Separate them by space in the same prompt as the Filename.")
            temp = input("Filename and reference fields > ").strip().split()
            if len(temp) > 0:
                if temp[0] == "config":
                    update_config_with_token("config", "title", "version")
                elif temp[0] == "index":
                    update_with_token("index", "question")
                elif temp[0] == "categories":
                    update_with_token("categories", "key", "title")
                else:
                    update_with_token(*temp)
                input("Completed! Press enter to reset!")
            else:
                input("Press enter to reset!")
        except FileNotFoundError:
            print(f"{temp[0]} File Cannot be found!")
            input("Press enter to reset!")
        except KeyboardInterrupt:
            pass
