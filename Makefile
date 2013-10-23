#################
# Variables
#
OPENSCAD := "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
OUTPUT_DIR := stl
IMAGES_DIR := images
INPUT_DIR := scad
TARGETS_STL := collar_stl nosecone_stl tube_stl tail_stl
TARGETS_PNG := collar_png nosecone_png tube_png tail_png
TARGETS := $(TARGETS_STL) $(TARGETS_PNG)
.DEFAULT_GOAL := all

#################
# Rockit Parts
#
# collar
collar_stl: $(OUTPUT_DIR)/collar.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/collar.scad
$(OUTPUT_DIR)/collar.stl: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/collar.scad
collar_png: $(IMAGES_DIR)/collar.png $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/collar.scad
$(IMAGES_DIR)/collar.png: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/collar.scad
collar: collar_stl collar_png

# nosecone
nosecone_stl: $(OUTPUT_DIR)/nosecone.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/nosecone.scad 
$(OUTPUT_DIR)/nosecone.stl: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/nosecone.scad
nosecone_png: $(IMAGES_DIR)/nosecone.png $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/nosecone.scad
$(IMAGES_DIR)/nosecone.png: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/nosecone.scad
nosecone: nosecone_stl nosecone_png

# tube
tube_stl: $(OUTPUT_DIR)/tube.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tube.scad
$(OUTPUT_DIR)/tube.stl: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tube.scad
tube_png: $(IMAGES_DIR)/tube.png $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tube.scad
$(IMAGES_DIR)/tube.png: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tube.scad
tube: tube_stl tube_png

# tail
tail_stl: $(OUTPUT_DIR)/tail.stl $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tube.scad
$(OUTPUT_DIR)/tail.stl: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tail.scad
tail_png: $(IMAGES_DIR)/tail.png $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tail.scad
$(IMAGES_DIR)/tail.png: $(OUTPUT_DIRS) $(INPUT_DIR)/rockit.scad $(INPUT_DIR)/tail.scad
tail: tail_stl tail_png

#################
# Rules
#
$(OUTPUT_DIRS): $(OUTPUT_DIR) $(IMAGES_DIR)

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)
$(IMAGES_DIR):
	mkdir -p $(IMAGES_DIR)

$(OUTPUT_DIR)/%.stl: $(INPUT_DIR)/%.scad
	$(OPENSCAD) -m make -o $@ $<

$(IMAGES_DIR)/%.png: $(INPUT_DIR)/%.scad
	$(OPENSCAD) -m make -o $@ $<

all: $(TARGETS)
stl: $(TARGETS_STL)
png: $(TARGETS_PNG)

clean:
	rm -rf $(OUTPUT_DIR)
