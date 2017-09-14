import unittest
from powerline_shell.utils import RepoStats


class RepoStatsTest(unittest.TestCase):

    def setUp(self):
        self.repo_stats = RepoStats()
        self.repo_stats.changed = 1
        self.repo_stats.conflicted = 4

    def test_dirty(self):
        self.assertTrue(self.repo_stats.dirty)

    def test_simple(self):
        self.assertEqual(self.repo_stats.new, 0)

    def test_n_or_empty__empty(self):
        self.assertEqual(self.repo_stats.n_or_empty("changed"), u"")

    def test_n_or_empty__n(self):
        self.assertEqual(self.repo_stats.n_or_empty("conflicted"), u"4")

    def test_index(self):
        self.assertEqual(self.repo_stats["changed"], 1)
