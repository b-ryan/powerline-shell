import unittest

import mock

from powerline_shell.segments.jobs import Segment


class JobsTest(unittest.TestCase):
    def setUp(self):
        self.powerline = mock.MagicMock()
        self.segment = Segment(self.powerline, {})

    @mock.patch('powerline_shell.segments.jobs.platform.system', return_value='Linux')
    @mock.patch('powerline_shell.segments.jobs.os.getppid', return_value=123)
    @mock.patch('powerline_shell.segments.jobs.subprocess.Popen')
    def test_similar_parent_pids_are_not_jobs(self, popen, getppid, system):
        popen.return_value.communicate.return_value = (
            b' PPID\n  123\n 1123\n 1230\n 123123\n', None)

        self.segment.run()
        self.assertEqual(self.segment.num_jobs, 0)
        self.segment.join = mock.Mock()
        self.segment.add_to_powerline()
        self.powerline.append.assert_not_called()

    @mock.patch('powerline_shell.segments.jobs.platform.system', return_value='Darwin')
    @mock.patch('powerline_shell.segments.jobs.os.getppid', return_value=123)
    @mock.patch('powerline_shell.segments.jobs.subprocess.Popen')
    def test_count_exact_parent_pids(self, popen, getppid, system):
        popen.return_value.communicate.return_value = (
            b' PPID\n  123\n  123\n  123\n 1123\n 1230\n', None)

        self.segment.run()
        self.assertEqual(self.segment.num_jobs, 2)
        self.segment.join = mock.Mock()
        self.segment.add_to_powerline()
        self.assertEqual(self.powerline.append.call_args[0][0], ' 2 ')

    @mock.patch('powerline_shell.segments.jobs.platform.system', return_value='Linux')
    @mock.patch('powerline_shell.segments.jobs.os.getppid', return_value=123)
    @mock.patch('powerline_shell.segments.jobs.subprocess.Popen')
    def test_whitespace_and_line_endings(self, popen, getppid, system):
        popen.return_value.communicate.return_value = (
            b' PPID\r\n\t123\r\n 123 \r\n\r\n', None)

        self.segment.run()
        self.assertEqual(self.segment.num_jobs, 1)

    @mock.patch('powerline_shell.segments.jobs.platform.system', return_value='CYGWIN_NT')
    @mock.patch('powerline_shell.segments.jobs.os.getppid', return_value=123)
    @mock.patch('powerline_shell.segments.jobs.subprocess.Popen')
    def test_cygwin_parent_pid_count(self, popen, getppid, system):
        popen.return_value.communicate.return_value = (
            b'UID PID PPID\n100 1 123\n100 2 123\n100 3 1123\n', None)

        self.segment.run()
        self.assertEqual(self.segment.num_jobs, 1)
