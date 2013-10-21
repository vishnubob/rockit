include $(wildcard *.deps)
OPENSCAD := "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
TARGETS := tube.stl tail.stl

all: $(TARGETS)

%.stl: %.scad
	$(OPENSCAD) -m make -o $@ $<
