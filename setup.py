#!/usr/bin/env python

from distutils.core import setup, Extension

rockit = {
    "name": "rockit",
    "description": "Model rocket generator",
    "author":"Giles Hall",
    "packages": ["rockit"],
    "package_dir": {
                    "rockit": "src", 
                    },
    "py_modules":[
                    "rockit.__init__", 
                    "rockit.rockit", 
                    "rockit.assemble", 
                    "rockit.nosecone", 
                    "rockit.utils", 
                    "rockit.parts", 
                ],
    "scripts":[
                "scripts/chute.py",
                "scripts/atlas.py",
               ],
    "version": "0.1",
}

if __name__ == "__main__":
    setup(**rockit)
