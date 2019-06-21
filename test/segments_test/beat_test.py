import unittest
import datetime
import mock
import powerline_shell.segments.beat as beat
from powerline_shell.themes.default import Color
from argparse import Namespace

class BeatTest(unittest.TestCase):
    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.theme = Color
        self.segment = beat.Segment(self.powerline, {})
        self.segment.current_datetime = self.patch_date1

    def test_colorize(self):
        self.powerline.segment_conf.return_value = True
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertRegex(args[0], r'@\d{3}\.\d')
        self.assertEqual(args[1], Color.TIME_FG)
        self.assertEqual(args[2], Color.TIME_BG)

    def test_config(self):
        self.segment = beat.Segment(self.powerline,
            {"show_at_sign":"False", "show_decimal":"False"})
        self.segment.current_datetime = self.patch_date1
        
        self.powerline.segment_conf.return_value = True
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertRegex(args[0], r'305', "config check")

    def test_beat(self):
        self.segment.current_datetime = self.patch_date1

        self.powerline.segment_conf.return_value = True
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertRegex(args[0], "@305.6", "specific time")

    def test_beat_rollover(self):
        self.segment.current_datetime = self.patch_date2
        
        # start before transition
        self.powerline.segment_conf.return_value = True
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertRegex(args[0], "@999.3", "before transition")
        
        self.segment.current_datetime = self.patch_date3
        
        # test transition at @000.0
        self.powerline.segment_conf.return_value = True
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertRegex(args[0], "@000.0", "at transition")
        
        # now test the other side of transition
        self.segment.current_datetime = self.patch_date4

        self.powerline.segment_conf.return_value = True
        self.segment.start()
        self.segment.add_to_powerline()
        args = self.powerline.append.call_args[0]
        self.assertRegex(args[0], "@000.7", "after transition")

    # ######################################################################

    def patch_date1(self):
        return datetime.datetime(2019, 6, 20, 6, 20) #@305.6

    def patch_date2(self):
        return datetime.datetime(2019, 6, 20, 22, 59) #@999.3

    def patch_date3(self):
        return datetime.datetime(2019, 6, 20, 23, 0) #@000.0

    def patch_date4(self):
        return datetime.datetime(2019, 6, 20, 23, 1) #@000.7
