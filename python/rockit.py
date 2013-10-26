# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
import traceback
import pprint
from solid import *

def in2mm(inches):
    return inches / 0.0393701

class RockitPart(dict):
    Defaults = {}
    Name = ''

    def __init__(self, **kw):
        self.name = self.Name or self.__class__.__name__
        self.__ns = None
        _dct = self.Defaults.copy()
        _dct.update(kw)
        super(RockitPart, self).__init__(**_dct)

    def copy(self):
        newcopy = self.__class__(self)
        newcopy.bind(self.__ns)
        return newcopy

    def bind(self, ns):
        self.__ns = ns

    def lookup(self, key):
        return self.__ns[key]
        
    def build(self):
        pass

    def __getattr__(self, key):
        if key not in self:
            raise AttributeError, key
        return self[key]

    def __setattr__(self, key, val):
        if key in self:
            self[key] = val
        else:
            super(RockitPart, self).__setattr__(key, val)

class RockitParts(object):
    def __init__(self, *parts):
        self.parts = list(parts)
        self.refresh_catalog()

    def refresh_parts_catalog(self):
        self.catalog = {}
        for part in self.parts:
            part.bind(self)
            self.catalog[part.name] = part

    def add_part(self, part):
        self.parts.append(part)
        self.refresh_catalog()

    def __getitem__(self, key):
        keys = key.split('.')
        attr = keys[-1]
        part = None
        for key in keys[:-1]:
            if part == None:
                part = self.catalog[key]
            else:
                part = part[key]
        return part[attr]

class RockitGlobal(RockitPart):
    Name = 'global'
    Defaults = {
        "min_overlap": .001,
        "circle_segments": 30
    }

class RockitEngine(RockitPart):
    Name = 'engine'

    Defaults = {
        "length": 0,
        "dia": 0,
        "fit": 1.02,
        "gap": in2mm(.5)
    }

