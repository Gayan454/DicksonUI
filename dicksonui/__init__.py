#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  __init__.py
#  
from sys import version_info
from .Control import *
from .Application import Application
if version_info[0] < 3:
    from .Form_min import *
    import Controls_min as Controls
else:
    from .Form import *
    from .Controls import *
del version_info

