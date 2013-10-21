include $(wildcard *.deps)
OPENSCAD := "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
OUTPUT_DIR := stl
INPUT_DIR := scad
SOURCES := $(INPUT_DIR)/nosecone.scad $(INPUT_DIR)/tube.scad $(INPUT_DIR)/tail.scad $(INPUT_DIR)/collar.scad
TARGETS := $(OUTPUT_DIR)/nosecone.stl $(OUTPUT_DIR)/tube.stl $(OUTPUT_DIR)/tail.stl $(OUTPUT_DIR)/collar.stl

$(OUTPUT_DIR)/%.stl: $(INPUT_DIR)/%.scad
	mkdir -p stl && $(OPENSCAD) -m make -o $@ $<

clean:
	rm -rf $(OUTPUT_DIR)

all: $(SOURCES) $(TARGETS)
nosecone: $(OUTPUT_DIR)/nosecone.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/nosecone.scad 
tube: $(OUTPUT_DIR)/tube.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tube.scad
collar: $(OUTPUT_DIR)/collar.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/collar.scad
tail: $(OUTPUT_DIR)/tail.stl
$(OUTPUT_DIR)/tail.stl: $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tail.scad
