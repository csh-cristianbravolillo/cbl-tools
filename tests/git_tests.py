import unittest, os, sys
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from ctbl_tools import create_tempdir
from ctbl_tools.git import git
from ctbl_tools.git import git_clone
from ctbl_tools.git import is_git_url
from ctbl_tools.git import is_git_folder
from ctbl_tools.process import process

class TestGitRemote(unittest.TestCase):

    tmp_git_folder = None

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_is_git_url(self):

        # Type of URL #1
        self.assertTrue(is_git_url("ssh://johndoe@somewhere.com:9000/csh-cristianbravolillo/ctbl_tools.git"), "git url type #1 should have been recognized; it was not")
        self.assertTrue(is_git_url("ssh://somewhere.com:9000/csh-cristianbravolillo/ctbl_tools.git"), "git url type #1 should have been recognized; it was not")
        self.assertTrue(is_git_url("ssh://johndoe@somewhere.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #1 should have been recognized; it was not")
        self.assertTrue(is_git_url("ssh://somewhere.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #1 should have been recognized; it was not")

        # Type of URL #2
        self.assertTrue(is_git_url("http://github.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #3 should have been recognized; it was not")
        self.assertTrue(is_git_url("https://github.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #3 should have been recognized; it was not")
        self.assertTrue(is_git_url("ftp://github.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #3 should have been recognized; it was not")
        self.assertTrue(is_git_url("ftps://github.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #3 should have been recognized; it was not")
        self.assertTrue(is_git_url("git://github.com/csh-cristianbravolillo/ctbl_tools.git"), "git url type #3 should have been recognized; it was not")

        # Type of URL #3
        self.assertTrue(is_git_url("git@github.com:csh-cristianbravolillo/ctbl_tools.git"), "git url type #1 should have been recognized; it was not")

    def test_git_clone_is_git_folder(self):

        # We clone a project into /tmp
        tmpfolder = create_tempdir(False)
        self.assertTrue(git_clone("https://github.com/arrow-py/arrow.git", tmpfolder), "Git clone didn't work")

        # We check if it is actually a git folder
        self.assertTrue(is_git_folder(tmpfolder), "is_git_folder didn't recognize a git folder")

        self.tmp_git_folder = tmpfolder

if __name__ == '__main__':
    unittest.main(verbosity=2)
