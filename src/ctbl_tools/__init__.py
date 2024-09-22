__all__ = ["create_tempdir", "norm_path", "is_file_readable"]

import os.path
import random
import tempfile

#> -----------------------------------------------------------------------------------
def create_tempdir(mkdir:bool = False) -> str:
    random.seed()
 
    p = tempfile.gettempdir()
    while True:
        fld = "cbl-config-" + str(random.randint(100000, 999999))
        if not os.path.exists(os.path.join(p, fld)):
            break

    thispath = os.path.join(p, fld)

    if mkdir:
        os.mkdir(thispath)

    return thispath

#> -----------------------------------------------------------------------------------
def norm_path(*args) -> str:
    if len(args) == 0 or not args[0]:
        return None
    else:
        return os.path.normpath(os.path.expanduser(os.path.join(*args)))

#> -----------------------------------------------------------------------------------
def is_file_readable(file:str) -> bool:
    return file and os.path.exists(file) and os.path.isfile(file) and os.access(file, os.R_OK)
