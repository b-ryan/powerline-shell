from ..utils import BasicSegment, warn
import os, subprocess, re

LOW_BATTERY_THRESHOLD = 20

class Segment(BasicSegment):
    def add_to_powerline(self):
        # See discussion in https://github.com/banga/powerline-shell/pull/204
        # regarding the directory where battery info is saved
        
        if os.path.exists("/sys/class/power_supply/BAT0"):
            dir_ = "/sys/class/power_supply/BAT0"
            self.handle_sys_class(dir_)
            return
        elif os.path.exists("/sys/class/power_supply/BAT1"):
            dir_ = "/sys/class/power_supply/BAT1"
            self.handle_sys_class(dir_)
            return
        elif os.path.exists("/usr/bin/pmset"):
            self.handle_pmset()
            return
        else:
            warn("battery directory could not be found")
            return
    
    def low_battery_threshold(self):
        '''
        gets the user configured threshold for low battery mode
        @return value between 0 and 100
        '''
        raw = self.powerline.segment_conf("battery","low",LOW_BATTERY_THRESHOLD)
        lbt = raw if 0<raw and raw<100 else LOW_BATTERY_THRESHOLD
        return lbt
    
    def handle_sys_class(self, dir_):
        '''
        Pull the batter info from the supplied proc file and send to powerline
        @param dir_ path to a sys class battery file
        '''
        cap = -1
        with open(os.path.join(dir_, "capacity")) as f:
            cap = int(f.read().strip())
        with open(os.path.join(dir_, "status")) as f:
            status = f.read().strip()
        self.display(status, cap)
    
    def display(self, status, cap, source="unknown"):
        '''
        sends formated text to powerline
        @return status charging status is one of [charged|discharging|???]
        @cap capacity 0-100 as a string
        '''
        pwr = u"\u26A1" if status.lower() == "charging" else u" "
        pwr = u"\u2301" if status.lower() == "discharging" else pwr
        
        src = u"\u2393" if source.lower() == "battery" else ""
        src = u"\u23E6" if source.lower() == "power" else src
        
        if cap<0 or 100<cap:
            warn ("'%d' is not a valid battery capacity" % cap)
        
        if cap < self.low_battery_threshold() and source!="ac":
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
        else:
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        self.powerline.append(" %s %d%% %s " % (src, cap, pwr), fg, bg)
    
    def handle_pmset(self):
        '''
        mac os x has pmset, but don't assume mac since all of Darwin could be 
        using this tool.
        '''
        status = ""         # [charged|discharging|charging|finishing charge]
        cap = -1            # capacity 0-100 as a string, -1 on error
        source = "unknown"  # one of [battery|power]
        
        cmd = ["/usr/bin/pmset", "-g", "batt"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        lines = proc.communicate()[0].decode("utf-8").split("\n")
        
        for raw in lines:
            line = raw.strip()
            if "Now drawing from" in line:
                source = "battery" if "'Battery Power'" in line else \
                    ("ac" if "'AC Power'" in line else "")
            elif "InternalBattery" in line:
                m = re.search('([0-9]{1,3})%;', lines[1])
                if m is not None:
                    raw_cap = int(m.group(1))
                    cap = raw_cap if (0<=raw_cap and raw_cap<=100) else -1
                m = re.search('[0-9]{1,3}%; ([a-z ]+);', lines[1])
                if m is not None:
                    status = m.group(1).strip()
                break
        
        self.display(status, cap, source)
