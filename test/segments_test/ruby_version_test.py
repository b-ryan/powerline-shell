import unittest
import mock
import powerline_shell.segments.ruby_version as ruby_version
from powerline_shell.themes.default import Color
from ..testing_utils import dict_side_effect_fn

class RubyVersionTest(unittest.TestCase):
    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.theme = Color
        self.segment = ruby_version.Segment(self.powerline, {})

    @mock.patch('powerline_shell.utils.get_PATH')
    def test_dependency_not_installed(self, get_PATH):
        get_PATH.return_value = ""  # so ruby and sed can't be found
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_count, 0)

    @mock.patch('powerline_shell.segments.ruby_version._get_ruby_version')
    def test_default_mode(self, mock_ruby_version):
        mock_ruby_version.return_value = "ruby 2.4.1p111"
        self.segment.start()
        self.segment.add_to_powerline()
        expected = ' ruby 2.4.1p111 '
        self.assertEqual(self.powerline.append.call_args[0][0], expected)

    @mock.patch('os.environ.get')
    @mock.patch('powerline_shell.segments.ruby_version._get_ruby_version')
    def test_with_valid_gem_home(self, mock_ruby_version, mock_env):
        mock_ruby_version.return_value = "ruby 2.4.1p111"
        mock_env.return_value = "/path/to/wherever/ruby-2.4.1p111@best_gemset"
        self.segment.start()
        self.segment.add_to_powerline()
        expected = ' ruby 2.4.1p111@best_gemset '
        self.assertEqual(self.powerline.append.call_args[0][0], expected)

    @mock.patch('os.environ.get')
    @mock.patch('powerline_shell.segments.ruby_version._get_ruby_version')
    def test_with_empty_gem_home(self, mock_ruby_version, mock_env):
        mock_ruby_version.return_value = "ruby 2.4.1p111"
        mock_env.return_value = ""
        self.segment.start()
        self.segment.add_to_powerline()
        expected = ' ruby 2.4.1p111 '
        self.assertEqual(self.powerline.append.call_args[0][0], expected)

    @mock.patch('os.environ.get')
    @mock.patch('powerline_shell.segments.ruby_version._get_ruby_version')
    def test_with_gem_home_lacking_gemset(self, mock_ruby_version, mock_env):
        mock_ruby_version.return_value = "ruby 2.4.1p111"
        mock_env.return_value = "/path/to/wherever/ruby-2.4.1p111"
        self.segment.start()
        self.segment.add_to_powerline()
        expected = ' ruby 2.4.1p111 '
        self.assertEqual(self.powerline.append.call_args[0][0], expected)

    @mock.patch('powerline_shell.segments.ruby_version._get_ruby_version')
    def test_fancy_mode(self, mock_ruby_version):
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("ruby_version", "mode"): "fancy",
        })
        mock_ruby_version.return_value = "ruby 2.4.1p111"
        self.segment.start()
        self.segment.add_to_powerline()
        expected = ' %s 2.4.1p111 ' % ruby_version.FANCY_RUBY
        self.assertEqual(self.powerline.append.call_args[0][0], expected)
