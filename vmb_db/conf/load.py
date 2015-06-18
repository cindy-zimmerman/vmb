import os
import sys
from importlib import import_module

COINDIR = os.environ.get('VMB_CONFIG_DIR', '/etc/vmb/config')
if COINDIR not in sys.path:
    sys.path.append(COINDIR)

__all__ = ['getModule']

getModule = import_module
