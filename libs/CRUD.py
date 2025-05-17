from pathlib import Path

def check_dir(path: str) -> bool:
    return Path(path).is_dir()

def make_dir(path: str):
    Path(path).mkdir()

def get_cur_dir() -> Path:
    return Path.cwd()