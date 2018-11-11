import unittest
import mock
import tempfile
import shutil
import sh
import powerline_shell.segments.fossil as fossil
from powerline_shell.utils import RepoStats
from ..testing_utils import dict_side_effect_fn

test_cases = {
    "EXTRA      new-file": RepoStats(new=1),
    "EDITED     modified-file": RepoStats(changed=1),
    "CONFLICT   conflicted-file": RepoStats(conflicted=1),
    "ADDED      added-file": RepoStats(staged=1),
}


class FossilTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("vcs", "show_symbol"): False,
        })

        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        sh.fossil("init", "test.fossil")
        sh.fossil("open", "test.fossil")

        self.segment = fossil.Segment(self.powerline, {})

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def _add_and_commit(self, filename):
        sh.touch(filename)
        sh.fossil("add", filename)
        sh.fossil("commit", "-m", "add file " + filename)

    def _checkout_new_branch(self, branch):
        sh.fossil("branch", "new", branch, "trunk")
        sh.fossil("checkout", branch)

    @mock.patch("powerline_shell.utils.get_PATH")
    def test_fossil_not_installed(self, get_PATH):
        get_PATH.return_value = "" # so fossil can't be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_non_fossil_directory(self):
        sh.fossil("close", "--force")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_standard(self):
        self._add_and_commit("foo")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], " trunk ")

    def test_different_branch(self):
        self._add_and_commit("foo")
        self._checkout_new_branch("bar")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], " bar ")

    @mock.patch('powerline_shell.segments.fossil._get_fossil_status')
    def test_all(self, check_output):
        for stdout, result in test_cases.items():
            stats = fossil.parse_fossil_stats([stdout])
            self.assertEquals(result, stats)
