#!/usr/bin/env python

import os
import sys
import importlib

def main(module, fun, *args):
    d = os.getcwd()
    try:
        mydir = os.path.dirname(os.path.realpath(__file__))
        os.chdir(mydir)
        mod = importlib.import_module(module)
        getattr(mod, fun)(*args)
    finally:
        os.chdir(d)
    

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *sys.argv[3:])