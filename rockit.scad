// Rockit - Model Rocket Construction Kit
//
// Giles Hall (C) 2012,2013
//
// Tail fin code based on:
// - Lutz Paelke (lpaelke) - http://www.thingiverse.com/thing:26508/

function in2mm(in) = in / 0.0393701;

/////////////////
// Engine Dimensions
// http://www2.estesrockets.com/pdf/Estes_Model_Rocket_Engines.pdf
// mini engine
mini_engine_pad = 0.2;
mini_engine_gap = in2mm(.5);
mini_engine_length = in2mm(1.75);
mini_engine_dia = in2mm(.5);
// standard engine
standard_engine_pad = 0.2;
standard_engine_gap = in2mm(.5);
standard_engine_length = in2mm(2.75);
standard_engine_dia = in2mm(.69);
// D engine
d_engine_pad = 0.2;
d_engine_gap = in2mm(1);
d_engine_length = in2mm(2.75);
d_engine_dia = in2mm(.95);
// E engine
e_engine_pad = 0.2;
e_engine_gap = in2mm(.5);
e_engine_length = in2mm(3.75);
e_engine_dia = in2mm(.95);
// engine selection
engine_length = standard_engine_length;
engine_dia = standard_engine_dia;
engine_gap = standard_engine_gap;
engine_pad = standard_engine_pad;

/////////////////
// Global
wall_thickness = 2;
collar_height = in2mm(.25);

/////////////////
// Engine Holder
engine_holder_enabled = 1;
engine_holder_overhang = 20;
engine_holder_inner_dia = engine_dia + engine_pad;
engine_holder_outer_dia = engine_dia + wall_thickness;
engine_holder_length = engine_length + engine_pad;
engine_holder_offset = collar_height;
engine_holder_firewall_length = in2mm(.25);

/////////////////
// Body
body_enabled = 1;
//body_height = engine_holder_length + engine_holder_offset + engine_holder_offset + in2mm(.2);
body_height = engine_holder_length + engine_holder_offset + engine_holder_offset;
body_inner_dia = engine_dia + engine_gap;
body_outer_dia = body_inner_dia + wall_thickness;

/////////////////
// Fins
fins_enabled = 1;
fin_count = 6;
fin_span = body_outer_dia * 3.5;
fin_thickness = wall_thickness;
fin_endchord = body_height * .6;
fin_sym_flag = 1;
//fin_offset = fin_endchord;
fin_offset = 0;
fin_coverage = .99;
fin_height = (body_height - fin_offset) * fin_coverage;

/////////////////
// Collar
collar_enabled = 1;
collar_overlap = collar_height * .5;
collar_fit = .990;
collar_outer_dia = body_inner_dia * collar_fit;
collar_inner_dia = collar_outer_dia - wall_thickness;

/////////////////
// Guide
guide_enabled = 1;
guide_inner_dia = 4.6;
guide_outer_dia = guide_inner_dia + 1;
guide_height = in2mm(2);
guide_offset = in2mm(.5);

/////////////////
// Quality
circle_segments = 30;

module fin(angle, deflection)
{
    translate([0,0,fin_offset])
    rotate([0,0,angle])
        polyhedron(points=[
        // inner-bottom
        [body_inner_dia / 2, fin_thickness / 2 + deflection, 0], 
        [body_inner_dia / 2, -fin_thickness / 2 + deflection, 0],
        // outer-bottom
        [fin_span / 2, fin_thickness / 2 + deflection, fin_sym_flag ? -fin_endchord : 0], 
        [fin_span / 2, -fin_thickness / 2 + deflection, fin_sym_flag ? -fin_endchord : 0],
        // outer-top
        [fin_span / 2, fin_thickness / 2 - deflection, fin_height - fin_endchord], 
        [fin_span / 2, -fin_thickness / 2 - deflection, fin_height - fin_endchord],
        // inner-top
        [body_inner_dia / 2, fin_thickness / 2 - deflection, fin_height],
        [body_inner_dia / 2, -fin_thickness / 2 - deflection, fin_height]],
        triangles=[[0, 1, 2],  [1, 3, 2], 
                    [2, 3, 4],  [3, 5, 4], 
                    [4, 5, 6],  [5, 7, 6], 
                    [6, 7, 0],  [7, 1, 0], 
                    [0, 2, 6],  [2, 4, 6], 
                    [1, 7, 3],  [3, 7, 5]]);
}

module tube(name, length, outer_dia, inner_dia)
{
    echo(str("Tube [", name, "]: ", length, "mm len, ", outer_dia, "mm OD, ", inner_dia, "mm ID"));
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
    echo(str("Tube2 [", name, "]: ", length, "mm len, ", outer_dia, "mm OD, ", inner_dia, "mm ID"));
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
    if (guide_enabled)
    {
		rotate([0, 0, 180 / fin_count]) 
        translate([body_outer_dia / 2 + guide_inner_dia / 2, 0, guide_offset])
        tube("guide", guide_height, guide_outer_dia, guide_inner_dia);
    }
}

module make_fins() 
{
    if (fins_enabled)
    {
		for (i = [0:fin_count - 1])
        {
            fin(i * (360 / fin_count), 0);
        }
    }
}

module make_collar()
{
    if (collar_enabled)
    {
        translate([0, 0, body_height - collar_overlap]) 
        tube("collar", collar_height + collar_overlap, collar_outer_dia, collar_inner_dia);
    }
}

module make_engine_holder()
{
    if (engine_holder_enabled)
    {
        union()
        {
            // engine offset
            translate([0, 0, engine_holder_offset * 2])
            tube("engine tube", engine_holder_length, engine_holder_outer_dia, engine_holder_inner_dia);
            // engine collar
            translate([0, 0, engine_holder_offset])
            tube2("engine tube", engine_holder_offset, body_outer_dia, body_inner_dia, engine_holder_outer_dia, engine_holder_inner_dia);
            // engine firewall
            translate([0, 0, engine_holder_offset + engine_holder_length])
            tube("engine firewall", engine_holder_firewall_length, body_outer_dia, engine_holder_inner_dia);
        }
    }
}

module make_body()
{
    if (body_enabled)
    {
        tube("body", body_height, body_outer_dia, body_inner_dia);
    }
}

module make_rocket()
{
    union()
    {
        // outer
        make_body();
        make_collar();
        make_guide();
        make_fins();
        make_engine_holder();
    }
}
