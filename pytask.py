import sys

def task(f):
    mod = sys.modules[f.__module__]
    pytasks = mod.__dict__.setdefault('pytasks', [])
    pytasks.append(f)
    return f