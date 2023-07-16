import os
import subprocess
from ..utils import BasicSegment
from ..colortrans import rgb2short
from ..color_compliment import stringToHashToColorAndOpposite


EMPTY = ''


def kube_info(cmd):
    try:
        p = subprocess.Popen(cmd.split(),
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=os.environ.copy())
    except OSError:
        return EMPTY

    data = p.communicate()
    if p.returncode:
        return EMPTY

    return data[0].decode('utf-8').splitlines()[0]


def ellipse(s, length):
    if length > 0:
        return (s[:length] + '~') if len(s) > length else s
    else:
        return EMPTY


class Segment(BasicSegment):
    def add_to_powerline(self):
        kctx = kube_info('kubectl-ctx -c')
        if not kctx:
            return                          # no context, nothing to do

        powerline = self.powerline
        conf = lambda key: powerline.segment_conf('k8s', key)

        kctx = ellipse(kctx, conf('max_context'))
        kns = ellipse(kube_info("kubectl-ns -c"), conf('max_namespace'))
        status = f"{kctx}{'|' if kctx and kns else EMPTY}{kns}"

        # the symbol and separator can be themed too
        bg = powerline.theme.K8S_BG
        fg = powerline.theme.K8S_FG
        sym_fg = powerline.theme.K8S_SYMBOL_FG

        if conf('colorize'):
            bg, fg = stringToHashToColorAndOpposite(status)
            fg, bg = (rgb2short(*color) for color in [fg, bg])

            if conf('colorize_symbol'):
                sym_fg = fg

        lspace = EMPTY if conf('ltrim') else ' '
        rspace = EMPTY if conf('rtrim') else ' '

        if conf('symbol'):
            powerline.append(f"{lspace}\U0001F578 ", sym_fg, bg)
            powerline.append(f"{status}{rspace}", fg, bg)
        else:
            powerline.append(f"{lspace}{status}{rspace}", fg, bg)
