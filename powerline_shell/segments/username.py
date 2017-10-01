from ..utils import BasicSegment
import os
import pwd


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        if powerline.args.shell == "bash":
            user_prompt = r" \u "
        elif powerline.args.shell == "zsh":
            user_prompt = " %n "
        else:
            user_prompt = " %s " % os.getenv("USER")

        if pwd.getpwuid(os.getuid())[0] == "root":
            bgcolor = powerline.theme.USERNAME_ROOT_BG
        else:
            bgcolor = powerline.theme.USERNAME_BG

        powerline.append(user_prompt, powerline.theme.USERNAME_FG, bgcolor)
