#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_z.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestZ(console.TestHarness):
    
    def test_z(self):
        suite.banner(self.test_z)
        self.run_test('z')
        self.assertEquals('Welcome to the Mach-8!', self.results[-10])