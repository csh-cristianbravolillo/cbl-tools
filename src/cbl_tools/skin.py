"""It implements a copy of a cylon: a git package, retrieved from a source.

A skin is a simply a set of folders and files to be put at the root of a user account in a server, with a set
of instructions about what to do to deploy. For example, I would like to copy most files, and then create symbolic
links to these files. Sometimes I would like to create certain files out of some content. All of these instructions
are contained within a config file, that is implemented through cbl_tools/config.

Most methods receive a boolean 'doit' which is by default false. This class has no direct interaction with the user.
If doit is false, no action will be done, and 'result' will contain information about what would have been done if
doit were true.
"""

import os
from cbl_tools import config, result

class skin:

    _events = None

    def __init__(self, event:str) -> None:
        """It loads a skin.

        Loading a skin means to load a local folder, already downloaded from a source, and
        reading the config file in order to check whether this copy is in good condition.

        The event could be either login, in, or logout. It represents three moments in which
        checks could be done. If none of those, it raises an error.

        Each method is responsible for adding itself to one or more of these events in the
        self.event variable. All callables inserted in one of these values will be executed.
        """
        self._events = {
            'login': [
                self.info,
                self.
            ],
            'in': [

            ],
            'logout': [

            ]
        }

    # def _addto(self, func:callable, where:str) -> bool:
    #     """It allows a method to add itself to login, in, or logout events."""
    #     if not where in self.events or func in self.events[where]:
    #         return False

    #     self.events[where].append(func)
    #     return True

    def info(self) -> result:
        """It returns information about itself."""
        pass

    def pull(self) -> result:
        """It checks for changes in the remote, and download changes.

        Since a skin is a git repository, one may do a git pull to check if there are any
        changes. This should be done initially, in order to bring everything to the same
        state.
        """
        pass

    def push(self) -> result:
        """It commits all changes and push them to the remote.

        This is the logical opposite of pull, obviously.
        """
        pass

    def get_symlinks(self) -> dict:
        """It returns all the pairs of symlinks to files that would be enforced if asked to."""
        pass

    def do_symlinks(self) -> result:
        """It checks the links in the section symlinks in the config.ini."""
        pass

    def get_copiedfiles(self) -> dict:
        """It returns all files within the section copied.files."""
        pass

    def do_copiedfiles(self) -> result:
        """It copies files in the section copied.files."""
        pass

    def get_apt(self) -> dict:
        """It returns all groups of apt packages within the corresponding section."""
        pass

    def do_apt(self, cat:str = 'required') -> result:
        """It checks the apt section looking for groups of packages, depending on 'cat':
        * If 'required' (default), it only checks whether the packages in the required
          key are installed.
        * If 'optional', it checks for all packages but the required.
        * If 'all', it checks for all packages.
        """
        pass

    def get_repo_sections(self) -> list:
        """It returns all repo sections."""
        pass

    def get_repo_names(self, section:str) -> dict:
        """It returns all repo names within a section."""
        pass

    def do_repo(self, section:str, name:str) -> result:
        """It downloads a repo into a folder."""
        pass
