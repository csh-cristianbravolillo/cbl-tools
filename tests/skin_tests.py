import unittest, os, sys, random
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from datetime import datetime
from tools import config, create_tempdir


class SkinTests(unittest.TestCase):

    path = None
    parser = None

    def setUp(self) -> None:
        self.path = create_tempdir(True)
        with open(self.path, "w") as fl:
            fl.write("""
[local]
id = sharon
description = Perfil personal, ubuntu, con bash.
os = Ubuntu 22.04
path = ${home}/lib
sh = /bin/bash

[remote]
server = cbravo@kind.cl
path = ~/git/data/sharon.git

[symlinks]
.bashrc = files/bashrc
.bash_logout = files/bash_logout
.joerc = files/joerc

[apt]
required = joe gimp gimp-data-extras htop curl
graphs = graphviz graphviz-doc

[repo]
server = cbravo@kind.cl
prefix = ~/git
""")
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_info(self) -> None:
        pass

    def test_get_symlinks(self) -> None:
        pass

    def test_get_copiesfiles(self) -> None:
        pass

    def test_get_apt(self) -> None:
        pass

    def test_get_repo_sections(self) -> None:
        pass

    def test_get_repo_names(self) -> None:
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
