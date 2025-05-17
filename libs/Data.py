import json

def get_data(filepath: str) -> list[dict[str, str]]:
    data : list[dict[str, str]] = []
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data