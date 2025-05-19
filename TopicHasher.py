import os
import json
import hashlib

def get_json(filename: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, filename + ".json")
    with open(config_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def set_json(filename: str, data: dict):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, filename + ".json")
    with open(config_path, 'w') as f:
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
    make_token(filename, **kwargs)
    set_json(filename, kwargs)
    
def update_index_with_token(filename: str, *args: str):
    args = get_json(filename)
    result = [make_token(f"{filename} {i}", **kwargs) for i, kwargs in enumerate(args)]
    set_json(filename, result)

if __name__ == "__main__":
    # update_config_with_token("config", "title", "version")
    # update_index_with_token("index", "question")
    pass
