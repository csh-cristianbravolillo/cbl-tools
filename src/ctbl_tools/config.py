"""It implements a config file that saves itself.

The idea is: we want to use a config file for an application, which is a simple text file that contains pairs of values, in a similar fashion to an INI file. If the file
exists, it is used; if it doesn't, it is created. We use configparser for this.

This class has just one public variable: path, which is the absolute path formed by initpath and filename, arguments to the constructor of the class.

_values is the configparser where one will find all the values that were read, if present. I'm not sure if I should make it public though.
"""

import os
import atexit
import errno
import configparser
from configparser import ExtendedInterpolation
from ctbl_tools.exceptions import *

class config(configparser.ConfigParser):

    path = None

    def __init__(self, initpath:str = '~/.config/config.ini', create_folder:bool = True, default_section:str = 'default') -> None:
        """It creates a config file.

        To create the file, we specify its path (by default, '~/.config/config.ini'). The last folder within the path may not exist,
        in which case it will be created. Neither initpath nor filename could be empty (an OSError will be raised). We can also specify whether an inexistent folder
        should be created with create_folder (by default, True).

        If thispath is empty it raises an error. If the last portion of thispath doesn't exist and create_folder is False, it raises a FileNotFoundError
        since we're being asked to use a folder that doesn't exist, and we're being told not to create it.

        Finally, if a file exists in initpath, it's read and put into self.values. If it doesn't exist, it will be created when the
        program is terminated, or when flush() is invoked.
        """

        if not initpath:
            raise EmptyValueError("initpath must not be empty")

        folder,filename = os.path.split(os.path.normpath(os.path.expanduser(initpath)))

        if not os.path.exists(folder) and not create_folder:
            raise FileNotFoundError(errno.ENOENT, "path does not exist and create_folder is False", folder)

        try:
            if not os.path.exists(folder) and create_folder:
                os.mkdir(folder, 0o700)

        except FileNotFoundError:
            raise FileNotFoundError(errno.ENOENT, "one or more of the parent folders in thispath don't exist, and won't be created", folder)

        except PermissionError:
            raise PermissionError(errno.EACCES, "cannot create folder: permission denied", folder)

        self.path = os.path.join(folder, filename)

        if os.path.exists(self.path) and not os.path.isfile(self.path):
            raise NotAFileError("last part of initpath already exists, and it's not a file")

        # If path goes out of normalized init_path, the user may be abusing this class, so we ban it
        if os.path.commonpath([self.path, initpath]) != initpath:
            raise ValueError(f"filename ({filename}) is relative to initpath ({initpath}), and it should be within it, but it's not ({self.path})")

        super().__init__(delimiters=('='), comment_prefixes=('#'), interpolation=ExtendedInterpolation(), default_section=default_section)

        # Si el archivo existe, hay que leerlo
        if os.path.exists(self.path):
            super().read(self.path)

        self.register(self._flush)

    def __str__(self) -> str:
        return f"<{__class__.__name__} object; path={self.path}>"

    def _flush(self) -> None:
        f = open(self.path, "w")
        self.write(f)
        f.close()

    def get_dirname(self) -> str:
        if self.path:
            return os.path.dirname(self.path)
        return None

    def get_filename(self) -> str:
        if self.path:
            return os.path.basename(self.path)
        return None

    def register(self, func:callable) -> None:
        atexit.register(func)
