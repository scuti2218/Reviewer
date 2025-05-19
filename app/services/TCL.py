import os
import sys
import pathlib

def check_tcl_path():
    # Find the base directory of the current Python installation
    base_dir = pathlib.Path(sys.executable).parent

    # Common Tcl directory path relative to Python installation
    possible_tcl_path = base_dir / "tcl" / "tcl8.6"

    if possible_tcl_path.exists():
        os.environ['TCL_LIBRARY'] = str(possible_tcl_path)
        return True
    else:
        print("Warning: Could not locate tcl8.6 directory.")
        return False