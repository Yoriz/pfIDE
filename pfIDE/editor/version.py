# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 20:27:12 2011
@author: Jakob
@reviewer: David
"""
import platform
import sys

def is_windows():
    """Tries to identify if we are on a windows machine."""
    if 'Windows' in platform.uname():
        return True
    else:
        return False

def introduction():
    """Returns interpreter infomation."""
    return "Python %s" % sys.version
    
def get_python_exe():
    """Return the location of the python executable."""
    return sys.executable
