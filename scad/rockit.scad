// Rockit - Model Rocket Construction Kit
//
// Giles Hall (C) 2012,2013
//
// Tail fin code based on:
// - Lutz Paelke (lpaelke) - http://www.thingiverse.com/thing:26508/

/////////////////
// Functions 
function in2mm(in) = in / 0.0393701;
//function stage_offset() = (fin_sym_flag ? fin_endchord : 0) + (fin_skirt_enabled ? fin_skirt_height : 0);
function stage_offset() = 0;

/////////////////
// Engine Dimensions
// http://www2.estesrockets.com/pdf/Estes_Model_Rocket_Engines.pdf
// mini engine
mini_engine_length = in2mm(1.75);
mini_engine_dia = in2mm(.5);
mini_engine_fit = 1.02;
mini_engine_gap = in2mm(.5);
// standard engine
standard_engine_length = in2mm(2.75);
standard_engine_dia = in2mm(.69);
standard_engine_fit = 1.02;
standard_engine_gap = in2mm(.5);
// D engine
d_engine_length = in2mm(2.75);
d_engine_dia = in2mm(.95);
d_engine_fit = 1.02;
d_engine_gap = in2mm(1);
// E engine
e_engine_length = in2mm(3.75);
e_engine_dia = in2mm(.95);
e_engine_fit = 1.02;
e_engine_gap = in2mm(1);
// engine selection
engine_length = standard_engine_length;
engine_dia = standard_engine_dia;
engine_fit = standard_engine_fit;
engine_gap = standard_engine_gap;

/////////////////
// Global
wall_thickness = 2;
min_overlap = .001;
collar_height = in2mm(.35);
circle_segments = 30;

/////////////////
// Engine Holder
engine_holder_inner_dia = engine_dia * engine_fit;
engine_holder_outer_dia = engine_holder_inner_dia + wall_thickness;
engine_holder_length = engine_length * engine_fit;
engine_holder_offset = collar_height;
engine_holder_firewall_length = in2mm(.25);

/////////////////
// Body
body_height = engine_holder_length + engine_holder_offset + engine_holder_offset;
body_inner_dia = engine_dia + engine_gap;
body_outer_dia = body_inner_dia + wall_thickness;
//----------------
// Body Standoff
body_standoff_thickness = wall_thickness;
body_standoff_neck_dia = wall_thickness / 2;
body_standoff_air_gap = body_standoff_neck_dia * .61;

/////////////////
// Fins
fin_count = 4;
fin_dia = body_outer_dia * 3.5;
fin_thickness = wall_thickness;
fin_endchord = body_height * .21;
//fin_sym_flag = 1;
fin_sym_flag = 0;
fin_offset = 0;
fin_coverage = .99;
fin_height = (body_height - fin_offset) * fin_coverage;
fin_deflection = 0;
fin_length = fin_dia / 2 - body_outer_dia / 2;
//----------------
// Fin Skirt
fin_skirt_enabled = 0;
fin_skirt_height = .5;
fin_skirt_width = body_outer_dia;
//----------------
// Fin Standoff
fin_standoff_thickness = fin_thickness;
fin_standoff_neck_dia = wall_thickness / 2;
fin_standoff_air_gap = fin_standoff_neck_dia * .61;

/////////////////
// Collar
collar_overlap = collar_height;
collar_fit = .990;
collar_outer_dia = body_inner_dia * collar_fit;
collar_inner_dia = collar_outer_dia - wall_thickness;

/////////////////
// Guide
guide_inner_dia = 4.6;
guide_outer_dia = guide_inner_dia + 1;
guide_height = in2mm(2);
guide_offset = in2mm(.5);

/////////////////
// Nosecone
nosecone_height = body_height;
nosecone_outer_dia = body_outer_dia;
nosecone_inner_dia = body_inner_dia;
nosecone_outer_rad = nosecone_outer_dia / 2;
nosecone_inner_rad = nosecone_inner_dia / 2;
nosecone_length = body_length;
nosecone_taper = 0.125;



/////////////////
// Post Globals
enable_standoff = (stage_offset() > 0);

module make_fin(name, angle, deflection)
{
    echo(str("    Fin [", name, "]: ", angle, " angle, ", deflection, " deflection"));
    translate([0,0,fin_offset])
    rotate([0,0,angle])
        polyhedron(points=[
        // inner-bottom
        [body_outer_dia / 2 - min_overlap, fin_thickness / 2 + deflection, 0], 
        [body_outer_dia / 2 - min_overlap, -fin_thickness / 2 + deflection, 0],
        // outer-bottom
        [fin_dia / 2, fin_thickness / 2 + deflection, fin_sym_flag ? -fin_endchord : 0], 
        [fin_dia / 2, -fin_thickness / 2 + deflection, fin_sym_flag ? -fin_endchord : 0],
        // outer-top
        [fin_dia / 2, fin_thickness / 2 - deflection, fin_height - fin_endchord], 
        [fin_dia / 2, -fin_thickness / 2 - deflection, fin_height - fin_endchord],
        // inner-top
        [body_outer_dia / 2 - min_overlap, fin_thickness / 2 - deflection, fin_height],
        [body_outer_dia / 2 - min_overlap, -fin_thickness / 2 - deflection, fin_height]],
        triangles=[[0, 1, 2],  [1, 3, 2], 
                    [2, 3, 4],  [3, 5, 4], 
                    [4, 5, 6],  [5, 7, 6], 
                    [6, 7, 0],  [7, 1, 0], 
                    [0, 2, 6],  [2, 4, 6], 
                    [1, 7, 3],  [3, 7, 5]]);
}

