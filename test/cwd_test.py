import unittest
import mock
import os
import tempfile
import shutil
import powerline_shell as p


class CwdTest(unittest.TestCase):

    def setUp(self):
        self.dirname = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dirname)

    @mock.patch('os.getenv')
    @mock.patch('powerline_shell.warn')
    def test_normal(self, warn, getenv):
        getenv.return_value = self.dirname
        self.assertEqual(p.get_valid_cwd(), self.dirname)
        self.assertEqual(warn.call_count, 0)

    @mock.patch('os.getenv')
    @mock.patch('powerline_shell.warn')
    def test_nonexistent_warns(self, warn, getenv):
        subdir = os.path.join(self.dirname, 'subdir')
        getenv.return_value = subdir
        self.assertEqual(p.get_valid_cwd(), subdir)
        self.assertEqual(warn.call_count, 1)

    @mock.patch('os.getenv')
    @mock.patch('powerline_shell.warn')
    def test_falls_back_to_getcwd(self, warn, getenv):
        getenv.return_value = None
        os.chdir(self.dirname)
        self.assertEqual(p.get_valid_cwd(), self.dirname)
        self.assertEqual(warn.call_count, 0)

    @mock.patch('os.getenv')
    @mock.patch('powerline_shell.warn')
    def test_nonexistent_getcwd_warns(self, warn, getenv):
        subdir = os.path.join(self.dirname, 'subdir')
        getenv.return_value = None

        os.mkdir(subdir)
        os.chdir(subdir)
        os.rmdir(subdir)

        with self.assertRaises(SystemExit) as e:
            p.get_valid_cwd()

        self.assertEqual(warn.call_count, 1)
