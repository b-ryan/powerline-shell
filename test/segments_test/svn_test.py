import tempfile
import unittest
import shutil
import mock
import sh
import powerline_shell.segments.svn as svn
from ..testing_utils import dict_side_effect_fn


class SvnTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("vcs", "show_symbol"): False,
        })

        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        # sh.svn("init", ".")

        self.segment = svn.Segment(self.powerline, {})

    def tearDown(self):
        shutil.rmtree(self.dirname)

    @mock.patch("powerline_shell.utils.get_PATH")
    def test_svn_not_installed(self, get_PATH):
        get_PATH.return_value = "" # so svn can't be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)
