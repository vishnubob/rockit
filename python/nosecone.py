#!/usr/bin/env python
import math
import time
from solid import *

def conical_nosecone_func(x=1, R=1, L=1, steps=100):
    # http://en.wikipedia.org/wiki/Nose_cone_design#Conical
    for step in xrange(steps):
        _x = x * float(step) / steps
        _y = _x * R / L
        yield(_x, _y)

def elliptical_nosecone_func(x=1, R=1, L=1, width=1, steps=100):
    for step in xrange(steps):
        _x = L * float(step) / (steps - 1)
        _y = R * math.sqrt(1.0 - (_x ** 2 / L ** 2))
        yield(_x, _y)
    
    x -= width
    R -= width
    L -= width

    for step in xrange(steps, 1, -1):
        _x = L * float(step) / (steps)
        _y = R * math.sqrt(1.0 - (_x ** 2 / L ** 2))
        yield(_x, _y)

def sbc_nosecone_func(x=1, R=1, L=1, rn=.5, steps=100):
    xt = (L ** 2 / R) * math.sqrt(rn ** 2 / (R**2 + L**2))
    for step in xrange(steps):
        _x = L * float(step) / steps
        _y = (xt * R) / L
        yield(_x, _y)


def nosecone_factory(pathgen):
    points = []
    points.append([0, 0])
    for (x, y) in pathgen:
        #if x == 0:
        #    continue
        points.append([x, y])
    # stay in the same x, return up
    points.append([points[-1][0], 0])
    # and back home
    return points

def render_crosshairs(length=25, width=1, height=1, rad=2):
    scad = \
        union()([
            # red
            rotate([0, 90, 0])( 
                translate([0, -width, -length/ 2.0 + width])( color([1, 0, 0])( cube([width, height, length]) ) ),
                translate([rad / 4.0, rad / 4.0 - width, length / 2.0])( color([1, 0, 0])( sphere(rad) ) ),
            ), 
            # green
            rotate([-90, 0, 0])( 
                translate([0, 0, -length / 2.0])( color([0, 1, 0])( cube([width, height, length]) ) ), 
                translate([rad / 4.0, rad / 4.0, length / 2.0])( color([0, 1, 0])( sphere(rad) ) ),
            ), 
            # blue
            rotate([0, 0, -90])( 
                translate([0, 0, -length/ 2.0])( color([0, 0, 1])( cube([width, height, length]) ) ),
                translate([rad / 4.0,  rad / 4.0, length / 2.0])( color([0, 0, 1])( sphere(rad) ) ),
            ), 
        ])
    return scad

def get_midpoint(points):
    return [sum(pts) / 2.0 for pts in zip(*points)]

def render_nosecone_2D(points, r):
    (r1, r2, r3) = r
    scad = rotate([r1, r2, r3])( translate([0, 0, 0])( polygon(points) ))
    return scad

def render_nosecone_3D(points, r):
    scad = union()([ rotate_extrude(convexity=10, segments=100)( render_nosecone_2D(points, r) )])
    return scad

def save_render(name, *scads):
    scads = list(scads)
    scad_render_to_file(union()(scads), "%s.scad" % name)

def save_nosecone(name, outer, inner, r=[0,0,-90]):
    outer_pts = list(nosecone_factory(outer))
    inner_pts = list(nosecone_factory(inner))
    # conical 2D
    _name = "%s_2D" % name
    save_render(_name, render_nosecone_2D(outer_pts, r))
    # conical 3D
    _name = "%s_3D" % name
    scad = difference()( render_nosecone_3D(outer_pts, r), render_nosecone_3D(inner_pts, r)) 
    save_render(_name, scad)

# elliptical
"""
name = "elliptical"
func = elliptical_nosecone_func(R=25.4, L=76.2, steps=400)
save_nosecone(name, func, [0,0,-90])

name = "conical"
conical_nosecone_func(x=76.2 * .75, R=25.4, L=76.2, steps=100)
func = conical_nosecone_func(x=76.2 * .75, R=25.4, L=76.2, steps=100)
save_nosecone(name, func, [0,0,-90])

name = "sbc"
func = sbc_nosecone_func(x=76.2 * .75, rn=10, R=25.4, L=76.2, steps=100)
save_nosecone(name, func, [0,0,-90])
"""

name = "elliptical"
outer = elliptical_nosecone_func(R=25.4, L=76.2, steps=100)
inner = elliptical_nosecone_func(R=25.4 - 1, L=76.2 - 2, steps=100)
save_nosecone(name, outer, inner)
