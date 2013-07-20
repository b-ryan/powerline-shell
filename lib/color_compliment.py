#! /usr/bin/env python

from colortrans import *
from colorsys import hls_to_rgb, rgb_to_hls
from md5 import md5
from sys import argv


def getOppositeColor(r,g,b):
    hls = rgb_to_hls(r,g,b)
    opp = list(hls[:])
    opp[0] = 255-opp[0] # reverse hue (a.k.a. color)
    if opp[1] > 255/2:   # for level you want to make sure they
        opp[1] -= 255/2  # are quite different so easily readable
    else:
        opp[1] += 255/2
    opp[1], 255-opp[2]
    opp = ( int(x) for x in opp)
    return hls_to_rgb(*opp)

def stringToHashToColorAndOpposite(string):
    string = md5(string).hexdigest()[:6] # get a random color
    color1 = rgbstring2tuple(string)
    color2 = getOppositeColor(*color1)
    return color1, color2
