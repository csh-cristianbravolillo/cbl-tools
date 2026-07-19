import unittest, os, sys
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from cylon import get_remote_folders


class GeneralTests(unittest.TestCase):

    def setUp(self) -> None:
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_remote_folders_list(self):

        lst = get_remote_folders("cbravo@kind.cl", "~/git/data")

        for tmp in lst:
            self.assertTrue(tmp.endswith(".git"))

if __name__ == '__main__':
    unittest.main(verbosity=2)
