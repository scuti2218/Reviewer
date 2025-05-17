import os
from .Data import get_data

get_defaults: list[str] = lambda path, iter : [f"Untitled {iter}", f"Reviewer for Untitled {iter}", path]
configname: str = "config.txt"
indexname: str = "index.json"
get_fullpath: str = lambda *args : os.path.join(*args)

def fix_config(path: str, iter: int = 0) -> list[str]:
    fullpath: str = get_fullpath(path, configname)
    defaults : list[str] = get_defaults(path, iter)
    rows: list[str] = defaults[:]
    
    if not os.path.exists(fullpath):
        with open(fullpath, 'w') as f:
            f.write(f"{defaults[0]}\n{defaults[1]}\n")
    else:
        with open(fullpath, 'r') as f:
            lines = f.readlines()
            
        lines = [line.strip() for line in lines]
        definer = lambda idx: lines[idx] if (len(lines) >= idx + 1) and (lines[idx].strip() != "") else defaults[idx]
        rows[0] = definer(0)
        rows[1] = definer(1)
        
        with open(fullpath, 'w') as f:
            f.write(f"{rows[0]}\n{rows[1]}\n")
            
    return rows

def evaluate_config(path: str) -> list[dict[str, str]]:
    fullpath: str = get_fullpath(path, indexname)
    return get_data(fullpath)