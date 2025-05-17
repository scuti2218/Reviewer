from pathlib import Path
from typing import Callable

function = Callable[[str, int], list[str]]

def check_dir(path: str) -> bool:
    return Path("data").is_dir()

def get_cur_dir() -> Path:
    return Path.cwd()

def get_sub_folders(path: str, func: function = None) -> list[list[Path]]:
    data_path = Path(path)
    result: list[Path] = []
    for i, folder in enumerate(data_path.iterdir()):
        if folder.is_dir():
            result.append([func(folder, i), [folder]][func == None])
    return result