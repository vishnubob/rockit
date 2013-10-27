# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
import math
import time
import os
import tempfile
import pprint
from solid import *

CIRCLE_SEGMENTS = 200

# scad
def tube(name, height, outer_dia, inner_dia, segments=None):
    msg = "Tube [%s]: Dia: inner=%.4f outer=%.4f, Height: %.4f" % (name, inner_dia, outer_dia, height)
    print msg
    return difference() (
        cylinder(h=height, r=outer_dia / 2.0, segments=segments),
        cylinder(h=height, r=inner_dia / 2.0, segments=segments)
    )

def tube2(name, height, outer_dia1, inner_dia1, outer_dia2, inner_dia2, segments=None):
    msg = "Tube2 [%s]: Dia1: inner=%.4f outer=%.4f, Dia2: inner=%.4f outer=%.4f, Height: %.4f" % (name, inner_dia1, outer_dia1, inner_dia2, outer_dia2, height)
    print msg
    return difference() (
        cylinder(h=height, r1=outer_dia1 / 2.0, r2=outer_dia2 / 2.0, segments=segments),
        cylinder(h=height, r1=inner_dia1 / 2.0, r2=inner_dia2 / 2.0, segments=segments),
    )

def save_stl(scadfn, stlfn):
    msg = "Converting SCAD to STL: %s -> %s" % (scadfn, stlfn)
    print msg
    cmd = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD -m make -o %s %s" % (stlfn, scadfn)
    os.system(cmd)

def save_scad(scad, scadfn):
    msg = "Generating SCAD file: %s" % scadfn
    print msg
    scad = scad_render(scad)
    f = open(scadfn, 'w')
    f.write(scad)
    f.close()

def save(scad, name):
    scadfn = name + ".scad"
    stlfn = name + ".stl"
    save_scad(scad, scadfn)
    save_stl(scadfn, stlfn)

def in2mm(inches):
    return inches / 0.0393701

def default(func):
    def _default(self, *args, **kwargs):
        if func.func_name in self and self[func.func_name] != None:
            return self[func.func_name]
        return func(self, *args, **kwargs)
    return property(_default)

class cproperty(property):
    def __get__(self, cls, owner):
        return self.fget.__get__(None, owner)()

class RockitObject(dict):
    def __getattr__(self, key):
        if key in self and self[key] != None:
            return self[key]
        return super(RockitObject, self).__getattribute__(key)

    def __setattr__(self, key, val):
        #print self.__class__.__name__, "SETATTR", key, val, key in self
        if key in self:
            self[key] = val
            return
        super(RockitObject, self).__setattr__(key, val)

class Rockit(RockitObject):
    def __init__(self, *parts, **kw):
        _dct = {part.name: part(rocket=self) for part in parts}
        super(Rockit, self).__init__(_dct)
        self.override(kw.get("override", {}))

    def override(self, config):
        for (key, val) in config.items():
            keys = key.split('.')
            obj = self
            for _key in keys[:-1]:
                obj = getattr(obj, _key)
            setattr(obj, keys[-1], val)

class RockitPart(RockitObject):
    Defaults = {"rocket": None}
    Name = ''

    def __init__(self, **kw):
        _dct = self.Defaults.copy()
        _dct.update(kw)
        super(RockitPart, self).__init__(**_dct)

    @cproperty
    @classmethod
    def name(cls):
        return cls.Name or cls.__name__

    def build(self):
        return ''

class RockitEngine(RockitPart):
    Name = 'engine'

    EngineDefaults = {
        "fit": 1.02,
        "gap": in2mm(.5)
    }

    def __init__(self, **kw):
        _dct = self.EngineDefaults.copy()
        _dct.update(kw)
        _dct.update(self.Defaults)
        super(RockitEngine, self).__init__(**_dct)

class Rockit_Mini_Engine(RockitEngine):
    Defaults = {
        "fit": 1.075,
        "height": in2mm(1.75),
        "dia": in2mm(.5),
    }

class Rockit_Standard_Engine(RockitEngine):
    Defaults = {
        "fit": 1.05,
        "height": in2mm(2.75),
        "dia": in2mm(.69),
    }

class Rockit_D_Engine(RockitEngine):
    Defaults = {
        "height": in2mm(2.75),
        "dia": in2mm(.95),
    }

class Rockit_E_Engine(RockitEngine):
    Defaults = {
        "height": in2mm(3.75),
        "dia": in2mm(.69),
    }

