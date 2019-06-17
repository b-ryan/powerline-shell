from ..utils import BasicSegment, warn
import os, subprocess, re

LOW_BATTERY_THRESHOLD = 20

class ChargeState:
    def __init__(self, parent, name, glyph):
        self.name = name
        self.glyph = parent.powerline.segment_conf("battery", name, glyph)

GLYPH_FULL = u"\U0001F50C "
GLYPH_CHARGING = u"\u26A1"
GLYPH_DISCHARGING = u"\u2301"

GLYPH_BATT = u"\u2393"
GLYPH_WALL = u"\u23E6"

class Segment(BasicSegment):
    def __init__(self, powerline):
        BasicSegment.__init__(self, powerline)
        self.sys_paths = ("/sys/class/power_supply/BAT0","/sys/class/power_supply/BAT1")
        self.charge_state = {
            "":                 ChargeState(self, "", ""),
            None:               ChargeState(self, "None", "?"),
            "charged":          ChargeState(self, "charged", GLYPH_FULL),
            "discharging":      ChargeState(self, "discharging", GLYPH_DISCHARGING),
            "charging":         ChargeState(self, "charging", GLYPH_CHARGING),
            "finishing charge": ChargeState(self, "finishing charge", GLYPH_CHARGING)
        }
        self.charge_state["full"] = self.charge_state["charged"]
        self.battery_state = {"":"", "battery":GLYPH_BATT, "ac":GLYPH_WALL}
    
    def add_to_powerline(self):
        # See discussion in https://github.com/banga/powerline-shell/pull/204
        # regarding the directory where battery info is saved
        for dir_ in self.sys_paths:
            if os.path.exists(dir_):
                self.handle_sys_class(dir_)
                return
        if os.path.exists("/usr/bin/pmset"):
            self.handle_pmset()
            return
        else:
            #add support for other operating systems here
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
            test = db[status] if status in charge_state else status
        self.display(status, cap)
    
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
    
    def display(self, raw_status, raw_cap, raw_source="unknown"):
        '''
        sends formated text to powerline, displays lots of things when needed
        The primary output is in the format of "source capacity state". Source
        is battery or ac, capacity is battery charge, and state is the charge
        state (charging, discharging, full).
        * source: battery/ac, glyph, always displays
        * charge: percent charge, number, may be hidden if 100%
        * state: charge direction, glyph, always displays
        Style changes if state is very low
        @return status charging status is one of [charged|discharging|charging|finishing charge]
        @cap capacity 0-100 as a string
        '''
        status = raw_status.strip().lower()
        source = raw_source.strip().lower()
        cap = int(raw_cap)
        if cap<0 or 100<cap:
            warn ("'%d' is not a valid battery capacity" % cap)
        format = " {src:s} {cap:d}% {pow:s} "
        ################
        # set display options based on source
        #print (source)
        src = self.battery_state[source] if source in self.battery_state else "?"
        ################
        # set display options based on capacity
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
        elif status in self.charge_state:
            pwr = self.charge_state[status].glyph
            #handle exceptions to the default behavior
            if status == "charged":
                if not self.powerline.segment_conf("battery", "always_show_percentage", False):
                    format = "{src:s} {pow:s}"
        else:
            pwr = u"?"  #unknown state
        
        self.powerline.append(format.format(src=src, cap=cap, pow=pwr), fg, bg)