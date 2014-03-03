#!/usr/bin/env python

from distutils.core import setup, Extension

rockit = {
    "name": "rockit",
    "description": "model rocket generator",
    "author":"Giles Hall",
    "packages": ["rockit", "rockit.solid"],
    "package_dir": {"rockit": "src/rockit"},
    "package_data": {'rockit': ['templates/*.json']},
    "scripts":["scripts/calculate_chute", "scripts/atlas"],
    "version": "0.5",
}

if __name__ == "__main__":
    setup(**rockit)
