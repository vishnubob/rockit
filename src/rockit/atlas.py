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
DEFAULT_TEMPLATE_DIR = os.path.join(os.path.split(__file__)[0], "templates")

def get_templates(template_dir):
    Templates = os.listdir(template_dir)

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
        part = build[part_name]
        utils.save_scad(part, scad_path)
        if args.export_stl:
            stl_path = os.path.join(args.output_dir, "%s_%s.stl" % (rocket.name, part_name))
            utils.save_stl(args.openscad_exe, scad_path, stl_path)
        if args.export_png:
            png_path = os.path.join(args.output_dir, "%s_%s.png" % (rocket.name, part_name))
            utils.save_png(args.openscad_exe, scad_path, png_path)
        if args.export_dxf:
            png_path = os.path.join(args.output_dir, "%s_%s.dxf" % (rocket.name, part_name))
            utils.save_dxf(args.openscad_exe, scad_path, dxf_path)

def check_scad_exe(args):
    return os.path.isfile(args.openscad_exe) and os.access(args.openscad_exe, os.X_OK)

def find_open_scad(args):
    if check_scad_exe(args):
        return True
    if sys.platform == "darwin":
        hint = "/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD"
        args.openscad_exe = hint
        if check_scad_exe(args):
            return True
    args.openscad_exe = utils.which("openscad")
    if check_scad_exe(args):
        return True
    return False

def get_templates(template_dir=None):
    template_dir = (template_dir or DEFAULT_TEMPLATE_DIR)
    return {os.path.splitext(os.path.split(fn)[-1])[0]: fn for fn in glob.glob(os.path.join(template_dir, "*.json"))}

def get_cli():
    defaults = {
        "export_stl": False,
        "openscad_exe": '',
        "debug": False,
        "template_dir": DEFAULT_TEMPLATE_DIR,
        "export_png": False,
        "export_dxf": False,
    }

    parser = argparse.ArgumentParser(description='model rocket generator')
    parser.add_argument('-i', '--input_json', help='rocket configuration file in JSON format')
    parser.add_argument('-t', '--template', help='load builtin template (%s)' % str.join(', ', get_templates().keys()))
    parser.add_argument('-T', '--template_dir', help='template directory (default=%s)' % DEFAULT_TEMPLATE_DIR)
    parser.add_argument('-o', '--output_dir', help='output directory')
    parser.add_argument('-S', '--openscad_exe', help='path to OpenSCAD')
    parser.add_argument('-s', '--export_stl', action="store_true", help='export .STL via OpenSCAD')
    parser.add_argument('-x', '--export_dxf', action="store_true", help='export .DXF of object')
    parser.add_argument('-p', '--export_png', action="store_true", help='export image of object')
    parser.add_argument('-d', '--debug', action="store_true", help='enable debugging log')

    parser.set_defaults(**defaults)

    args = parser.parse_args()
    # Templates
    if args.template:
        jsfn = args.template + '.json'
        jsfn = utils.find(jsfn, args.template_dir)
        templates = get_templates(args.template_dir)
        if args.template not in templates:
            msg = "could not find template: %s, options are: %s" % (args.template, str.join(',', templates.keys()))
            raise RuntimeError, msg
        args.input_json = templates[args.template]
    # OpenSCAD
    if (args.export_png or args.export_stl):
        if not find_open_scad(args):
            raise RuntimeError, "Can't find OpenSCAD, is it installed?"
    return args

def main():
    args = get_cli()
    configure_logger(args)
    rocket = load_rocket_json(args)
    save_rocket(args, rocket)

if __name__ == "__main__":
    main()
