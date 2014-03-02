Rockit
======

Rockit provides a framework to rapidly generate 3D models of workable model rockets.  It leverages [OpenSCAD](http://www.openscad.org/ OpenSCAD) to render rocket part specificiations to three dimensional models. This allows you the ability to configure and generate individual model rocket parts suitable for manufacturing on a wide range of 3D printing platforms.  With carefully configured paramaters, you can design, print and fly your rocket in under two hours.  Rockit parses JSON rocket configuration files and writes out to a variety of formats including .json, .scad, .stl, .dxg, .png.   It ships with a variety of default templates based on different engine sizes, but these will require local tuning for proper operation.  

Requirements
------------
Rockit requires [OpenSCAD](http://www.openscad.org/downloads.html), [Python](http://www.python.org/download/).  [SolidPython](https://github.com/SolidCode/SolidPython) is baked into the distribution, because rockit requires the development branch.  This might change at some point.

Getting Started
---------------
### Step 1: download and install rockit
Use pip to install the rockit package by executing the following command, ideally in a fresh [virtual environment](https://pypi.python.org/pypi/virtualenv):
'''javascript
$ pip install https://github.com/vishnubob/rockit/archive/master.zip
'''
You can also [download](https://github.com/vishnubob/rockit/archive/master.zip) the package directly and install it by hand.

### Step 2: Build a "mini" template, with images

```jacascript
$ atlas.py -t mini -p
```

This command will create a directory called "mini_engine" and it will save images for all the parts that make up a mini rocket.  Look for "mini_engine/mini_engine.json" file, this is the full JSON configuration for this template.  You can copy this file, and tweak your rocket design based on this template.  Some parameters are based on other parameters, which is why these parameters have null values in the JSON config file.  With the config file, you can provide values, and these will override the automatic assignment.

```jacascript
$ cp mini_engine/mini_engine.json my_mini_engine.json
```

Open your favorite editor and edit the "my_mini_engine.json" file.  Scroll down to the bottom of the file, and look for the section that defines the tail section.  It should look something like this:


'''javascript
   "tail": {
       "fin_count": 4
   }
'''

Let's increase the number of fins in our tail section from four to eight:

'''javascript
   "tail": {
       "fin_count": 8
   }
'''

Save this config, and run atlas on our new config file:

```jacascript
$ atlas.py -i my_mini_engine.json -p
```

What does the Fin image look like now?










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

