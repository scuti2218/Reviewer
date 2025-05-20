from os import mkdir, getcwd, listdir
from os.path import isdir, join as path_join, exists
import json
from ..models.Topic import Topic
from ..models.ModelData import ModelData
from ..models.Category import Category
from ..models.Question import Question
from typing import TypeVar

def check_dir(path: str) -> bool:
    return isdir(path)

def make_dir(path: str):
    mkdir(path)

def get_cur_dir() -> str:
    return getcwd()



def get_json_data(dir: str, filename: str, default_out = {}):
    filepath: str = path_join(dir, filename + ".json")
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except:
        return default_out

TModelData = TypeVar("TModelData", bound=ModelData)
def set_json_data(dir: str, filename: str, data: TModelData):
    filepath: str = path_join(dir, filename + ".json")
    with open(filepath, "w") as f:
        json.dump(data.get_json(), f, indent=4)



# CONFIG.JSON
def get_config(dir: str) -> Topic:
    return Topic(**get_json_data(dir, "config"), dir=dir)

def set_config(data: Topic):
    set_json_data(data.dir, "config", data)

def get_configs(path: str):
    result: list[Topic] = []
    i: int = 0
    for name in listdir(path):
        full_path = path_join(path, name)
        if isdir(full_path):
            if not exists(path_join(full_path, "config.json")):
                set_config(Topic(f"Sample{i}", "Sample Info", full_path))
            result.append(get_config(full_path))
            i += 1
    return result


# CATEGORY.JSON
def get_categories(dir: str):
    return [Category(**i) for i in get_json_data(dir, "categories", [])]


# INDEX.JSON
def get_questions(dir: str):
    return [Question(**i) for i in get_json_data(dir, "index", [])]