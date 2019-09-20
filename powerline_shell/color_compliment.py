from colorsys import hls_to_rgb, rgb_to_hls
# md5 deprecated since Python 2.5
try:
    from md5 import md5
except ImportError:
    from hashlib import md5
import sys
from .colortrans import *
from .utils import py3


def getOppositeColor(r,g,b):
    """returns RGB components of complementary color"""
    # colorsys functions expect values to be between 0 and 1
    hls = rgb_to_hls(*[x/255.0 for x in [r, g, b]]) # r,g,b are now between 0 and 1
    opp = hls_to_rgb(*[ (x+0.5)%1 for x in hls ])
    return tuple([ int(x*255) for x in opp ]) # convert back to value range 0-255

def stringToHashToColorAndOpposite(string):
    if py3:
        string = string.encode('utf-8')
    string = md5(string).hexdigest()[:6] # get a random color
    color1 = rgbstring2tuple(string)
    color2 = getOppositeColor(*color1)
    return color1, color2
