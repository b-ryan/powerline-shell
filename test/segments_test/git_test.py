import unittest
from contextlib import ExitStack

import mock
import tempfile
import shutil
import sh
import powerline_shell.segments.git as git
from ..testing_utils import dict_side_effect_fn


class GitTest(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("vcs", "show_symbol"): False,
        })

        self.dirname = tempfile.mkdtemp()
        with sh.pushd(self.dirname):
            sh.git("init", ".")
            sh.git("config", "user.name", "Test")
            sh.git("config", "user.email", "example@example.com")

        self.segment = git.Segment(self.powerline, {})

        with ExitStack() as stack:
            self._resource = stack.enter_context(sh.pushd(self.dirname))
            self.addCleanup(stack.pop_all().close)


    def tearDown(self):
        shutil.rmtree(self.dirname)

    def _add_and_commit(self, filename):
        sh.touch(filename)
        sh.git("add", filename)
        sh.git("commit", "-m", "add file " + filename)

    def _checkout_new_branch(self, branch):
        sh.git("checkout", "-b", branch)

    def _get_commit_hash(self):
        return sh.git("rev-parse", "HEAD")

    @mock.patch('powerline_shell.utils.get_PATH')
    def test_git_not_installed(self, get_PATH):
        get_PATH.return_value = "" # so git can't be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_non_git_directory(self):
        shutil.rmtree(".git")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    def test_big_bang(self):
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], ' Big Bang ')

    def test_master_branch(self):
        self._add_and_commit("foo")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertIn(self.powerline.append.call_args[0][0], [' master ', ' main '])

    def test_different_branch(self):
        self._add_and_commit("foo")
        self._checkout_new_branch("bar")
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], ' bar ')

    def test_detached(self):
        self._add_and_commit("foo")
        commit_hash = self._get_commit_hash()
        self._add_and_commit("bar")
        sh.git("checkout", "HEAD^")
        self.segment.start()
        self.segment.add_to_powerline()

        # In detached mode, we output a unicode symbol and then the shortened
        # commit hash.
        self.assertIn(self.powerline.append.call_args[0][0].split()[1],
                      commit_hash)
