# Rockit - Model Rocket Construction Kit
# Giles Hall (C) 2013
from solid import *
from . rockit import *
from . nosecone import *
import logging

logger = logging.getLogger(__name__)

CIRCLE_SEGMENTS = 200

class RockitEngine(RockitPart):
    Name = 'engine'

    Defaults = {
        "fit": 1.02,
        "gap": in2mm(.5)
    }

    EngineTypes = {
        "mini_engine": {
            "fit": 1.08,
            "height": in2mm(1.75),
            "dia": in2mm(.5),
        },
        "standard_engine": {
            "fit": 1.08,
            "height": in2mm(2.75),
            "dia": in2mm(.69),
        },
        "d_engine": {
            "height": in2mm(2.75),
            "dia": in2mm(.95),
        },
        "e_engine": {
            "height": in2mm(3.75),
            "dia": in2mm(.69),
        },
    }

    def __init__(self, rocket, **kw):
        _dct = kw.copy()
        if "type" in kw:
            engine_type = _dct["type"]
            engine_conf = self.EngineTypes[engine_type]
            _dct.update(engine_conf)
        _dct.update(kw)
        super(RockitEngine, self).__init__(rocket, **_dct)

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

    def render_scad(self):
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

    def render_scad(self):
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

    def render_scad(self):
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

    def render_scad(self):
        scad = polyhedron(points=self.points, triangles=self.triangles)
        return scad

class RockitTail(RockitPart):
    Name = 'tail'
    Defaults = {
        "fin_count": 4,
    }

    def render_scad(self):
        parts = []
        # rocket body 
        parts.append(self.rocket.body.render_scad())
        # engine mount
        parts.append(self.rocket.engine_mount.render_scad())
        # fins
        for finidx in range(self.fin_count):
            z_angle = finidx * (360.0 / self.fin_count)
            part = rotate([0,0,z_angle])( self.rocket.fin.render_scad() )
            parts.append(part)
        # launch lug
        z_angle = (360.0 / self.fin_count) / 2.0
        part = rotate([0,0,z_angle])( self.rocket.launchlug.render_scad() )
        parts.append(part)
        return union()(parts)

class RockitCollarTest(RockitPart):
    Name = 'collar_test'

    def render_scad(self):
        return union()(
            union()(
                self.rocket.body.render_scad(),
                self.rocket.collar.render_scad(),
            ),
            translate([self.rocket.body.outer_dia * 1.1,0,0]) (
                union()(
                    self.rocket.body.render_scad(),
                    self.rocket.collar.render_scad(),
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

    def render_scad(self):
        return union()(
            tube("body", self.height, self.outer_dia, self.inner_dia, self.rocket.constants.circle_segments),
            self.rocket.collar.render_scad(),
        )

class RockitConstants(RockitPart):
    Name = 'constants'

    Defaults = {
        "min_overlap": .001,
        "circle_segments": CIRCLE_SEGMENTS,
    }

class RockitNosecone(RockitPart):
    Name = 'nosecone'

    Defaults = {
        "height": None,
        "width": None,
        "inner_dia": None,
        "outer_dia": None,
        "mount_height": None,
        "steps": 100,
    }

    @default
    def height(self):
        return self.rocket.body.height

    @default
    def width(self):
        return self.rocket.body.width

    @default
    def inner_dia(self):
        return self.rocket.body.inner_dia

    @default
    def outer_dia(self):
        return self.rocket.body.outer_dia

    @default
    def mount_height(self):
        return self.rocket.collar.height + 1

    def render_scad(self):
        points = elliptical_nosecone_func(height=self.height, width=self.width, diameter=self.outer_dia, steps=self.steps)
        #return rotate_extrude(convexity=10, segments=self.rocket.constants.circle_segments)( rotate([0, 0, -90])( polygon(points)))
        return union()(
            rotate_extrude(convexity=10, segments=self.rocket.constants.circle_segments)( rotate([0, 0, -90])( polygon(points))),
            translate([0, 0, -self.mount_height])(
                translate([0, -self.inner_dia / 2.0 + self.rocket.constants.min_overlap, 0])(
                    rotate([-90, 0, 0])(
                        cylinder(h=self.inner_dia, r=self.rocket.body.width / 2.0, segments=self.rocket.constants.circle_segments),
                    )),
                translate([self.inner_dia / 2.0 - self.rocket.constants.min_overlap, 0, 0])(
                    rotate([0, -90, 0])(
                        cylinder(h=self.inner_dia, r=self.rocket.body.width / 2.0, segments=self.rocket.constants.circle_segments),
                    )),
            ))