class RockitEngineMount(RockitPart):
    Name = 'engine_mount'
    Defaults = {
        "height": None,
        "inner_dia": None,
        "outer_dia": None,
        "tube_height": None,
        "taper_height": None,
        "firewall_height": None,
        "firewall_inner_dia": None,
        "firewall_outer_dia": None,
    }

    @default
    def height(self):
        return self.tube_height + self.taper_height

    @default
    def tube_height(self):
        return self.rocket.engine.height * self.rocket.engine.fit

    @default
    def inner_dia(self):
        return self.rocket.engine.dia * self.rocket.engine.fit

    @default
    def outer_dia(self):
        return self.inner_dia + self.rocket.body.width

    @default
    def taper_height(self):
        return self.rocket.collar.height

    @default
    def firewall_height(self):
        return self.rocket.collar.height

    @default
    def firewall_inner_dia(self):
        return self.rocket.engine.dia * (1.0 / self.rocket.engine.fit)

    @default
    def firewall_outer_dia(self):
        return self.rocket.body.outer_dia

    def build(self):
        # assume we have been translated to the correct height (collar, offset, etc)
        return union()(
            # engine mount taper
            tube2("engine tube", self.taper_height, self.rocket.body.outer_dia, self.rocket.body.inner_dia, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments),
            # engine mount tube
            translate([0, 0, self.taper_height])( 
                tube("engine tube", self.height, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments),
            ),
            # engine firewall
            translate([0, 0, self.height + self.taper_height - self.firewall_height])( 
                tube2("engine firewall", self.firewall_height, self.rocket.body.outer_dia, self.outer_dia, self.firewall_outer_dia, self.firewall_inner_dia, self.rocket.constants.circle_segments) 
            ),
        )

class RockitCollar(RockitPart):
    Name = 'collar'
    Defaults = {
        "height": in2mm(.35),
        "fit": .985,
        "overlap": None,
        "outer_dia": None,
        "inner_dia": None,
        "outer_dia": None,
        "inner_dia": None,
        # chamfer
        "chamfer_height": 1,
    }

    @default
    def height(self):
        return in2mm(.35)

    @default
    def overlap(self):
        return self.height

    @default
    def inner_dia(self):
        return self.outer_dia - self.rocket.body.width

    @default
    def outer_dia(self):
        return self.rocket.body.inner_dia * self.fit

    def build(self):
        scad = union()(
            translate([0, 0, self.rocket.body.height - self.overlap])(
                tube2("collar", self.overlap, self.rocket.body.outer_dia, self.rocket.body.inner_dia, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments)
            ),
            difference()(
                translate([0, 0, self.rocket.body.height])(
                    tube("collar", self.height, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments)
                ),
                translate([0, 0, self.rocket.body.height + self.height - self.chamfer_height])(
                    tube2("collar chamfer", self.chamfer_height * 2, 
                        self.outer_dia + 1, self.outer_dia, 
                        self.outer_dia + 1, self.inner_dia - 1, 
                        segments=self.rocket.constants.circle_segments)
                ),
            ),
        )
        return scad

class RockitLaunchLug(RockitPart):
    Name = 'launchlug'
    Defaults = {
        #"rod_dia": in2mm(0.1875),
        "rod_dia": in2mm(0.125),
        "fit": 1.55,
        "height": in2mm(2),
        "inner_dia": None,
        "outer_dia": None,
    }

    @default
    def inner_dia(self):
        return self.rod_dia * self.fit

    @default
    def outer_dia(self):
        return self.inner_dia + self.rocket.body.width

    def build(self):
        x_offset = self.rocket.body.outer_dia / 2.0 + self.inner_dia / 2.0
        scad = translate([x_offset, 0, 0])(
            tube("launchlug", self.height, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments)
        )
        return scad

class RockitFin(RockitPart):
    Name = 'fin'
    Defaults = {
        "width": None,
        "height": None,
        "inner_dia": None,
        "outer_dia": None,
        "endchord": None,
        "deflection": 0,
        "coverage": .8,
        "ratio": .5,
        "triangles": None,
        "points": None,
    }

    @default
    def height(self):
        return self.rocket.body.height * self.coverage

    @default
    def width(self):
        return self.rocket.body.width * .5

    @default
    def inner_dia(self):
        return self.rocket.body.outer_dia - self.rocket.constants.min_overlap

    @default
    def outer_dia(self):
        return self.rocket.body.outer_dia * 3.5

    @default
    def endchord(self):
        return self.rocket.body.height * self.ratio

    @default
    def triangles(self):
        return [[0, 1, 2],  [1, 3, 2], [2, 3, 4],  [3, 5, 4], [4, 5, 6], [5, 7, 6], 
                    [6, 7, 0], [7, 1, 0], [0, 2, 6], [2, 4, 6], [1, 7, 3],  [3, 7, 5]]

    @default
    def points(self):
        return [
            # inner-bottom
            [self.inner_dia / 2.0, self.width / 2.0 + self.deflection, 0], 
            [self.inner_dia / 2.0, -self.width / 2.0 + self.deflection, 0],
            # outer-bottom
            [self.outer_dia / 2.0, self.width / 2.0 + self.deflection, 0],
            [self.outer_dia / 2.0, -self.width / 2.0 + self.deflection, 0],
            # inner-top
            [self.outer_dia / 2.0, self.width / 2.0 - self.deflection, self.height - self.endchord], 
            [self.outer_dia / 2.0, -self.width / 2.0 - self.deflection, self.height - self.endchord],
            # outer-top
            [self.inner_dia / 2.0, self.width / 2.0 - self.deflection, self.height],
            [self.inner_dia / 2.0, -self.width / 2.0 - self.deflection, self.height],
        ]

    def build(self):
        scad = polyhedron(points=self.points, triangles=self.triangles)
        return scad

