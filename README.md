Rockit
======

Rockit is a set of tools to generate 3D models of working model rockets.  Using [OpenSCAD](http://www.openscad.org/ OpenSCAD), Rockit can generate parts of a rocket and export them to DXF or STL, suitable for manufacturing on a wide range of CNC platforms.  Using a rockit generated 3D model and a modern tabletop 3D printer, you can design, print and fly your rocket in about two hours.  It's currently very ALPHA, with lots of missing features.  But the system is new, so it's easy to add new features!

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
Rockit requires [OpenSCAD](http://www.openscad.org/downloads.html), [Python](http://www.python.org/download/), and [GNU Make](http://www.gnu.org/software/make/) although you can just get OpenSCAD to explore and change the shipped examples.

Getting Started
---------------
### Step 1: Download Rockit
[Download Rockit](https://github.com/vishnubob/rockit/archive/master.zip), unpack the archive if necessary

### Step 2: Fire up OpenSCAD
Open up OpenSCAD and load [scad/stub.scad](https://github.com/vishnubob/rockit/blob/master/scad/stub.scad)
<img src="http://i.imgur.com/C7UpA5E.png" alt="Step 1" style="width: 600px;"/>

### Step 3: Make a Rock Tail!

Add `make_rockit_tail();` to your stub, so that your file looks like this:

```jacascript
import <rockit.scad>;
make_rockit_tail();
```

And you should now have a four fin rocket tail that can accept standard sized engines!

<img src="http://i.imgur.com/t84cv5ul.png" alt="Step 2" style="width: 600px;"/>

### Step 4: Training Fins First!

Add `fincount = 3;` between the first and second lines of your stub, so that your file looks like this:

```jacascript
import <rockit.scad>;
fin_count = 3; 
make_rockit_tail();
```

Now your rocket looks much sleeker with only three fins.

<img src="http://i.imgur.com/mIMIzeU.png" alt="Step 2" style="width: 600px;"/>

### Step 5. MOAR FINS!

ok... let's bump your fincount with `fincount = 5;`, so now your file looks like this:

```jacascript
import <rockit.scad>;
fin_count = 5; 
make_rockit_tail();
```

badass...

<img src="http://i.imgur.com/XkH7idu.png" alt="Step 3" style="width: 600px;"/>

### Step 6. Rockets with a Twist

What happens when you adjust your fins 2.5mm deflection?  Configure your file like this:

```jacascript
import <rockit.scad>;
fin_count = 5; 
fin_deflection = 2.5;
make_rockit_tail();
```

Now you have a rocket that will produce a stunning, corkscrew-shaped contrail.

<img src="http://i.imgur.com/K0cxxr0.png" alt="Step 4" style="width: 600px;"/>

### Step 7. Save your Design!

You can use OpenSCAD to save your design in a number of formats, including DXF and STL.

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

