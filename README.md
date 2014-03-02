Rockit
======

Rockit is a set of tools to generate 3D models of working model rockets.  Using [OpenSCAD](http://www.openscad.org/ OpenSCAD), Rockit can generate parts of a rocket and export them to DXF or STL, suitable for manufacturing on a wide range of CNC platforms.  Using a rockit generated 3D model and a 3D printer, you can design, print and fly your rocket in about two hours.  

Configurable Rockit Parts
-------------------------

### Connector Ring
A connector ring can be configured for any part.  It provides a compression fitting collar, making it easy to interchange and assemble rocket parts; kind of like legos.  You can print a variety of different rocket parts, and in the field, you can quickly configure, assemble and launch your rocket.
### Launch Lug 
Launch lugs slide over the launch rod of a launch pad, and guide the rocket during lift off.  You can configure your launch lugs how you wish.
### Nosecone
This is an active work in progress right now.
### Body Tube
*Length configuration* The body tube is just a tube with a connector ring, so you can connect as many together as you need to produce whatever length rocket you want.
*Payload potential* Since the body tube is completely empty, you can use it stash all sorts of payloads.  You can even make custom housing for whatever payload you have in mind.
### Fins
You can configure everything about your fins: two wide fins, with a 1.2 degree tilt; six short, thin fins wih no tilt.  Since your fins (and your rocket) will be manufactured with computer precision, you can use this to carefully experiment with different designs. 
### Rocket Engine Holder
All the common rocket engines and diameters are baked in, making it easy to choose a rocket engine for your design.  The rocket engine holder is designed as a compression fit.  All you have to do is print it, stuff a rocket engine in, and launch it!
### Multiple Stages
You can link tail parts together to create your own multi-stage rocket.

Output Formats
--------------
1. .STL
2. .DXF
3. .PNG

Requirements
------------
Rockit requires [OpenSCAD](http://www.openscad.org/downloads.html), [Python](http://www.python.org/download/).  Right now, [SolidPython](https://github.com/SolidCode/SolidPython) is baked into the distribution, because it currently requires the development branch.

Getting Started
---------------
### Step 1: Download Rockit
[Download Rockit](https://github.com/vishnubob/rockit/archive/master.zip), unpack the archive if necessary

### Step 2: Fire up OpenSCAD
Unzip master.zip and open a terminal.  Change your directory to the archive contents, and install the python package:
```jacascript
python setup.py install
```

### Step 3: Build a "mini" template, with images

```jacascript
atlas.py -t mini -p
```

This command will build out all the parts that make up a mini rocket, and save .PNG images for all parts.  It will also save a full config file for "mini.json" file, which you can copy and configure to your specifications.

now edit and use to 
Open up OpenSCAD and load [scad/stub.scad](https://github.com/vishnubob/rockit/blob/master/scad/stub.scad)
<img src="http://i.imgur.com/C7UpA5E.png" alt="Step 1" style="width: 600px;"/>

Resources for Learning More
---------------------------
- To get a feel of how to configure your own rockit, check out [scad/rockit.scad](https://github.com/vishnubob/rockit/blob/master/scad/rockit.scad)
- [Documentation](http://en.wikibooks.org/wiki/OpenSCAD_User_Manual/The_OpenSCAD_Language) is available on the OpenSCAD programming language.
- Check out the [Makefile](https://github.com/vishnubob/rockit/blob/master/Makefile).  You can build STL or PNG files by issuing a `make` from the command line from within the rockit directory.

Credits
-------
- Rockit is written and maintained by Giles Hall (C) 2012-2013
- Original fin design based on [Thingiverse](http://www.thingiverse.com/) [Object #26508 (Simple model rocket tail fins)](http://www.thingiverse.com/thing:26508), an *.scad* script written by [Lutz Paelke](http://www.thingiverse.com/lpaelke/designs) and published on Jul 9, 2012.
- [Rockit](https://github.com/vishnubob/rockit), the model rocket construction kit, should not to be confused by [Rockit](http://en.wikipedia.org/wiki/Rockit), an excellent electro track from 1983 by [Herbie Hancock](http://en.wikipedia.org/wiki/Herbie_Hancock)

