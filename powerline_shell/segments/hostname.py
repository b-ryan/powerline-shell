from ..utils import BasicSegment
from ..color_compliment import stringToHashToColorAndOpposite
from ..colortrans import rgb2short
from socket import gethostname


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        if powerline.segment_conf("hostname", "colorize"):
            hostname = gethostname()
            FG, BG = stringToHashToColorAndOpposite(hostname)
            FG, BG = (rgb2short(*color) for color in [FG, BG])
            host_prompt = " %s " % hostname.split(".")[0]
            powerline.append(host_prompt, FG, BG)
        else:
            if powerline.args.shell == "bash":
                host_prompt = r" \h "
            elif powerline.args.shell == "zsh":
                host_prompt = " %m "
            else:
                host_prompt = " %s " % gethostname().split(".")[0]
            powerline.append(host_prompt,
                             powerline.theme.HOSTNAME_FG,
                             powerline.theme.HOSTNAME_BG)
