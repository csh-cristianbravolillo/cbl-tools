"""It implements a cylon config, which is a specialization of a config."""

import os
from datetime import datetime
from cbl_tools import config
import platform

class CylonConfig(config.config):

    def __init__(self, path:str) -> None:
        """Loads a path for the cylon folder.
        
        It adds two features over a usual config: it adds several variables to the default section,
        and it adds a 'last_modified' with the timestamp of the last modification to the config file.
        
        It also fixes the name of the file: files/cylon.ini, within path.
        """
        super().__init__(initpath = path, filename = "files/cylon.ini")
        self.register(self.__writedown2)
        self.set('base',    'home',     os.getenv('HOME'))
        self.set('local',   'system',   platform.system())
        self.set('local',   'node',     platform.node())
        self.set('local',   'machine',  platform.machine())
        self.set('local',   'sh',       os.getenv('SHELL'))

    def __writedown2(self) -> None:
        now = datetime.now()
        self.set('base', 'last_modified', now.strftime("%Y%m%d%H%M%S"))
