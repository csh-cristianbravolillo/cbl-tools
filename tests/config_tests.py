import unittest, os, sys, random, tempfile
sys.path.append(os.path.normpath(os.path.join(os.path.abspath(sys.path[0]), '../src')))
from datetime import datetime
from cbl_tools import cbl_config


class TestCommon(unittest.TestCase):

    def test_exceptions(self):
        # Opening an inexistent folder should raise an OSError:1
        try:
            cbl_config.config(thispath = '/inexistent')
        except OSError as e:
            self.assertEqual(e.errno, 1, "Config should raise an OSError:1 when opening an inexistent path")

        # Giving an empty filename should raise an OSError:2
        try:
            cbl_config.config(filename = '')
        except OSError as e:
            self.assertEqual(e.errno, 2, "Config should raise an OSError:2 when given an empty filename")

        # Asking me to open an inexistent folder and not letting me create it raises an OSError:3
        try:
            cbl_config.config(folder = 'narciso', create_folder = False)
        except OSError as e:
            self.assertEqual(e.errno, 3, "Config should raise an OSError:3 when given an inexistent folder but not allowing to create it")


    def test_create_normal_folder(self):
        random.seed()
        x = cbl_config.config(tempfile.gettempdir(), self._create_tempdir())

        # If asked to open an inexistent folder within a valid path, I should be able to create it.
        path = os.path.dirname(x.path)
        self.assertTrue(os.path.exists(path), f"Config should be able to create folder {path}")
        self.assertTrue(os.path.isdir(path), f"{path} should be a folder (it's not)")

        # Create a few values and then retrieve them
        self.assertTrue(x.add_section('blabla'), "Cannot create section 'blabla'")
        self.assertTrue(x.set('blabla', 'a', '1'))
        self.assertTrue(x.set('blabla', 'b', '2'))
        self.assertTrue(x.set('blabla', 'c', '3'))
        self.assertEqual(x.get('blabla', 'a'), '1')
        self.assertEqual(x.get('blabla', 'b'), '2')
        self.assertEqual(x.get('blabla', 'c'), '3')

        # Test interpolation
        self.assertTrue(x.add_section('naka'), "Cannot create section 'naka'")
        self.assertTrue(x.set('naka', 'valor1', 'a${blabla:a}c${blabla:c}zzz${blabla:b}'))
        self.assertEqual(x.get('naka', 'valor1'), 'a1c3zzz2')


    def _create_tempdir(self):
        while True:
            tmpname = "cbl-config-" + str(random.randint(100000, 999999))
            if not os.path.exists(os.path.join(tempfile.gettempdir(), tmpname)):
                break
        return tmpname


if __name__ == '__main__':
    unittest.main()
