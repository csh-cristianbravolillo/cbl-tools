"""It implements a config file that saves itself.

The idea is: we want to use a config file for an application, which is a simple text file that contains pairs of values, in a similar fashion to an INI file. If the file
exists, it is used; if it doesn't, it is created. We use configparser for this."""

import os, atexit, configparser
from datetime import datetime
from configparser import ExtendedInterpolation

class config:

    path = None
    values = None

    def __init__(self, thispath:str = '~/.config', folder:str = 'cbl-config', filename:str = 'config.ini', create_folder:bool = True) -> None:
        """It creates a config file.

        To create the file, we specify its path (by default, '~/.config'), its containing folder (by default, 'cbl-config'; it might be empty), and its filename. Neither
        the path nor the filename could be empty. We can also specify whether an inexistent folder should be created with create_folder (by default, True).

        If the path doesn't exist or the filename is empty it raises an error. If the folder is not empty, it doesn't exist, and the create_folder argument is False, it
        also raises an error since we're being asked to use a folder that doesn't exist, and we're being told not to create it.

        If the folder is not empty, it doesn't exist, and create_folder is True, the folder is created.

        Finally, if a file exists in path/folder/filename, it is read and put into self.values. If it doesn't exist, it will be created in path/folder/filename when the
        program is terminated.
        """

        thispath = os.path.normpath(os.path.expanduser(thispath))

        if not os.path.isdir(thispath):
            raise OSError(1, "Path is either empty or not a path", thispath)

        if not filename:
            raise OSError(2, "Filename empty when creating object config")

        if folder and not os.path.exists(os.path.normpath(os.path.join(thispath, folder))):
            if not create_folder:
                raise OSError(3, "Folder not empty, it does not exist, and it should not be created.")
            
            os.mkdir(os.path.join(thispath, folder), 0o700)

        self.path = os.path.normpath(os.path.join(thispath, folder, filename))
        self.values = configparser.ConfigParser(delimiters=('='), comment_prefixes=('#'), interpolation = ExtendedInterpolation())

        # Si el archivo existe, hay que leerlo
        if os.path.exists(self.path):
            self.values.read(self.path)

        # Si no existe, hay que crear uno y dejarlo listo para recibir valores
        else:
            self.values.add_section('common')

        atexit.register(self._writedown)


    def get(self, section:str, key:str):
        if not section or not key or not section in self.values.sections():
            return None

        return self.values.get(section, key)


    def set(self, section:str, key:str, value:str):
        if not section or not key or not value or not section in self.values.sections():
            return False

        self.values.set(section, key, value)
        return True


    def add_section(self, section:str):
        if not section:
            return False

        self.values.add_section(section)
        return True


    def _writedown(self) -> None:
        now = datetime.now()
        self.values['common'] = {'last_modified': now.strftime("%Y%m%d%H%M%S")}

        with open(self.path, "w") as thisfile:
            self.values.write(thisfile)
