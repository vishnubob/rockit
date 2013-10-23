# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
import traceback
import pprint
from scad import *

def in2mm(inches):
    return inches / 0.0393701

class RockitPart(dict):
    Defaults = {}
    Name = ''

    def __init__(self, bound=None, **kw):
        self.name = self.Name or self.__class__.__name__
        self.bound = bound
        _dct = self.Defaults.copy()
        _dct.update(kw)
        super(RockitPart, self).__init__(**_dct)

    def copy(self):
        return self.__class__(bound=self.bound, **super(RockitPart, self).copy())

    def __repr__(self):
        code = "%s(**%s)" % (self.__class__.__name__, str(dict(self)))
        return code

    def bind(self, ns=None):
        self.bound = ns

    def localize_key(self, key):
        if key.startswith(self.name + '_') or key.startswith(self.name + '.'):
            return key[len(self.name) + 1:]
        return key

    def __getattr__(self, key):
        return super(RockitPart, self).__getitem__(key)

    def __setattr__(self, key, val):
        if super(RockitPart, self).__contains__(key):
            super(RockitPart, self).__setitem__(key, val)
        else:
            super(RockitPart, self).__setattr__(key, val)

    def __contains__(self, key):
        key = self.localize_key(key)
        return super(RockitPart, self).__contains__(key)

    def __getitem__(self, okey):
        key = self.localize_key(okey)
        print "__getitem__", okey
        ret = super(RockitPart, self).__getitem__(key)
        if self.bound:
            print "bound"
            if type(ret) == str:
                try:
                    print "Trying", ret
                    ret = eval(ret, self.bound)
                except:
                    pass
        return ret

    def __contains__(self, key):
        key = self.localize_key(key)
        return super(RockitPart, self).__contains__(key)

    def __setitem__(self, key, item):
        key = self.localize_key(key)
        super(RockitPart, self).__setitem__(key, item)

    def fq_keys(self):
        return [self.name + '_' + key for key in self.keys()]

    def scad_variables(self):
        banner = '#' * 80 + '\n'
        scad = banner + "## %s - Variables\n" % self.__class__.__name__
        scad += str.join('', ["%s=%s;\n" % (key, val) for (key, val) in self.items()])
        scad += '\n'
        return scad

    def scad_modules(self):
        banner = '#' * 80 + '\n'
        scad = banner + "## %s - Modules\n" % self.__class__.__name__
        scad += '\n'
        return scad

    def scad(self):
        try:
            return scad_variables() + scad_modules()
        except:
            traceback.print_exc()
            raise

class RockitParts(RockitPart):
    def __init__(self, *args, **kw):
        super(RockitParts, self).__init__(*args, **kw)
        print self
        self.update({name: self[name]() for name in self if not isinstance(self[name], RockitPart) and type(self[name]) not in (str,int,float,list)})

    def scad(self, parts=[]):
        #print
        #print [(key, self[key]) for key in self]
        #print
        scad = ''
        parts = parts or self.keys()
        for partname in parts:
            part = self[partname]
            scad += part.scad_variables()
            self["current_part"] = part
            scad += eval("current_part.scad_module()", self.ns(), locals())
        return scad

    def bind(self, ns=None):
        for pname in self:
            self[pname].bind(ns)
        super(RockitParts, self).bind(ns)

    def fq_keys(self):
        ret = []
        map(ret.extend, [part.fq_keys() for part in self.values()])
        return ret

    def symbol_lock(self, symbol, ns):
        if type(symbol) != str:
            return
        while 1:
            try:
                try:
                    new_sym = eval(symbol, ns)
                except:
                    break
                if new_sym != symbol:
                    symbol = new_sym
                else:
                    break
            except:
                pass
        return symbol

    def ns(self):
        ns = {key: self[key] for key in self.fq_keys()}
        ns = self.__class__(**ns)
        ns.update({key: self[key] for key in self.keys()})
        resolved = set([key for key in ns if type(ns[key]) != str])
        unresolved = set(ns.keys()).difference(resolved)
        loopcnt = 0
        while unresolved:
            loopcnt += 1
            ur = len(unresolved)
            for key in unresolved:
                _ns = ns.copy()
                _ns.update(globals())
                _ns.update(locals())
                self.bind(_ns)
                try:
                    print "EVAL: %s = eval(%s)" % (key, ns[key])
                    if type(_ns[key]) == str:
                        ret = eval(str(_ns[key]), _ns)
                        ns[key] = ret
                        print "ret: ", ret
                        if type(ret) != str:
                            print "EVAL: %s = %s = eval(%s)" % (key, ret, ns[key])
                    resolved.add(key)
                    #print "ret", key, ret
                except Exception, e:
                    #print
                    #print "eval", key, '"%s"' % _ns[key]
                    #print
                    traceback.print_exc()
                    print e
                    print
                    continue
                print
                unresolved = unresolved.difference(resolved)
            #pprint.pprint(ns)
            #print
            if (ur == len(unresolved)):
                print "Early Break!"
                break
        self.bind()
        ns = {key: _ns[key] for key in ns}
        msg = "Loop: %d passed with %d resolved, %d unresolved" % (loopcnt, len(resolved), len(unresolved))
        print unresolved
        print msg
        return ns

    def get_part(self, key):
        for partname in self:
            part = super(RockitParts, self).__getitem__(partname)
            if partname == key.split('_')[0]:
                print "get_part", partname, key
                return part
        raise KeyError, key

    def has_part(self, key):
        try:
            self.get_part(key)
        except KeyError:
            return False
        return True

    def __getitem__(self, key):
        if super(RockitParts, self).__contains__(key):
            return super(RockitParts, self).__getitem__(key)
        return self.get_part(key)[key]

    def __contains__(self, key):
        return self.has_part(key)

    def __setitem__(self, key, item):
        try:
            part = self.get_part(key)
            part[key] = item
        except KeyError:
            super(RockitParts, self).__setitem__(key, item)

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
        "inner_dia": "engine.dia * engine.fit",
        "outer_dia": "engineholder.inner_dia + body.thickness",
        "firewall_length": in2mm(.25),
        "engineholder_offset": "collar.height",
    }

class RockitGlobal(RockitPart):
    Name = 'global'
    Defaults = {
        "min_overlap": .001,
        "circle_segments": 30
    }

class RockitBody(RockitPart):
    Name = 'body'
    Defaults = {
        "thickness": 2,
        "height": "engineholder.length + 2 * engineholder.offset",
        "inner_dia": "engine.dia + engine.gap",
        "outer_dia": "body.inner_dia + body.thickness",
    }

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
