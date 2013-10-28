#!/usr/bin/env python

import rockit
import sys
try:
    mass = float(sys.argv[1])
except:
    print "please provide your rocket mass in kg"

dia = rockit.utils.chute_size(mass)
print "Chute needs to be %.2fm in diameter (%.2fmm, %.2fin)" % (dia, dia * 1000, rockit.utils.mm2in(dia * 1000))
