#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: hello.py 77 2011-11-04 20:23:44Z mcgann $
#------------------------------------------------------------------------------
from mach8.yap import * 

def compile():
    
    _;  NEW() 
    _;      PRINTLN('Hello world!')
    _;  DONE() 
    
