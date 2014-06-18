========
py_tasks
========

Convert Python functions to Fabric tasks.

Usage
=====

Write your Python function, such as:

.. code-block: python

   # file: example.py
   
   import platform
   
   def foo():
       print(platform.uname())

The directory structure looks like::

   work/example.py
   work/py_tasks/...
   work/fabfile.py
   
Run as::

   fab -H localhost,remote_host py_tasks.foo
   
Compose it with other functions in your ``fabfile`` by using the name ``py_tasks.foo``.
