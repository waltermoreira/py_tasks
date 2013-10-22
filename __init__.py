import sys
import os
import os.path
import re
import importlib
import types
import glob

import fabric.api
import fabric.tasks


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SUDO_PREFIX = re.compile(r'/(root|sudo)_?', re.I)

def collect_pytasks(filename):
    d = os.getcwd()
    try:
        os.chdir(os.path.dirname(filename))
        name, _ = os.path.splitext(os.path.basename(filename))
        if '' not in sys.path:
            sys.path.insert(0, '')
        mod = importlib.import_module(name)
        for fun_name in mod.__dict__:
            if not fun_name.startswith('_'):
                fun = getattr(mod, fun_name)
                if isinstance(fun, types.FunctionType):
                    tasks[fun_name] = PythonTask(filename, name, fun_name)
    finally:
        os.chdir(d)
    

class ScriptTask(fabric.tasks.Task):

    def __init__(self, script_path, name=None, sudo=False):
        super(ScriptTask, self).__init__()
        self.script_path = script_path
        self.script_name = os.path.basename(script_path)
        self.name = name or os.path.splitext(self.script_name)[0]
        self.sudo = sudo
        if sudo:
            self.remote_path = '/root/{}'.format(self.script_name)
        else:
            self.remote_path = '/tmp/{}'.format(self.script_name)

    def run(self):
        self.put()
        if self.sudo:
            fabric.api.sudo(self.remote_path)
        else:
            fabric.api.run(self.remote_path)

    def put(self):
        fabric.api.put(
                self.script_path,
                self.remote_path,
                mirror_local_mode=True,
                use_sudo=self.sudo)
            
class PythonTask(ScriptTask):

    def __init__(self, filename, module, fun, sudo=False):
        super(PythonTask, self).__init__(filename, sudo=sudo)
        self.module = module
        self.fun = fun
        self.name = self.fun
        self.base_dir = os.path.dirname(filename)

    def run(self, *args):
        fabric.api.put(
            os.path.join(SCRIPT_DIR, '__executer.py'),
            '/tmp/__executer.py',
            mirror_local_mode=True)
        self.put()
        fabric.api.run('/tmp/__executer.py {} {} {}'.
                       format(self.module, self.fun, ' '.join(args)))
        

__all__ = []
tasks = {}

for filename in os.listdir(SCRIPT_DIR):
    if filename.startswith('__'):
        continue
    filename = os.path.join(SCRIPT_DIR, filename)
    if os.path.isfile(filename):
        task_is_sudo = bool(SUDO_PREFIX.search(filename))
        if os.access(filename, os.X_OK):        
            task = ScriptTask(filename, sudo=task_is_sudo)
            tasks[task.name] = task

pys = os.path.join(SCRIPT_DIR, '../*.py')
for filename in glob.glob(pys):
    if filename.startswith('_') or filename.endswith('fabfile.py'):
        continue
    # Collect all py_tasks of Python files outside the package
    collect_pytasks(os.path.abspath(filename))


for task_name, task in tasks.iteritems():
    globals()[task_name] = task
    __all__.append(task_name)