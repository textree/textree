#!/usr/bin/env python
# -*- coding: utf-8 -*-
if __name__ == '__main__':
    import platform
    vers = platform.python_version_tuple()
    import os, sys
    import subprocess
    print('python version', vers)
    def run_unit_test(py_ver):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        subprocess.call("python" + py_ver + " " + os.path.join(this_dir, "py" + py_ver, "TestTexTree.py"), shell=True)
    if   2 == int(vers[0]): run_unit_test(vers[0])
    elif 3 == int(vers[0]): run_unit_test(vers[0])
    else: raise Exception('There is no source code corresponding to the specified Python version.')

