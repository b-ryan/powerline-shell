from ..utils import BasicSegment, warn
import os
from sys import platform
MACOS = platform == "darwin"

class Segment(BasicSegment):
    def add_to_powerline(self):
        # See discussion in https://github.com/banga/powerline-shell/pull/204
        # regarding the directory where battery info is saved
        if os.path.exists("/sys/class/power_supply/BAT0"):
            dir_ = "/sys/class/power_supply/BAT0"
        elif os.path.exists("/sys/class/power_supply/BAT1"):
            dir_ = "/sys/class/power_supply/BAT1"
        elif MACOS:
            pass
        else:
            warn("battery directory could not be found")
            return
        if MACOS:
            # This way the non-macos people don't have to pay for the imports
            from subprocess import check_output
            import re
            source = check_output(["pmset", "-g", "batt"]).strip().decode()
            # capacity
            cap = int(re.findall(r"[0-9]{1,3}%", source)[0][:-1])
            status_source = source[source.find(";") + 2: source.rfind(";")]

            if status_source == "charged":
                status = "Full"
            elif status_source == "charging":
                status = "Charging"
            else:
                status = "Discharging"

        else:                
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
