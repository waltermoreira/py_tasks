#!/usr/bin/env python

import os
import sys
import importlib

def main(module, fun):
    d = os.getcwd()
    try:
        mydir = os.path.dirname(os.path.realpath(__file__))
        print mydir
        os.chdir(mydir)
        mod = importlib.import_module(module)
        getattr(mod, fun)()
    finally:
        os.chdir(d)
    

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])