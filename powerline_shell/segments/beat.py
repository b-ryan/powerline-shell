import math
import datetime
from ..utils import BasicSegment

class Segment(BasicSegment):
    def add_to_powerline(self):
        '''
        Interface method called by Powerline
        '''
        pline = self.powerline
        beat = self.current_beat()
        format = "%05.1f" if self.show_decimal() else "%03.0f"
        if self.show_at_sign():
            format = " @%s " % format
        pline.append(format % beat, pline.theme.TIME_FG, pline.theme.TIME_BG)
    def show_decimal(self):
        '''
        @return boolean
        '''
        raw = self.powerline.segment_conf("beat", "show_decimal", "True")
        return raw != "False"
    def show_at_sign(self):
        '''
        @return boolean
        '''
        raw = self.powerline.segment_conf("beat", "show_at_sign", "True")
        return raw != "False"
    def current_datetime(self):
        '''
        Don't do anything in this function but get the current UTC time. This 
        method will be monkey patched when tested.
        @return current date and time
        '''
        return datetime.datetime.utcnow()
    def current_beat(self):
        '''
        Handles the math of finding a beat
        @return current beat as a float
        '''
        now = self.current_datetime()
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        beat = ( (now - midnight).seconds + 3600) / 86.4
        # 1000.000000 >= 1000.0 was not passing, so using rounded values
        if round(beat) >= 1000:
            beat = math.copysign(beat-1000.0, 0)
        return beat
