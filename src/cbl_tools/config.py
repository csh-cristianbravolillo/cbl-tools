"""It implements a config file that saves itself.

The idea is: we want to use a config file for an application, which is a simple text file that contains pairs of values, in a similar fashion to an INI file. If the file
exists, it is used; if it doesn't, it is created. We use configparser for this.

This class has two variables:

* path: it's the absolute path formed by initpath and filename, arguments to the constructor of the class.
* values: it's the configparser where one will find all the values that were read, if present.

We may add sections and values to the self.values variable, and when the whole program exits, it will save those values into the file pointed to by self.path.
"""

import os
import atexit
import errno
import configparser
from configparser import ExtendedInterpolation


class config:

    path = None
    values = None

    def __init__(self, initpath:str = '~/.config', filename:str = 'config.ini', create_folder:bool = True, default_section:str = 'default') -> None:
        """It creates a config file.

        To create the file, we specify its path (by default, '~/.config'), and its filename (by default, 'config.ini'). The last folder within the path may not exist,
        in which case it will be created. Neither initpath nor filename could be empty (an OSError will be raised). We can also specify whether an inexistent folder
        should be created with create_folder (by default, True).

        If thispath or filename are empty it raises an error. If the last portion of thispath doesn't exist and create_folder is False, it raises a FileNotFoundError
        since we're being asked to use a folder that doesn't exist, and we're being told not to create it.

        Finally, if a file exists in path/folder/filename, it is read and put into self.values. If it doesn't exist, it will be created in path/folder/filename when the
        program is terminated.
        """

        initpath = os.path.normpath(os.path.expanduser(initpath))

        if initpath == ".":
            raise OSError(errno.EINVAL, "path cannot be empty")

        if not filename:
            raise OSError(errno.EINVAL, "filename cannot be empty")

        if not os.path.exists(initpath) and not create_folder:
            raise FileNotFoundError(errno.ENOENT, "path does not exist and create_folder is False", initpath)

        try:
            if not os.path.exists(initpath) and create_folder:
                os.mkdir(initpath, 0o700)
        except FileNotFoundError:
            raise FileNotFoundError(errno.ENOENT, "one or more of the parent folders in thispath don't exist, and won't be created", initpath)
        except PermissionError:
            raise PermissionError(errno.EACCES, "cannot create such folder: permission denied", initpath)

        self.path = os.path.normpath(os.path.join(initpath, filename))

        # If path goes out of normalized init_path, the user may be abusing this class, so we ban it
        if os.path.commonpath([self.path, initpath]) != initpath:
            raise ValueError(f"filename ({filename}) is relative to initpath ({initpath}), and it should be within it, but it's not ({self.path})")

        self.values = configparser.ConfigParser(delimiters=('='), comment_prefixes=('#'), interpolation = ExtendedInterpolation())
        self.values.default_section = default_section

        # Si el archivo existe, hay que leerlo
        if os.path.exists(self.path):
            self.values.read(self.path)

        self.register(self.__writedown)


    def register(self, func:callable) -> None:
        atexit.register(func)


    def __writedown(self) -> None:
        with open(self.path, "w") as thisfile:
            self.values.write(thisfile)


    def set(self, section:str, var:str, val:str) -> None:
        if not var or not val:
            raise ValueError("set() was called without a var or a val")
        self.values.set(section, var, val)


    def get(self, section:str, var:str = '') -> str:
        if not section:
            raise ValueError("get() was called without a section or a var")

        if var:
            return self.values.get(section, var)
        else:
            return self.values.get(section.split(":")[0], section.split(":")[1])


    def sections(self) -> list:
        return self.values.sections()


    def section(self, section:str) -> dict:
        if not section:
            raise ValueError("items() was called without a section")

        lst = {}
        for pair in self.values.items(section):
            lst[pair[0]] = pair[1]

        return lst


    def keys(self, section:str) -> list:
        if not section:
            raise ValueError("keys() was called without a section")
        return self.values.options(section)
