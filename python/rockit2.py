# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
import traceback
import pprint
from solid import *

# scad
def tube(name, length, outer_dia, inner_dia, segments=None):
    msg = "Tube [%s]: Dia: inner=%.4f outer=%.4f, Length: %.4f" % (name, inner_dia, outer_dia, length)
    print msg
    return difference() (
        cylinder(h=length, r=outer_dia / 2, segments=segments),
        cylinder(h=length, r=inner_dia / 2, segments=segments)
    )

def tube2(name, length, outer_dia1, inner_dia1, outer_dia2, inner_dia2, segments=None):
    msg = "Tube2 [%s]: Dia1: inner=%.4f outer=%.4f, Dia2: inner=%.4f outer=%.4f, Length: %.4f" % (name, inner_dia1, outer_dia1, inner_dia2, outer_dia2, length)
    print msg
    return difference() (
        cylinder(h=length, r1=outer_dia1 / 2, r2=outer_dia2 / 2, segments=segments),
        cylinder(h=length, r1=inner_dia1 / 2, r2=inner_dia2 / 2, segments=segments),
    )

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
    Defaults = {"rockit": None}
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

class RockitConstants(RockitPart):
    Name = 'constants'

    Defaults = {
        "min_overlap": .001,
        "circle_segments": 30
    }

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
        # .07 felt a little too tight, and .08 felt a little too loose
        "fit": 1.075,
        "length": in2mm(1.75),
        "dia": in2mm(.5),
    }

class Rockit_Standard_Engine(RockitEngine):
    Defaults = {
        "length": in2mm(2.75),
        "dia": in2mm(.69),
    }

class Rockit_D_Engine(RockitEngine):
    Defaults = {
        "length": in2mm(2.75),
        "dia": in2mm(.95),
    }

class Rockit_E_Engine(RockitEngine):
    Defaults = {
        "length": in2mm(3.75),
        "dia": in2mm(.69),
    }

class EngineHolder(RockitPart):
    Name = 'engine_mount'
    Defaults = {
        "length": in2mm(3.75),
        "firewall_length": in2mm(.25),
        "offset": None,
        "inner_dia": None,
        "outer_dia": None,
        "taper_length": None,
        "taper_inner_dia": None,
        "taper_outer_dia": None,
    }

    @default
    def inner_dia(self):
        return self.rocket.engine.dia * self.rocket.engine.fit

    @default
    def outer_dia(self):
        return self.inner_dia + self.rocket.body.thickness

    @default
    def taper_length(self):
        return self.rocket.collar.length

    @default
    def taper_inner_dia(self):
        return self.rocket.body.inner_dia

    @default
    def taper_outer_dia(self):
        return self.rocket.body.outer_dia

    def build(self):
        # assume we have been translated to the correct length (collar, offset, etc)
        return union()(
            # engine mount taper
            tube2("engine tube", self.taper_length, self.taper_outer_dia, self.taper_inner_dia, self.outer_dia, self.inner_dia),
            # engine mount tube
            translate([0, 0, self.taper_length])( 
                tube("engine tube", self.length, self.outer_dia, self.inner_dia),
            )
            # engine firewall
            #translate([0, 0, self.offset + self.length])( tube("engine firewall", self.firewall_length, self.rocket.body.outer_dia, self.inner_dia) ),
        )

class RockitCollar(RockitPart):
    Name = 'collar'
    Defaults = {
        "length": None,
        "fit": .990,
        "overlap": None,
        "outer_dia": None,
        "inner_dia": None,
    }

    @default
    def length(self):
        return self.rocket.constants.min_overlap + in2mm(.35)

    @default
    def inner_dia(self):
        return self.outer_dia - self.rocket.body.thickness

    @default
    def outer_dia(self):
        return self.rocket.body.inner_dia + self.fit

class RockitBody(RockitPart):
    Name = 'body'
    Defaults = {
        "thickness": 2,
        "length": None,
        "inner_dia": None,
        "outer_dia": None,
    }

    @default
    def length(self):
        return 2 * self.rocket.engine_mount.length + self.rocket.engine_mount.offset

    @default
    def inner_dia(self):
        return self.rocket.engine.dia + self.rocket.engine.gap

    @default
    def outer_dia(self):
        return self.rocket.body.inner_dia + self.rocket.body.thickness

def engine_mount_test():
    override = {}
    override["engine_mount.length"] = 10
    override["engine_mount.taper_length"] = 0
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, EngineHolder, RockitBody, RockitCollar, override=override)
    pprint.pprint(rocket)
    f = open("engine_mount_test.scad", 'w')
    scad = rocket.engine_mount.build()
    f.write(scad_render(scad))

def make_engine_panel():
    override = {}
    override["engine_mount.length"] = 10
    override["engine_mount.taper_length"] = 0
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, EngineHolder, RockitBody, RockitCollar, override=override)
    slist = []
    for (idx, x) in enumerate(range(10)):
        x += 3
        x = x / 100.0 + 1
        print x
        rocket.engine.fit = x
        pprint.pprint(rocket)
        scad = rocket.engine_mount.build()
        scad = translate([idx * rocket.engine_mount.outer_dia * 1.1,0,0])(scad)
        slist.append(scad)
    scad = union()(slist)
    f = open("engine_mount_panel.scad", 'w')
    f.write(scad_render(scad))

make_engine_panel()
