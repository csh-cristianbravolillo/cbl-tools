"""It implements a copy of a cylon: a git package, retrieved from a source.

A skin is a simply a set of folders and files to be put at the root of a user account in a server, with a set
of instructions about what to do to deploy. For example, I would like to copy most files, and then create symbolic
links to these files. Sometimes I would like to create certain files out of some content. All of these instructions
are contained within a config file, that is implemented through cbl_tools/config.

This class has no CLI interaction with the user.
"""

import os.path
from datetime import datetime
from tools import norm_path
from tools.config import config
from tools.process import process
from tools.git import git

class skin(config):

    def __init__(self, path:str, touch_inifile:bool = False) -> None:
        """It loads a skin located in path. Path should be the root of the cylon folder,
        not the files/ folder which contains the ini file.

        Loading a skin means to load a local folder, already downloaded from a source, and
        reading the config file in order to check whether this copy is in good condition.
        """
        super().__init__(initpath=os.path.join(path, 'files/cylon.ini'), create_folder=False)

        # Seteamos valores importantes en cylon.ini
        self.set('local', 'home', os.getenv('HOME'))
        self.set('local', 'sh', os.getenv('SHELL'))
        self._set_value('uname -o', 'os')
        self._set_value('uname -n', 'node')
        self._set_value('uname -p', 'arch')

        # Crea un objeto git y lo asocia a una variable interna
        self.gitobj = git(self.get_dirname())
        self.set('local', 'path', self.gitobj.local_path)

        # Finalmente, registra un método que actualiza el valor de "last_modified"
        if touch_inifile:
            self.register(self._set_postvalue)

    def _set_value(self, com:str, label:str) -> None:
        p = process()
        p.run(com)
        if not p.is_ok() or not p.is_there_stdout():
            raise OSError(f"Cannot run {com}")
        self.set('local', label, p.stdout[0])

    def _set_postvalue(self) -> None:
        self.set('local', 'last_modified', datetime.now().strftime('%Y%m%d%H%M%S'))

    def fix_links(self, color:bool = True) -> list:
        """Checks all links in section "symlinks", and fixes them if they are not currently set.

        The idea is: the section "symlinks" contains a set of pairs. The key is a symlink in the root of the user ("a link"),
        and the value is a file within the "path" of the cylon folder ("the target"). This method checks whether the target
        exists (if not, it complains), whether the link exists and is not a link (if not, it complains), and whether the link
        indeed points to the target (if not, it corrects the link so it points to the target).
        """

        results = []
        for key in self.options("symlinks"):
            link = os.path.join(self.get("local", "home"), key)
            target = norm_path(self.get('local', 'path'), self.get("symlinks", key))
            result = {'link': link, 'target': target, 'OK':False}

            if not os.path.exists(target):
                result['OK'] = False
                if color:
                    result['msg'] = f"[r|Target {target} in config file does not exist]. Please check."
                else:
                    result['msg'] = f"Target {target} in config file does not exist. Please check."

            elif os.path.exists(link) and not os.path.islink(link):
                result['OK'] = False
                if color:
                    result['msg'] = f"[r|Link {link} mentioned in config file exists, and is not a link]. Please check."
                else:
                    result['msg'] = f"Link {link} mentioned in config file exists, and is not a link. Please check."

            elif os.path.lexists(link) and os.path.realpath(link) != target:
                os.remove(link)
                result['OK'] = True
                if color:
                    result['msg'] = f"[r|{link} points to {os.path.realpath(link)} instead of {target}], so fixing it..."
                else:
                    result['msg'] = f"{link} points to {os.path.realpath(link)} instead of {target}, so fixing it..."

            elif not os.path.exists(link):
                os.symlink(target, link)
                result['OK'] = True
                if color:
                    result['msg'] = f"[y|Creating {link} -> {target}]"
                else:
                    result['msg'] = f"Creating {link} -> {target}"
            else:
                result['OK'] = None
                result['msg'] = "No change"

            results.append(result)
        return results

    def fix_xdg_dirs(self) -> dict[str, list[str]]:
        """Checks all user dirs, based on the xdg group. Returns a dict with two arrays: one for all stuff that went
        well, and another for all that didn't.
        
        The idea is: the group "xdg" contains the user dirs, as defined by the unix manual "man xdg-user-dirs-update".
        This method cycles through all keys in that section, and points them to the correct user dir. If the special
        keyword "None" is used, that means that we don't want to have a dir for that, so that key is set to /dev/null.
        """

        p = process()
        results = {
            "Yes": [],
            "No": []
        }

        for key in self.options("xdg"):

            if self.get("xdg", key) == "None":
                p.run(f"xdg-user-dirs-update --set {key} /dev/null")
                if p.is_ok():
                    results['Yes'].append(f"xdg:{key} set to None")
                else:
                    results['No'].append(f"xdg:{key} does not exist!")
                continue

            val = os.path.join(self.get("local", "path"), self.get("xdg", key))

            if not os.path.exists(val):
                results['No'].append(f"xdg:{key} points to non-existent file/folder!")
            else:
                p.run(f"xdg-user-dirs-update --set {key} {val}")
                if p.is_ok():
                    results['Yes'].append(f"xdg:{key} set to {val}")
                else:
                    results['No'].append(f"xdg:{key} does not exist!")

        return results
