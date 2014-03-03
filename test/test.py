#!/usr/bin/env python

import os

if not os.path.exists("examples"):
    os.mkdir("examples")
for template in ("mini", "mini_8fin", "mini_8fin_spin", "std", "d", "e"):
    cmd = "atlas.py -t %s -o examples/%s -p -s -x" % (template, template)
    os.system(cmd)
