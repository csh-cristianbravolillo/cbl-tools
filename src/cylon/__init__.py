__all__ = ["cprint", "get_remote_folders"]

import re
import json
from colorama import Fore, Style
from tools.process import process

#> -----------------------------------------------------------------------------------
def cprint(arg:str, return_it:bool = False, end:str = "\n"):
    """Prints colored output.
    
    This method prints colored output. The argument has to specify which substrings
    should be colored through the following format:
    
    "... bla bla bla [r|this text will be in red] and [b|this one will go in blue]..."

    Allowed colors are r (red), g (green), b (blue) and y (yellow)."""

    arg = re.sub(r"\[R\|([^]]+?)\]", Fore.RED + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[G\|([^]]+?)\]", Fore.GREEN + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[B\|([^]]+?)\]", Fore.BLUE + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[Y\|([^]]+?)\]", Fore.YELLOW + Style.BRIGHT + r"\1" + Style.RESET_ALL, arg)

    arg = re.sub(r"\[r\|([^]]+?)\]", Fore.RED + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[g\|([^]]+?)\]", Fore.GREEN + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[b\|([^]]+?)\]", Fore.BLUE + r"\1" + Style.RESET_ALL, arg)
    arg = re.sub(r"\[y\|([^]]+?)\]", Fore.YELLOW + r"\1" + Style.RESET_ALL, arg)

    if return_it:
        return arg
    else:
        print(arg, end=end)
        return None

#> -----------------------------------------------------------------------------------
def get_remote_folders(rmt_server:str, rmt_path:str, rmt_file:str = 'cylon.json') -> dict:
    """
    It gets all remote folders as a list, using the cylon convention.
    
    If rmt_server or rmt_path are empty, it returns an empty list.
    """

    if not rmt_server or not rmt_path:
        raise ValueError("rmt_server and rmt_path must be non-empty strings")

    tst = process()
    tst.run(f"ssh {rmt_server} cat '{rmt_path}/{rmt_file}'")
    if not tst.is_ok():
        raise OSError(f"Cannot run ssh {rmt_server} cat '{rmt_path}/{rmt_file}'")

    content = "\n".join(tst.stdout)
    return json.loads(content)