class Rockit_Mini_Engine(RockitEngine):
    Defaults = {
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
    Name = 'engineholder'
    Defaults = {
        "length": in2mm(3.75),
        "firewall_length": in2mm(.25),
    }

    @property
    def offset(self):
        return self.lookup("collar.height")

class RockitBody(RockitPart):
    Name = 'body'
    Defaults = {
        "thickness": 2,
        "inner_dia": "engine.dia + engine.gap",
        "outer_dia": "body.inner_dia + body.thickness",
    }

    @property
    def length(self):
        if "length" not in self:
            
        "height": "engineholder.length + 2 * engineholder.offset",

class RockitBodyStandoff(RockitPart):
    Name = 'bodystandoff'
    Defaults = {
        "thickness": "body.thickness",
        "neck_dia": "body.thickness / 2",
        "air_gap": "bodystandoff.neck_dia * .61"
    }

class RockitCollar(RockitPart):
    Name = 'collar'
    Defaults = {
        "height": in2mm(.35),
        "overlap": "collar.height",
        "fit": .990,
        "outer_dia": "body.inner_dia * collar.fit",
        "inner_dia": "collar.outer_dia - body.thickness",
    }

class RockitFin(RockitPart):
    Name = 'fin'
    Triangles = [[0, 1, 2],  [1, 3, 2], [2, 3, 4],  
                    [3, 5, 4], [4, 5, 6], [5, 7, 6], 
                    [6, 7, 0], [7, 1, 0], [0, 2, 6], 
                    [2, 4, 6], [1, 7, 3],  [3, 7, 5]]
    Defaults = {
        "count": 6,
        "dia": "body.outer_dia * 3.5",
        "thickness": "body.thickness",
        "endchord": "body.height * .21",
        "sym_flag": 1,
        "offset": 0,
        "coverage": .99,
        "height": "(body.height - fin.offset) * fin.coverage",
        "deflection": 0,
        "length": "fin.dia / 2 - body.outer_dia / 2",
        "triangles": Triangles,
    }

    def scad_module(self):
        return module(self.__class__.__name__, [
            translate([0,0,fin_offset]),
                rotate([0,0,angle]),
                    polyhedron(points=[
                        # inner-bottom
                        [body_outer_dia / 2 - min_overlap, fin_thickness / 2 + deflection, 0], 
                        [body_outer_dia / 2 - min_overlap, -fin_thickness / 2 + deflection, 0],
                        # outer-bottom
                        [fin_dia / 2, fin_thickness / 2 + deflection, [-fin_endchord, 0]][bool(fin_sym_flag)],
                        [fin_dia / 2, -fin_thickness / 2 + deflection, [-fin_endchord, 0]][bool(fin_sym_flag)],
                        # inner-top
                        [fin_dia / 2, fin_thickness / 2 - deflection, fin_height - fin_endchord], 
                        [fin_dia / 2, -fin_thickness / 2 - deflection, fin_height - fin_endchord],
                        # outer-top
                        [body_outer_dia / 2 - min_overlap, fin_thickness / 2 - deflection, fin_height],
                        [body_outer_dia / 2 - min_overlap, -fin_thickness / 2 - deflection, fin_height]],
                        # triangles
                        triangles=fin_triangles)])


class RockitFinSkirt(RockitPart):
    Name = 'finskirt'
    Defaults = {
        "height": .5,
        "width": "body.outer_dia"
    }

class RockitFinStandoff(RockitPart):
    Name = 'finstandoff'
    Defaults = {
        "thickness": "fin.thickness",
        "neck_dia": "body.thickness / 2",
        "air_gap_factor": .61,
        "air_gap": "finstandoff.neck_dia * finstandoff.air_gap_factor",
    }

    def scad_module(self):
        return module("make_finstandoff", ["angle"], [
            #translate([0, 0, global.stage_offset]),
            rotate([0,0,"angle"]),
            union([
                polyhedron(points=[ 
                    # inner-bottom
                    [body_outer_dia / 2 - min_overlap, fin_thickness / 2 + deflection, 0], 
                    [body_outer_dia / 2 - min_overlap, -fin_thickness / 2 + deflection, 0],
                    # outer-bottom
                    [fin_dia / 2 - max(0, finstandoff_air_gap), fin_thickness / 2 + deflection, 0], 
                    [fin_dia / 2 - max(0, finstandoff_air_gap), -fin_thickness / 2 + deflection, 0],
                    # outer-top
                    [fin_dia / 2 - max(0, finstandoff_air_gap), fin_thickness / 2.0 - deflection, 0],
                    [fin_dia / 2 - max(0, finstandoff_air_gap), -fin_thickness / 2.0 - deflection, 0],
                    # inner-top
                    [body_outer_dia / 2 - min_overlap, fin_thickness / 2.0 - deflection, fin_endchord - finstandoff_air_gap],
                    [body_outer_dia / 2 - min_overlap, -fin_thickness / 2.0 - deflection, fin_endchord - finstandoff_air_gap]],
                    # triangles
                    triangles=fin_triangles),
                # neck
                translate([fin_dia / 2 - max(0, finstandoff_air_gap), 0, 0], 
                [
                    rotate([0, -atan2(fin.length - finstandoff.air_gap, fin.endchord - finstandoff.air_gap), 0], 
                    [
                        difference(
                        [
                            linear_extrude(height=(fin_dia - body_outer_dia) / 2), 
                                circle(r=finstandoff_neck_dia / 2, fn=circle_segments),
                            translate([-1, -fin_thickness / 2, 0]), 
                                cube([1, fin_thickness, fin_dia / 2])
                        ]),
                    ]),
                ]),
                #color([255, 0, 0]),
                #translate([-1, -fin.thickness / 2, 0]),
                #   cube([1, fin.thickness, fin_dia / 2]),
            ]),
        ])


class RockitGuide(RockitPart):
    Name = 'guide'
    Defaults = {
        "inner_dia": 4.6,
        "outer_dia": "guide_inner_dia + body.thickness",
        "height": in2mm(2),
        "offset": in2mm(.5),
    }

class RockitNosecone(RockitPart):
    Name = 'nosecone'
    Defaults = {
        "inner_dia": 4.6,
        "outer_dia": "guide_inner_dia + body.thickness",
        "height": in2mm(2),
        "offset": in2mm(.5),
    }


"""

module tube(name, length, outer_dia, inner_dia)
{
    echo(str("   Tube [", name, "]: ", length, "mm len, ", outer_dia, "mm OD, ", inner_dia, "mm ID"));
    difference()
    {
        // outer
        cylinder(h=length, r=outer_dia / 2, $fn=circle_segments);
        // inner
        cylinder(h=length, r=inner_dia / 2, $fn=circle_segments);
    }
}

module tube2(name, length, outer_dia1, inner_dia1, outer_dia2, inner_dia2)
{
    echo(str("    Tube2 [", name, "]: ", length, "mm len, ", outer_dia1, "mm OD1, ", inner_dia1, "mm ID1 ", outer_dia2, "mm OD2, ", inner_dia2, "mm ID2"));
    difference()
    {
        // outer
        cylinder(h=length, r1=outer_dia1 / 2, r2=outer_dia2 / 2, $fn=circle_segments);
        // inner
        cylinder(h=length, r1=inner_dia1 / 2, r2=inner_dia2 / 2, $fn=circle_segments);
    }
}

module make_guide() 
{
    echo(str("Making guide"));
    rotate([0, 0, 180 / fin_count]) 
    translate([body_outer_dia / 2 + guide_inner_dia / 2, 0, guide_offset])
    tube("guide", guide_height, guide_outer_dia, guide_inner_dia);
}

module make_fins() 
{
    echo(str("Making fins"));
    for (i = [0:fin_count - 1])
    {
        make_fin(i + 1, i * (360 / fin_count), fin_deflection);
    }
    union()
    {
        if (finskirt_enabled)
        {
            translate([0, 0, -stage_offset()])
            tube("fin skirt", finskirt_height, fin_dia + (finskirt_width / 2), fin_dia - (finskirt_width / 2));
            echo(str("Making fins"));
        }
        for (i = [0:fin_count - 1])
        {
            make_fin(i + 1, i * (360 / fin_count), fin_deflection);
            make_finstandoff(i + 1, i * (360 / fin_count), fin_deflection);
        }
    }
}

module make_collar()
{
    echo(str("Making collar"));
    translate([0, 0, body_height - collar_overlap]) 
    tube("collar", collar_height + collar_overlap, collar_outer_dia, collar_inner_dia);
}

module make_engineholder()
{
    echo(str("Making engine holder"));
    union()
    {
        // engine offset
        translate([0, 0, engineholder_offset * 2])
        tube("engine tube", engineholder_length, engineholder_outer_dia, engineholder_inner_dia);
        // engine collar
        translate([0, 0, engineholder_offset])
        tube2("engine tube", engineholder_offset, body_outer_dia, body_inner_dia, engineholder_outer_dia, engineholder_inner_dia);
        // engine firewall
        translate([0, 0, engineholder_offset + engineholder_length])
        tube("engine firewall", engineholder_firewall_length, body_outer_dia, engineholder_inner_dia);
    }
}

module make_body()
{
    echo(str("Making body"));
    midpoint = (body_outer_dia - body_inner_dia) / 2 + body_inner_dia;
    union()
    {
        // body
        tube("body", body_height, body_outer_dia, body_inner_dia);
        // standoff
        if (bodystandoff_enabled)
        {
            // base
            translate([0, 0, -stage_offset()])
                tube("body standoff base", stage_offset() - bodystandoff_air_gap, 
                    midpoint + bodystandoff_thickness / 2, 
                    midpoint - bodystandoff_thickness / 2);
            // neck
            translate([0, 0, -bodystandoff_air_gap])
                rotate_extrude(convexity=10, $fn=circle_segments)
                    translate([midpoint / 2, 0, 0])
                        circle(r=bodystandoff_neck_dia / 2, $fn=circle_segments);
        }
    }
}

module make_nosecone()
{
    echo(str("Making nosecone"));
    tube("nosecone", nosecone_height, nosecone_inner_dia, nosecone_outer_dia);
}

module make_rockit_nosecone()
{
    make_nosecone();
}

module make_rockit_tail()
{
    union()
    {
        translate([0, 0, stage_offset()])
        {
            make_engineholder();
            make_guide();
            make_body();
            make_collar();
            make_fins();
        }
    }
}

module make_rockit_tube()
{
    union()
    {
        make_body();
        make_collar();
    }
}
"""
