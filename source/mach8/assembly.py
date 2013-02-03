#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: assembly.py 107 2011-12-17 02:36:33Z mcgann $
#------------------------------------------------------------------------------
"""
Globally import all symbols in this module when writing assembly code.

Importing this module is the same as the following::

    >>> from mach8.instructions import * 
    >>> from mach8.expressions import * 
    >>> from mach8.macros import * 
   
This module also exports the ``_`` object which can be used to bypass
Python's monopoly on whitespace. Example:: 

    >>> _;         a(lda_imm, 0x42) 
"""

_ = object() 

from mach8.instructions import *
from mach8 import instructions

from mach8.expressions import * 
from mach8 import expressions

from mach8.macros import * 
from mach8 import macros 

__all__ = ['_'] + instructions.__all__ + expressions.__all__ + macros.__all__
 
                