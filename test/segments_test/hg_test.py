import unittest
import mock
import tempfile
import shutil
import sh
import powerline_shell.segments.hg as hg


class HgTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()

        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        sh.hg("init", ".")

        self.segment = hg.Segment(self.powerline)

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def _add_and_commit(self, filename):
        sh.touch(filename)
        sh.hg("add", filename)
        sh.hg("commit", "-m", "add file " + filename)

    def _checkout_new_branch(self, branch):
        sh.hg("branch", branch)

    @mock.patch("powerline_shell.segments.hg.get_PATH")
    def test_hg_not_installed(self, get_PATH):
        get_PATH.return_value = "" # so hg can"t be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_non_hg_directory(self):
        shutil.rmtree(".hg")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_standard(self):
        self._add_and_commit("foo")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], " default ")