module make_fin_standoff(name, angle, deflection)
{
    echo(str("    Fin Standoff [", name, "]: ", angle, " angle, ", deflection, " deflection"));
    translate([0, 0, -stage_offset()])
    rotate([0,0,angle])
    union()
    {
        polyhedron(points=[
        // inner-bottom
        [body_outer_dia / 2 - min_overlap, fin_thickness / 2 + deflection, 0], 
        [body_outer_dia / 2 - min_overlap, -fin_thickness / 2 + deflection, 0],
        // outer-bottom
        [fin_dia / 2 - max(0, fin_standoff_air_gap), fin_thickness / 2 + deflection, 0], 
        [fin_dia / 2 - max(0, fin_standoff_air_gap), -fin_thickness / 2 + deflection, 0],
        // outer-top
        [fin_dia / 2 - max(0, fin_standoff_air_gap), fin_thickness / 2.0 - deflection, 0],
        [fin_dia / 2 - max(0, fin_standoff_air_gap), -fin_thickness / 2.0 - deflection, 0],
        // inner-top
        [body_outer_dia / 2 - min_overlap, fin_thickness / 2.0 - deflection, fin_endchord - fin_standoff_air_gap],
        [body_outer_dia / 2 - min_overlap, -fin_thickness / 2.0 - deflection, fin_endchord - fin_standoff_air_gap]],
        // triangles
        triangles=[[0, 1, 2],  [1, 3, 2], 
                    [2, 3, 4],  [3, 5, 4], 
                    [4, 5, 6],  [5, 7, 6], 
                    [6, 7, 0],  [7, 1, 0], 
                    [0, 2, 6],  [2, 4, 6], 
                    [1, 7, 3],  [3, 7, 5]]);
        // neck
        translate([fin_dia / 2 - max(0, fin_standoff_air_gap), 0, 0])
        {
            // align us down th endchord angle
            rotate([0, -atan2(fin_length - fin_standoff_air_gap, fin_endchord - fin_standoff_air_gap), 0])
            {
                difference()
                {
                    linear_extrude(height=(fin_dia - body_outer_dia) / 2)
                        circle(r=fin_standoff_neck_dia / 2, $fn=circle_segments);
                    translate([-1, -fin_thickness / 2, 0])
                        cube([1, fin_thickness, fin_dia / 2]);
                }
                /*
                color([255, 0, 0])
                translate([-1, -fin_thickness / 2, 0])
                        cube([1, fin_thickness, fin_dia / 2]);
                */
            }
        }
    }
}

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
        if (fin_skirt_enabled)
        {
            translate([0, 0, -stage_offset()])
            tube("fin skirt", fin_skirt_height, fin_dia + (fin_skirt_width / 2), fin_dia - (fin_skirt_width / 2));
            echo(str("Making fins"));
        }
        for (i = [0:fin_count - 1])
        {
            make_fin(i + 1, i * (360 / fin_count), fin_deflection);
            if (stage_offset())
                make_fin_standoff(i + 1, i * (360 / fin_count), fin_deflection);
        }
    }
}

module make_collar()
{
    echo(str("Making collar"));
    translate([0, 0, body_height - collar_overlap]) 
    tube("collar", collar_height + collar_overlap, collar_outer_dia, collar_inner_dia);
}

module make_engine_holder()
{
    echo(str("Making engine holder"));
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

module make_body()
{
    echo(str("Making body"));
    midpoint = (body_outer_dia - body_inner_dia) / 2 + body_inner_dia;
    union()
    {
        // body
        tube("body", body_height, body_outer_dia, body_inner_dia);
        // standoff
        if (stage_offset())
        {
            // base
            translate([0, 0, -stage_offset()])
                tube("body standoff base", stage_offset() - body_standoff_air_gap, 
                    midpoint + body_standoff_thickness / 2, 
                    midpoint - body_standoff_thickness / 2);
            // neck
            translate([0, 0, -body_standoff_air_gap])
                rotate_extrude(convexity=10, $fn=circle_segments)
                    translate([midpoint / 2, 0, 0])
                        circle(r=body_standoff_neck_dia / 2, $fn=circle_segments);
        }
    }
}

module make_nosecone()
{
    echo(str("Making nosecone"));
    union()
    {
        // http://en.wikipedia.org/wiki/Nose_cone_design#Conical
        // y = xR / L
        steps = 100;
        R = body_outer_dia / 2;
        L = nosecone_length;
        x = L - collar_height;
        points = [];
        for (y = [0:steps])
        {
            polygon(points=[
            
        polygon(
            translate ([0, 0, 15]) 
                scale([1, 1, length/(body_inner_dia / 2)]) 
                    difference() 
                    {
                        sphere(r=(body_inner_dia / 2), $fn=circle_segments);
                        translate ([0, 0, -(body_inner_dia / 4)]) 
                            cube(size=[nosecone_inner_dia,nosecone_inner_dia,nosecone_inner_dia / 2], center=true);
                    }
    }
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
            make_engine_holder();
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
