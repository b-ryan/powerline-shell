import unittest
import mock
import tempfile
import shutil
import sh
import powerline_shell_base as p
import segments.git as git

git.Color = mock.MagicMock()
git.RepoStats = p.RepoStats


class GitTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()

        self.dirname = tempfile.mkdtemp()
        sh.cd(self.dirname)
        sh.git("init", ".")

    def tearDown(self):
        shutil.rmtree(self.dirname)

    def _add_and_commit(self, filename):
        sh.touch(filename)
        sh.git("add", filename)
        sh.git("commit", "-m", "add file " + filename)

    def _new_branch(self, branch):
        sh.git("checkout", "-b", branch)

    def _get_commit_hash(self):
        return sh.git("rev-parse", "HEAD")

    @mock.patch('segments.git.get_PATH')
    def test_git_not_installed(self, get_PATH):
        get_PATH.return_value = "" # so git can't be found
        git.add_git_segment(self.powerline)
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_non_git_directory(self):
        shutil.rmtree(".git")
        git.add_git_segment(self.powerline)
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_big_bang(self):
        git.add_git_segment(self.powerline)
        self.assertEqual(self.powerline.append.call_args[0][0], ' Big Bang ')

    def test_master_branch(self):
        self._add_and_commit("foo")
        git.add_git_segment(self.powerline)
        self.assertEqual(self.powerline.append.call_args[0][0], ' master ')

    def test_different_branch(self):
        self._add_and_commit("foo")
        self._new_branch("bar")
        git.add_git_segment(self.powerline)
        self.assertEqual(self.powerline.append.call_args[0][0], ' bar ')

    def test_detached(self):
        self._add_and_commit("foo")
        commit_hash = self._get_commit_hash()
        self._add_and_commit("bar")
        sh.git("checkout", "HEAD^")
        git.add_git_segment(self.powerline)

        # In detached mode, we output a unicode symbol and then the shortened
        # commit hash.
        self.assertIn(self.powerline.append.call_args[0][0].split()[1],
                      commit_hash)
