Rockit
======

Rockit is a set of tools to generate 3D models of working model rockets.  Using [http://www.openscad.org/ OpenSCAD], Rockit can generate subsections of a rocket and export them to DXF or STL, suitable for manufacturing on a wide range of CNC platforms, including table top 3D printing.  Using a rockit generated 3D model and a modern tabletop 3D printer, you can design, print and fly your rocket in about two hours.  It's currently very ALPHA, with lots of missing features.  But the system is simple, and should be easy to add.

Configurable Rockit Parts
-------------------------

### Connector Ring
A connector ring can be configured for any part.  It provides a compression fitting collar, making all rockit parts easy to interchange and assemble, kind of like legos.  You can print a variety of different rockit parts, and in the field, you can quickly configure, assemble and launch your rocket.
### Launch Lug 
Launch lugs slide over the launch rod of a launch pad, and guide the rocket during lift off.  You can configure your launch lugs how you wish.
### Nosecone
This is an active work in progress right now.
### Fins
You can configure them with anything you want, two fins, ten fins, fins with a tilt, wide fins, short fins.  Since your fins (and your rocket) will be manufactured with computer precision, you can use this to carefully experiment with different designs. 
### Rocket engine holder
All the common rocket engines and diameters are baked in, making it easy to choose a rocket engine for your design.  The rocket engine holder is designed as a compression fit.  All you have to do is print it, stuff a rocket engine in, and launch it!
### Multi-stages
You can link tail parts together to create your own multi-stage rocket.
### Body Tube
*Length configuration* The body tube is just a tube with a connector ring, so you can connect as many together as you need to produce whatever length rocket you want.

*Payload potential* Since the body tube is completely empty, you can use it stash all sorts of payloads.  You can even make custom housing for whatever payload you have in mind.

Output Formats
--------------
1. .STL
2. .DXF
3. .PNG

Requirements
------------
Rockit requires [OpenSCAD](http://www.openscad.org/downloads.html), [Python](http://www.python.org/download/), and [GNU Make](http://www.gnu.org/software/make/) although you can just get OpenSCAD to explore and change the shipped examples.

Getting Started
---------------
1. [Download Rockit](https://github.com/vishnubob/rockit/archive/master.zip), unpack the archive if necessary
2. Open up OpenSCAD and load scad/stub.scad
<img src="http://i.imgur.com/C7UpA5E.png" alt="Step 1" style="width: 600px;"/>
3. Add the following code:
```
make_rockit_tail();
```
<img src="http://i.imgur.com/t84cv5ul.png" alt="Step 2" style="width: 600px;"/>
4. Four fins are boring, how about 3?
```
fin_count = 3; 
```
<img src="http://i.imgur.com/mIMIzeU.png") alt="Step 2" style="width: 600px;"/>
5. How about 5?
```
fin_count = 5; 
```
<img src="http://i.imgur.com/XkH7idu.png" alt="Step 3" style="width: 600px;"/>
6. What about 5 fins with a 2.5mm deflection?
```
fin_count = 5; 
fin_deflection = 2.5;
```
<img src="http://i.imgur.com/K0cxxr0.png" alt="Step 4" style="width: 600px;"/>

Resources for Learning More
---------------------------
- To get more of a feel of what is possible, examine scad/rockit.scad.
- [Documentation]([http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language]  is available on the OpenSCAD programming language.
- Check out the Makefile.  You can build STL or PNG files by issuing a '''make''' from the command line from within the rockit directory.

Credits
-------
* Rockit is written and maintained by Giles Hall (C) 2012-2013
* Original fin design based on [Thingiverse](http://www.thingiverse.com/) ["Object #26508 (Simple model rocket tail fins)"](http://www.thingiverse.com/thing:26508), an .scad script written by [Lutz Paelke](http://www.thingiverse.com/lpaelke/designs) and published on Jul 9, 2012.
* Rockit, the model rocket construction kit, should not to be confused by [Rockit](http://en.wikipedia.org/wiki/Rockit), an excellent electro track from 1983 by [Herbie Hancock](http://en.wikipedia.org/wiki/Herbie_Hancock)
