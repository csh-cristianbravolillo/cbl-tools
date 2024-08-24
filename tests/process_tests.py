import unittest, os, sys
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from tools.process import process, git_remote, git_clone

class TestProcess(unittest.TestCase):

    tp = None

    def setUp(self):
        self.tp = process()
        return super().setUp()

    def tearDown(self):
        return super().tearDown()

    def test_ls(self):
        self.tp.run("ls")
        self.assertEqual(self.tp.command, "ls")
        self.assertEqual(self.tp.returncode, 0)
        self.assertTrue(self.tp.is_ok())
        self.assertTrue(self.tp.is_there_stdout())
        self.assertFalse(self.tp.is_there_stderr())


class TestGitRemote(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestGitClone(unittest.TestCase):

    def setUp(self):
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


if __name__ == '__main__':
    unittest.main()
