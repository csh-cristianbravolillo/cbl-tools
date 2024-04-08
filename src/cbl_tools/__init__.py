__all__ = ["create_tempdir"]

import os, random, tempfile

def create_tempdir(mkdir:bool = False):
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
