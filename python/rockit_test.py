#!/usr/bin/env python

from rockit import *

class RedRockit(RockitParts):
    DefaultList = [
        RockitGlobal,
        RockitNosecone,
        RockitBody,
        RockitBodyStandoff,
        RockitCollar,
        RockitGuide,
        RockitFin,
        RockitFinStandoff,
        RockitFinSkirt,
        Rockit_Standard_Engine,
    ]
    Defaults = {cls.Name: cls for cls in DefaultList}

rr = RedRockit()
ns = rr.ns()
print rr.body.outer_dia
print rr.body.thickness
print rr.body.inner_dia
#print rr.scad(["finstandoff"])
