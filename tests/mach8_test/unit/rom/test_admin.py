#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_admin.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestAdmin(execution.TestHarness):
    
    def test_welcome(self):
        suite.banner(self.test_welcome)
        a = self.a
                
        _;      a(jsr,  'WELCOME')
        
        self.run_test() 
        self.assertEquals('\nWelcome to the Mach-8!\n\n', 
                          self.output.getvalue())
        