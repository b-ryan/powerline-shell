import os
import re
import subprocess
import platform
from ..utils import ThreadedSegment

class Segment(ThreadedSegment):
    '''
    Display the disk usage for the current working directory as a segment.
    No configuration needed, simply add "du" to segments array in the
    ~/.powerline-shell.json file.
    @author thomas.cherry@gmail.com
    '''
    def run(self):
        self.usage = ""
        ignore = self.powerline.segment_conf("du", "ignore", ())
        wd = self.powerline.cwd or os.getenv('PWD')
        cmd = ['du','-sh', "."]
        
        rule = "(^" + "$)|(^".join(ignore) + "$)"
        if re.match(rule, wd):
            return
        
        try:
            nul_f = open(os.devnull, 'w') 
            result = subprocess.check_output(cmd,stderr=nul_f,timeout=1)
            self.usage = result.split()[0].decode('utf-8')
        except subprocess.CalledProcessError as e:
            self.usage = e.output.split()[0].decode('utf-8')
        except subprocess.TimeoutExpired as e:
            self.usage = "?"
    
    def add_to_powerline(self):
        self.join()
        if len(self.usage) > 0:
            text = '(%s)' % self.usage
            fg_color = self.powerline.theme.CWD_FG      #just use CWD's colors
            bg_color = self.powerline.theme.PATH_BG     #just use CWD's colors
            self.powerline.append(text, fg_color, bg_color)
