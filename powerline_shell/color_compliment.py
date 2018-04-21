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
    r, g, b = [x/255.0 for x in [r, g, b]] # convert to float before getting hls value
    hls = rgb_to_hls(r,g,b)
    opp = list(hls[:])
    opp[0] = (opp[0]+0.2)%1 # shift hue (a.k.a. color)
    if opp[1] > 255/2:   # for level you want to make sure they
        opp[1] -= 255/2  # are quite different so easily readable
    else:
        opp[1] += 255/2
    if opp[2] > -0.5: # if saturation is low on first color increase second's
        opp[2] -= 0.5
    opp = hls_to_rgb(*opp)
    m = max(opp)
    if m > 255: #colorsys module doesn't give caps to their conversions
        opp = [ x*254/m for x in opp]
    return tuple([ int(x) for x in opp])

def stringToHashToColorAndOpposite(string):
    if py3:
        string = string.encode('utf-8')
    string = md5(string).hexdigest()[:6] # get a random color
    color1 = rgbstring2tuple(string)
    color2 = getOppositeColor(*color1)
    return color1, color2
