import tempfile
import unittest
import shutil
from contextlib import ExitStack

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

        self.upstream_dir = tempfile.mkdtemp()
        self.checkout_dir = tempfile.mkdtemp()
        sh.svnadmin("create", self.upstream_dir)
        sh.svn("checkout", f"file://{self.upstream_dir}", self.checkout_dir)

        self.segment = svn.Segment(self.powerline, {})

        with ExitStack() as stack:
            self._resource = stack.enter_context(sh.pushd(self.checkout_dir))
            self.addCleanup(stack.pop_all().close)

    def tearDown(self):
        shutil.rmtree(self.upstream_dir)
        shutil.rmtree(self.checkout_dir)

    @mock.patch("powerline_shell.utils.get_PATH")
    def test_svn_not_installed(self, get_PATH):
        get_PATH.return_value = ""  # so svn can't be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)
