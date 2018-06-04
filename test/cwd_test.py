import unittest
import mock
import os
import tempfile
import shutil
import powerline_shell as p
import powerline_shell.segments.cwd as cwd_segment
from ..testing_utils import dict_side_effect_fn


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


class PlainModeTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("cwd", "mode"): "plain",
        })


    def test_home_directories(self):
        os.chdir(os.getenv("HOME"))
        segment = cwd_segment.Segment(self.powerline)
        segment.start()
        segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], ' ~ ')
