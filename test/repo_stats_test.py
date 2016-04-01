import unittest
import powerline_shell_base as p


class RepoStatsTest(unittest.TestCase):

    def setUp(self):
        self.repo_stats = p.RepoStats()
        self.repo_stats.not_staged = 1
        self.repo_stats.conflicted = 4

    def test_dirty(self):
        self.assertTrue(self.repo_stats.dirty)

    def test_simple(self):
        self.assertEqual(self.repo_stats.untracked, 0)

    def test_n_or_empty__empty(self):
        self.assertEqual(self.repo_stats.n_or_empty("not_staged"), u"")

    def test_n_or_empty__n(self):
        self.assertEqual(self.repo_stats.n_or_empty("conflicted"), u"4")

    def test_index(self):
        self.assertEqual(self.repo_stats["not_staged"], 1)
