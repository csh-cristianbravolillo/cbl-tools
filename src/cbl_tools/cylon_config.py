"""It implements a cylon config, which is a specialization of a config."""

import os
from datetime import datetime
from cbl_tools import config

class CylonConfig(config.config):

    def __init__(self, path:str) -> None:
        """Loads a path for the cylon folder.
        
        It adds two features over a usual config: it adds 'home' as a variable to the default section
        with the user folder value, and it adds a 'last_modified' with the timestamp of the last
        modification to the config file."""
        super().__init__(initpath = path, filename = "files/cylon.ini")
        self.values.set(self.values.default_section, 'home', os.getenv('HOME'))
        self.register(self.__writedown2)


    def __writedown2(self) -> None:
        now = datetime.now()
        self.values.set(self.values.default_section, 'last_modified', now.strftime("%Y%m%d%H%M%S"))
