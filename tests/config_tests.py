import unittest, os, sys, tempfile, errno
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from cbl_tools import config, create_tempdir


class ConfigTests(unittest.TestCase):

    x = None

    def setUp(self) -> None:
        self.x = config.config(create_tempdir(True), 'zort.ini')
        return super().setUp()


    def test_trivial_exceptions(self):

        # Trivial exceptions
        try:
            config.config(initpath = "")
        except OSError as e:
            self.assertEqual(e.errno, errno.EINVAL, "Empty path should raise an OSError")

        try:
            config.config(filename = "")
        except OSError as e:
            self.assertEqual(e.errno, errno.EINVAL, "Empty filename should raise an OSError")


    def test_not_trivial_exceptions(self):
        # Opening an inexistent folder should raise an OSError:1
        try:
            config.config(initpath = os.path.join(tempfile.gettempdir(), "inexistent_folder_029837492837498"), create_folder=False)
        except FileNotFoundError as e:
            self.assertEqual(e.errno, errno.ENOENT, "An inexistent path with false create_folder should raise a FileNotFoundError")

        try:
            config.config(initpath = os.path.join(tempfile.gettempdir(), 'X', 'Y'))
        except FileNotFoundError as e:
            self.assertEqual(e.errno, errno.ENOENT, "More than two inexistent folders should raise a FileNotFoundError")

        try:
            config.config(initpath = '/root/my_own_folder')
        except PermissionError as e:
            self.assertEqual(e.errno, errno.EACCES, "Trying to create a folder within /root should raise a PermissionError!")


    def test_create_normal_config(self):

        # If asked to open an inexistent folder within a valid path, I should be able to create it.
        path = os.path.dirname(self.x.path)
        self.assertTrue(os.path.exists(path), f"Config should be able to create folder {path}")
        self.assertTrue(os.path.isdir(path), f"{path} should be a folder (it's not)")

        # Create a few values and then retrieve them
        self.assertFalse(self.x.values.has_section('blabla'), "An inexistent section ('blabla') exists")
        self.x.values.add_section('blabla')
        self.assertTrue(self.x.values.has_section('blabla'), "Cannot create section 'blabla'")
        self.x.values.set('blabla', 'a', '1')
        self.x.values.set('blabla', 'b', 'be')
        self.x.values.set('blabla', 'c', '3.141592653')
        self.x.values.set('blabla', 'switch', 'on')

        self.assertEqual(self.x.values.get('blabla', 'a'), '1', 'get(blabla:a) should be equal to \'1\'; it\'s not')
        self.assertEqual(self.x.values.getint('blabla', 'a'), 1, 'getint(blabla:a) should be equal to 1; it\'s not')
        self.assertEqual(self.x.values.get('blabla', 'b'), 'be', 'get(blabla:b) should be equal to \'be\'; it\'s not')
        self.assertEqual(self.x.values.getfloat('blabla', 'c'), 3.141592653, 'getint(blabla:c) should be equal to pi; it\'s not')
        self.assertTrue(self.x.values.getboolean('blabla', 'switch'), 'getint(blabla:switch) should be True; it\'s not')


    def test_interpolation(self):

        # Test interpolation
        self.x.values.add_section('blabla')
        self.assertTrue(self.x.values.has_section('blabla'), "Cannot create section 'blabla'")

        self.x.values.set('blabla', 'a', '1')
        self.x.values.set('blabla', 'b', 'be')
        self.x.values.set('blabla', 'c', '3.141592653')
        self.x.values.set('blabla', 'switch', 'on')

        self.x.values.add_section('naka')
        self.x.values.set('naka', 'valor1', 'a${blabla:a}c${blabla:c}zzz${blabla:b}')

        self.assertTrue(self.x.values.has_section('naka'), "Cannot create section 'naka'")
        self.assertEqual(self.x.values.get('naka', 'valor1'), 'a1c3.141592653zzzbe')
        self.assertEqual(self.x.values.getboolean('blabla', 'switch'), True, "")


    def test_abusive_conf(self):
        try:
            self.x = config.config(os.getenv("HOME"), "../another_user")
        except ValueError:
            pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
