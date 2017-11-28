from ..utils import BasicSegment, warn
import os, subprocess, re

LOW_BATTERY_THRESHOLD = 20

charge_state = {
    "charged":"charged",
    "discharging":"discharging",
    "charging":"charging",
    "finishing charge":"finishing charge",
    
    "full":"charged"
}

GLYPH_FULL = u"\U0001F50C"
GLYPH_CHARGING = u"\u26A1"
GLYPH_DISCHARGING = u"\u2301"

GLYPH_BATT = u"\u2393"
GLYPH_WALL = u"\u23E6"

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
            if status.lower() in charge_state:
                status = charge_state[status.lowwer()]
        self.display(status, cap)
    
    def display(self, raw_status, raw_cap, raw_source="unknown"):
        '''
        sends formated text to powerline, displays lots of things when needed:
        * battery/ac(glyph) percent_charge(number) charge_action(glyph)
        * battery/ac glpyh always displays
        * percent_charge may be hidden if 100
        * charge_action always displays
        @return status charging status is one of [charged|discharging|charging|finishing charge]
        @cap capacity 0-100 as a string
        '''
        status = raw_status.strip().lower()
        source = raw_source.strip().lower()
        cap = int(raw_cap)
        format = " {src:s} {cap:d}% {pow:s} "
        
        ################
        # set display options based on source
        if len(source)==0:
            src = u""   # no source giving, display nothing
        elif source=="battery":
            src = GLYPH_BATT
        elif source=="power":
            src = GLYPH_WALL
        else:
            src = u""   #unknown source, display nothing
        
        ################
        # set display options based on capacity
        if cap<0 or 100<cap:
            warn ("'%d' is not a valid battery capacity" % cap)
        if cap < self.low_battery_threshold() and source!="ac":
            # need human to take note of this state
            bg = self.powerline.theme.BATTERY_LOW_BG
            fg = self.powerline.theme.BATTERY_LOW_FG
        else:
            bg = self.powerline.theme.BATTERY_NORMAL_BG
            fg = self.powerline.theme.BATTERY_NORMAL_FG
        
        '''
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
        '''
        
        ################
        # set display options based on status
        if len(status)==0:
            pwr = u""   # no status giving, display nothing
        elif status == "charged":
            # show less info if charged
            pwr = self.powerline.segment_conf("battery","g_charged", GLYPH_FULL)
            if not self.powerline.segment_conf("battery", "always_show_percentage", False):
                format = "{src:s} {pow:s}"
                pwr = self.powerline.segment_conf("battery","g_charged", GLYPH_FULL)
        elif status == "discharging":
            pwr = self.powerline.segment_conf("battery","g_discharging", GLYPH_DISCHARGING)
        elif status == "charging":
            pwr = self.powerline.segment_conf("battery","g_charging", GLYPH_CHARGING)
        elif status == "finishing charge":
            pwr = self.powerline.segment_conf("battery","g_finishing", GLYPH_CHARGING)
        else:
            pwr = u""   # unknown status given, display nothing
        
        self.powerline.append(format.format(src=src, cap=cap, pow=pwr), fg, bg)
    
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