class RockitTail(RockitPart):
    Name = 'tail'
    Defaults = {
        "fin_count": 4,
    }

    def build(self):
        parts = []
        # rocket body 
        parts.append(self.rocket.body.build())
        # collar 
        parts.append(self.rocket.collar.build())
        # engine mount
        parts.append(self.rocket.engine_mount.build())
        # fins
        for finidx in range(self.fin_count):
            z_angle = finidx * (360.0 / self.fin_count)
            part = rotate([0,0,z_angle])( self.rocket.fin.build() )
            parts.append(part)
        # launch lug
        z_angle = (360.0 / self.fin_count) / 2.0
        part = rotate([0,0,z_angle])( self.rocket.launchlug.build() )
        parts.append(part)
        return union()(parts)

class RockitCollarTest(RockitPart):
    Name = 'collar_test'

    def build(self):
        return union()(
            union()(
                self.rocket.body.build(),
                self.rocket.collar.build(),
            ),
            translate([self.rocket.body.outer_dia * 1.1,0,0]) (
                union()(
                    self.rocket.body.build(),
                    self.rocket.collar.build(),
                )
            )
        )

class RockitBody(RockitPart):
    Name = 'body'
    Defaults = {
        "width": 2.5,
        "height": None,
        "inner_dia": None,
        "outer_dia": None,
    }

    @default
    def height(self):
        return self.rocket.engine_mount.height + self.rocket.collar.height

    @default
    def inner_dia(self):
        return self.rocket.engine.dia + self.rocket.engine.gap

    @default
    def outer_dia(self):
        return self.rocket.body.inner_dia + self.rocket.body.width

    def build(self):
        return tube("body", self.height, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments)

class RockitConstants(RockitPart):
    Name = 'constants'

    Defaults = {
        "min_overlap": .001,
        "circle_segments": CIRCLE_SEGMENTS,
    }

def engine_mount_test():
    override = {}
    override["engine_mount.height"] = 10
    override["engine_mount.taper_height"] = 0
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, RockitEngineMount, RockitBody, RockitCollar, override=override)
    pprint.pprint(rocket)
    f = open("engine_mount_test.scad", 'w')
    scad = rocket.engine_mount.build()
    f.write(scad_render(scad))

def make_engine_panel():
    override = {}
    override["engine_mount.height"] = 10
    override["engine_mount.taper_height"] = 0
    #rocket = Rockit(RockitConstants, Rockit_Mini_Engine, RockitEngineMount, RockitBody, RockitCollar, override=override)
    rocket = Rockit(RockitConstants, Rockit_Standard_Engine, RockitEngineMount, RockitBody, RockitCollar, override=override)
    slist = []
    for (idx, x) in enumerate(range(4)):
        x += 4
        x = 4 / 100.0 + (.005 * idx) + 1
        print x
        rocket.engine.fit = x
        pprint.pprint(rocket)
        scad = rocket.engine_mount.build()
        scad = translate([idx * rocket.engine_mount.outer_dia * 1.1,0,0])(scad)
        slist.append(scad)
    scad = union()(slist)
    f = open("engine_mount_panel.scad", 'w')
    f.write(scad_render(scad))

def make_collar_test():
    rocket = Rockit(RockitConstants, RockitEngineMount, Rockit_Mini_Engine, RockitBody, RockitCollar, RockitCollarTest)
    rocket.body.height = 10
    rocket.collar.height = 5
    pprint.pprint(rocket)
    scad = rocket.collar_test.build()
    fn = "collar_test"
    save(scad, fn)
#make_collar_test()

def make_tail(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, override=override)
    pprint.pprint(rocket)
    scad = rocket.tail.build()
    name = "tail"
    save(scad, name)
make_tail()

