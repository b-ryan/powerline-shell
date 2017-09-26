import unittest
import mock
import tempfile
import shutil
import sh
import powerline_shell.segments.fossil as fossil
from powerline_shell.utils import RepoStats


rs = RepoStats()
test_cases = {
    "EXTRA      new-file": rs.symbols["new"],
    "EDITED     modified-file": rs.symbols["changed"],
    "CONFLICT   conflicted-file": rs.symbols["conflicted"],
    "ADDED      added-file": rs.symbols["staged"],
}


class FossilTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()

        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        sh.fossil("init", "test.fossil")
        sh.fossil("open", "test.fossil")

        self.segment = fossil.Segment(self.powerline)

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def _add_and_commit(self, filename):
        sh.touch(filename)
        sh.fossil("add", filename)
        sh.fossil("commit", "-m", "add file " + filename)

    def _checkout_new_branch(self, branch):
        sh.fossil("branch", "new", branch, "trunk")

    @mock.patch("powerline_shell.segments.fossil.get_PATH")
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

    @mock.patch('powerline_shell.segments.fossil._get_fossil_status')
    def test_all(self, check_output):
        for stdout, result in test_cases.items():
            check_output.return_value = [stdout]
            self.segment.start()
            self.segment.add_to_powerline()
            self.assertEqual(self.powerline.append.call_args[0][0].split()[0],
                             result)
