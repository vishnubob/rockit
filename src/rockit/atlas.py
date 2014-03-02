#!/usr/bin/env python
import os
import sys
import argparse
import solid
import logging
import glob
from . import utils
from . import rockit

logger = logging.getLogger(__name__)


def get_templates(args):
    Templates = os.listdir

def configure_logger(args):
    root_logger = logging.getLogger("rockit")
    if args.debug:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s:%(name)s:%(levelname)s]: %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

def load_rocket_json(args):
    conf = utils.load_json(args.input_json)
    return rockit.Rockit(**conf)

def save_rocket(args, rocket):
    if not args.output_dir:
        args.output_dir = rocket.name
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    json_path = os.path.join(args.output_dir, "%s.json" % rocket.name)
    utils.save_json(rocket, json_path)
    build = rocket.get_build()
    for part_name in build:
        if not build[part_name]:
            continue
        scad_path = os.path.join(args.output_dir, "%s_%s.scad" % (rocket.name, part_name))
        stl_path = os.path.join(args.output_dir, "%s_%s.stl" % (rocket.name, part_name))
        part = build[part_name]
        utils.save_scad(part, scad_path)
        if args.export_stl:
            utils.save_stl(scad_path, stl_path)

def find_open_scad():
    cmd = None
    if sys.platform == "darwin":
        cmd = utils.find("OpenSCAD", "/Applications")
    if not cmd:
        cmd = utils.which("openscad")
    return cmd

def get_cli():
    defaults = {
        "export_stl": False,
        "openscad_exe": False,
        "debug": False,
        "template_dir": os.path.join(os.path.split(__file__)[0], "templates")
    }

    parser = argparse.ArgumentParser(description='Atlas model rocket generator.')
    parser.add_argument('-i', '--input_json', help='The name of the JOSN rocket configuration file')
    parser.add_argument('-o', '--output_dir', help='The output directory')
    parser.add_argument('-t', '--template', help='Use one of the standard, builtin templates')
    parser.add_argument('-S', '--openscad_exe', help='Path to OpenSCAD')
    parser.add_argument('-s', '--export_stl', action="store_true", help='Use OpenSCAD to generate .STL files')
    parser.add_argument('-d', '--debug', action="store_true", help='Enable debugging log')
    parser.add_argument('-T', '--template_dir', help='Alternate template directory')

    parser.set_defaults(**defaults)

    args = parser.parse_args()
    # templates
    if args.template:
        jsfn = args.template + '.json'
        jsfn = utils.find(args.template_dir, jsfn)
        print args.template_dir
        options = [os.path.splitext(fn)[0] for fn in glob.glob(os.path.join(args.template_dir, "*.json"))]
        if args.template not in options:
            msg = "could not find template: %s.  options are: %s" % (args.template, str.join(',', options))
            raise RuntimeError, msg
    # OpenSCAD
    if args.export_stl and args.openscad_exe == None:
        args.openscad_exe = find_open_scad()
        if not args.openscad_exe:
            raise RuntimeError, "Can't find OpenSCAD, is it installed?"
    return args

def main():
    args = get_cli()
    configure_logger(args)
    rocket = load_rocket_json(args)
    save_rocket(args, rocket)

if __name__ == "__main__":
    main()
