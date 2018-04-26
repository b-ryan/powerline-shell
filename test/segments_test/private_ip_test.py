import unittest
import mock
import sh
import powerline_shell.segments.private_ip as private_ip
from powerline_shell.utils import RepoStats
from ..testing_utils import dict_side_effect_fn


class PrivateIp(unittest.TestCase):

    def setUp(self):
        self.powerline = mock.MagicMock()
        self.powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("private_ip", "interface", private_ip.Defaults.INTERFACE): "eth0",
            ("private_ip", "show_offline", private_ip.Defaults.SHOW_OFFLINE): True,
        })
        self.segment = private_ip.Segment(self.powerline)

    def test_ifconfig_parser(self):
        output = """eth0      Link encap:Ethernet  HWaddr 02:42:ac:11:00:02
        inet addr:172.17.0.2  Bcast:172.17.255.255  Mask:255.255.0.0
        UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
        RX packets:9 errors:0 dropped:0 overruns:0 frame:0
        TX packets:6 errors:0 dropped:0 overruns:0 carrier:0
        collisions:0 txqueuelen:0
        RX bytes:1078 (1.0 KB)  TX bytes:508 (508.0 B)"""
        ip = private_ip.ifconfig_parser(output)
        self.assertEqual(ip, "172.17.0.2")

    @mock.patch('powerline_shell.segments.private_ip.ifconfig_parser')
    def test_correct_appending(self, ifconfig_parser):
        ifconfig_parser.return_value = "172.17.0.2"
        self.segment.start()
        self.segment.add_to_powerline()
        self.assertEqual(
            self.powerline.append.call_args[0][0].split()[0], "172.17.0.2")

    @mock.patch('powerline_shell.segments.private_ip.PrivateIp')
    def test_hide_offline(self, private_ip_constructor):
        powerline = mock.MagicMock()
        ip = private_ip_constructor.return_value
        ip.get.return_value = None
        powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("private_ip", "interface", private_ip.Defaults.INTERFACE): "eth0",
            ("private_ip", "show_offline", private_ip.Defaults.SHOW_OFFLINE): False,
        })
        segment = private_ip.Segment(powerline)
        segment.start()
        segment.add_to_powerline()
        self.assertEqual(
            powerline.append.call_args, None)

    @mock.patch('powerline_shell.segments.private_ip.PrivateIp')
    def test_show_offline(self, private_ip_constructor):
        powerline = mock.MagicMock()
        ip = private_ip_constructor.return_value
        ip.get.return_value = None
        powerline.segment_conf.side_effect = dict_side_effect_fn({
            ("private_ip", "interface", private_ip.Defaults.INTERFACE): "eth0",
            ("private_ip", "show_offline", private_ip.Defaults.SHOW_OFFLINE): True,
        })
        segment = private_ip.Segment(powerline)
        segment.start()
        segment.add_to_powerline()
        self.assertEqual(
            powerline.append.call_args[0][0].split()[0], "Offline")