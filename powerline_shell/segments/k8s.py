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


def ellipse(string, length):
    if length > 0:
        return (string[:length] + '~') if len(string) > length else string
    else:
        return EMPTY


class Segment(BasicSegment):
    def add_to_powerline(self):
        kctx = kube_info('kubectl-ctx -c')
        if not kctx:
            return                          # no context, nothing to do

        powerline = self.powerline

        kctx = ellipse(kctx,
                       powerline.segment_conf('k8s', 'max_context'))

        kns = ellipse(kube_info("kubectl-ns -c"),
                      powerline.segment_conf('k8s', 'max_namespace'))

        status = kctx + ('|' if kctx and kns else EMPTY) + kns

        bg = powerline.theme.K8S_BG
        fg = powerline.theme.K8S_FG
        sym_fg = powerline.theme.K8S_SYMBOL_FG

        if powerline.segment_conf('k8s', 'colorize'):
            bg, fg = stringToHashToColorAndOpposite(status)
            fg, bg = (rgb2short(*color) for color in [fg, bg])

            if powerline.segment_conf('k8s', 'colorize_symbol'):
                sym_fg = fg

        lspace = EMPTY if powerline.segment_conf('k8s', 'ltrim') else ' '
        rspace = EMPTY if powerline.segment_conf('k8s', 'rtrim') else ' '

        if powerline.segment_conf('k8s', 'symbol'):
            powerline.append(lspace + U'\U0001F578' + ' ', sym_fg, bg)
            powerline.append(status + rspace, fg, bg)
        else:
            powerline.append(lspace + status + rspace, fg, bg)
