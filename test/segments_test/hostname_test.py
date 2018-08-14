import unittest
import mock
import powerline_shell.segments.hostname as hostname
from powerline_shell.themes.default import Color
from argparse import Namespace
from ..testing_utils import dict_side_effect_fn

class HostnameTest(unittest.TestCase):
    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.theme = Color
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("hostname", "colorize"): True,
            ("hostname", "fg", ""): "",
            ("hostname", "bg", ""): "",
        })
        self.segment = hostname.Segment(self.powerline)

    def test_colorize(self):
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertNotEqual(args[0], r" \h ")
        self.assertNotEqual(args[1], Color.HOSTNAME_FG)
        self.assertNotEqual(args[2], Color.HOSTNAME_BG)
