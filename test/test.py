#!/usr/bin/env python

import os
import subprocess

def execute(cmd):
    try:
        retcode = subprocess.call(cmd.split(' '))
        if retcode < 0:
            raise RuntimeError, "Child was terminated by signal: %d" % (-retcode,)
        else:
            raise RuntimeError, "Child returned retcode: %d" % (retcode,)
    except OSError as exc:
        raise RuntimeError, "Execution failed: %s" % exc
    return True

if not os.path.exists("examples"):
    os.mkdir("examples")
for template in ("mini", "mini_8fin", "mini_8fin_spin", "std", "d", "e"):
    cmd = "atlas -t %s -o examples/%s -p -s -x" % (template, template)
    execute(cmd)
