# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
from solid import *
from . parts import *
import pprint

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

def make_mini_nosecone(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, RockitNosecone, override=override)
    pprint.pprint(rocket)
    scad = rocket.nosecone.build()
    name = "mini_nosecone"
    save(scad, name)

def make_mini_tube(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, RockitNosecone, override=override)
    pprint.pprint(rocket)
    scad = rocket.body.build()
    name = "mini_tube"
    save(scad, name)

def make_mini_tail(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Mini_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, override=override)
    pprint.pprint(rocket)
    scad = rocket.tail.build()
    name = "mini_tail"
    save(scad, name)

def make_standard_tail(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Standard_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, override=override)
    pprint.pprint(rocket)
    scad = rocket.tail.build()
    name = "standard_tail"
    save(scad, name)

def make_standard_tube(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Standard_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, RockitNosecone, override=override)
    pprint.pprint(rocket)
    scad = rocket.body.build()
    name = "standard_tube"
    save(scad, name)

def make_standard_nosecone(oride=None):
    override = oride or dict()
    rocket = Rockit(RockitConstants, Rockit_Standard_Engine, RockitEngineMount, RockitBody, RockitCollar, RockitTail, RockitFin, RockitLaunchLug, RockitNosecone, override=override)
    pprint.pprint(rocket)
    scad = rocket.nosecone.build()
    name = "standard_nosecone"
    save(scad, name)
