from ..utils import BasicSegment, warn
import os

LOW_BATTERY_THRESHOLD = 20


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
            cap = f.read().strip()
        with open(os.path.join(dir_, "status")) as f:
            status = f.read().strip()
        pwr = u" \u26A1 " if status == "Charging" else u" "
        if int(cap) < LOW_BATTERY_THRESHOLD:
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
        else:
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        self.powerline.append(" " + cap + "%" + pwr, fg, bg)
