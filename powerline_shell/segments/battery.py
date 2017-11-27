from ..utils import BasicSegment, warn
import os


class Segment(BasicSegment):
    def add_to_powerline(self):
        # See discussion in https://github.com/banga/powerline-shell/pull/204
        # regarding the directory where battery info is saved
        if os.path.exists("/sys/class/power_supply/BAT0"):
            dir_ = "/sys/class/power_supply/BAT0"
        elif os.path.exists("/sys/class/power_supply/BAT1"):
            dir_ = "/sys/class/power_supply/BAT1"
        else:
            warn("battery directory could not be found")
            return

        with open(os.path.join(dir_, "capacity")) as f:
            cap = int(f.read().strip())
        with open(os.path.join(dir_, "status")) as f:
            status = f.read().strip()
        if status == "Full":
            if self.powerline.segment_conf("battery", "always_show_percentage", False):
                pwr_fmt = u" {cap:d}% \U0001F50C "
            else:
                pwr_fmt = u" \U0001F50C "
        elif status == "Charging":
            pwr_fmt = u" {cap:d}% \u26A1 "
        else:
            pwr_fmt = " {cap:d}% "

        if cap < self.powerline.segment_conf("battery", "low_threshold", 20):
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
        else:
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        self.powerline.append(pwr_fmt.format(cap=cap), fg, bg)
