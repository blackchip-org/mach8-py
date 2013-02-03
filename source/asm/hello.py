#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: hello.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import * 

def assemble(a):
    _;      a(jsr,      'PRIMM')
    _;      a.data      ('\nHello world!\n\n', 0)
    _;      a(rts) 