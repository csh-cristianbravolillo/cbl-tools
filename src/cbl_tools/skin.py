"""It implements a copy of a cylon: a git package, retrieved from a source.

A skin is a simply a set of folders and files to be put at the root of a user account in a server, with a set
of instructions about what to do to deploy. For example, I would like to copy most files, and then create symbolic
links to these files. Sometimes I would like to create certain files out of some content. All of these instructions
are contained within a config file, that is implemented through cbl_tools/config.

This class has no CLI interaction with the user. Most methods use a 'result' to contain information about (Alas!)
the result of the execution.
"""

from cbl_tools import cylon_config

class skin:

    config = None

    def __init__(self, path:str) -> None:
        """It loads a skin located in path. Path should be the root of the cylon folder,
        not the files/ folder which contains the ini file.

        Loading a skin means to load a local folder, already downloaded from a source, and
        reading the config file in order to check whether this copy is in good condition.
        """
        self.config = cylon_config.CylonConfig(path)

    def info(self) -> str:
        """It returns information about itself."""
        pass


    def pull(self) -> bool:
        """It checks for changes in the remote, and download changes.

        Since a skin is a git repository, one may do a git pull to check if there are any
        changes. This should be done initially, in order to bring everything to the same
        state.
        """
        pass


    def push(self) -> bool:
        """It commits all changes and push them to the remote.

        This is the logical opposite of pull, obviously.
        """
        pass


    def get_symlinks(self) -> dict:
        """It returns all the pairs of symlinks to files that would be enforced if asked to."""
        return self.config.values.items('symlinks')


    def do_symlinks(self) -> bool:
        """It checks the links in the section symlinks in the config.ini."""
        pass


    def get_copiedfiles(self) -> bool:
        """It returns all files within the section copied.files."""
        return self.config.values.items('copied.files')


    def do_copiedfiles(self) -> bool:
        """It copies files in the section copied.files."""
        pass


    def get_apt(self) -> dict:
        """It returns all groups of apt packages within the corresponding section."""
        return self.config.values.items('apt')


    def do_apt(self, cat:str = 'required') -> bool:
        """It checks the apt section looking for groups of packages, depending on 'cat':
        * If 'required' (default), it only checks whether the packages in the required
          key are installed.
        * If 'optional', it checks for all packages but the required.
        * If 'all', it checks for all packages.
        """
        pass
