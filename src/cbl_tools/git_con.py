import re
import os.path
from cbl_tools import process

class git_remote(process):
    folder = None
    url_user = None
    url_domain = None
    url_path = None
    remote = None

    def __init__(self, folder:str) -> None:
        if not os.path.exists(folder) or not os.path.isdir(folder):
            print(f"{folder} is not a folder.")
            exit(1)

        self.folder = folder

        self.run(f"git -C {self.folder} remote -v")
        res = {}

        for line in self.search("^(\w+)\t(\S+)\s\((fetch|push)\)"):
            if not line[0] in res:
                res[line[0]] = {}
            res[line[0]][line[2]] = self._url_split(line[1])
        self.remote = res

    def _url_split(self, arg:str) -> list:
        tst = re.search(r"([^@]+?)@([^:]+?):(.+)", arg)

        if tst:
            self.url_user = tst.group(1)
            self.url_domain = tst.group(2)
            self.url_path = tst.group(3)
            if self.url_path.startswith("~" + self.url_user):
                self.url_path = '~' + self.url_path[len(self.url_user)+1:]
            return [self.url_user, self.url_domain, self.url_path]
        else:
            return None

    def get_server(self) -> str:
        if not self.url_user or not self.url_domain:
            return None
        else:
            return self.url_user + '@' + self.url_domain

    def does_path_start_with(self, path:str) -> bool:
        if not path:
            return False
        return self.url_path.startswith(path)

class git_clone(process):
    url = None
    target = None

    def __init__(self, url:str, target:str) -> None:
        self.url = url
        self.target = target
        self.run(f"git clone {self.url} {self.target}", True)
