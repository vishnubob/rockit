#!/usr/bin/env python
import sys
import rockit

try:
    partname = sys.argv[1]
except:
    print "Please provide a part name to build"
    sys.exit(-1)

funcname = "make_%s" % partname
try:
    func = getattr(rockit.assemble, funcname)
except:
    print "Sorry, I could not find a function called: %s" % funcname
    sys.exit(-1)

func()
