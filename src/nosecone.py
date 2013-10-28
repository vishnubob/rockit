#!/usr/bin/env python
import math
from solid import *

def conical_nosecone_func(x=1, R=1, L=1, steps=100):
    # http://en.wikipedia.org/wiki/Nose_cone_design#Conical
    for step in xrange(steps):
        _x = x * float(step) / steps
        _y = _x * R / L
        yield(_x, _y)

def elliptical_nosecone_func(height=1, diameter=1, width=1, steps=100):
    points = []
    # outer
    for step in xrange(steps):
        _x = height * float(step) / (steps - 1)
        _y = (diameter / 2.0) * math.sqrt(1.0 - (_x ** 2 / height ** 2))
        points.append([_x, _y])
    # shrink to inner
    height -= width 
    # woops, need to fix this
    #diameter -= 2 * width 
    diameter -= width 
    _x -= width
    points.append([_x, _y])
    # inner
    for step in xrange(int(_x), -1, -1):
        _x = height * float(step) / (steps - 1)
        _y = (diameter / 2.0) * math.sqrt(1.0 - (_x ** 2 / height ** 2))
        points.append([_x, _y])
    return points

def sbc_nosecone_func(x=1, R=1, L=1, rn=.5, steps=100):
    xt = (L ** 2 / R) * math.sqrt(rn ** 2 / (R**2 + L**2))
    for step in xrange(steps):
        _x = L * float(step) / steps
        _y = (xt * R) / L
        yield(_x, _y)
