import os
import re
import subprocess
import platform
from ..utils import ThreadedSegment

class Segment(ThreadedSegment):
    '''
    @author thomas.cherry@gmail.com
    '''
    def __init__(self, powerline, config):
        super(Segment, self).__init__(powerline)
        self.config = config
        self.output = None

    def run(self):
        opt = self.config["options"]
        cmd = opt["command"]
        if len(cmd)>0 and len(cmd[0])>0:
            self.output = subprocess.check_output(cmd).decode('utf-8').strip()
        
    def add_to_powerline(self):
        self.join()
        if  self.output is not None and len(self.output) > 0:
            text = ' %s ' % self.output
            fg_color = self.powerline.theme.CWD_FG      #just use CWD's colors
            bg_color = self.powerline.theme.PATH_BG     #just use CWD's colors
            self.powerline.append(text, fg_color, bg_color)
