from ..utils import BasicSegment
import os
import getpass
from socket import gethostname


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        
        if powerline.segment_conf("username", "withHost"):
            hostname = gethostname()
            user_prompt = " %s@%s " % (os.getenv("USER"),
                    hostname.split(".")[0])
        else:
            if powerline.args.shell == "bash":
                user_prompt = r" \u "
            elif powerline.args.shell == "zsh":
                user_prompt = " %n "
            else:
                user_prompt = " %s " % os.getenv("USER")

        if getpass.getuser() == "root":
                bgcolor = powerline.theme.USERNAME_ROOT_BG
        else:
                bgcolor = powerline.theme.USERNAME_BG           

        powerline.append(user_prompt, powerline.theme.USERNAME_FG, bgcolor)
