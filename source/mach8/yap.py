#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: yap.py 73 2011-10-27 12:44:53Z mcgann $
#------------------------------------------------------------------------------
"""
Yet Another Programming thing. 
"""
from mach8 import yapc 

__all__ = ['_', 'NEW', 'DONE', 'PRINT', 'PRINTLN']

_ = object() 
_yc = None 

def NEW():
    global _yc
    _yc = yapc.compiler_factory()
    _yc.new() 
    
DONE = lambda: _yc.done() 
PRINT = lambda *args: _yc.print_(*args) 
PRINTLN = lambda *args: _yc.println(*args) 

