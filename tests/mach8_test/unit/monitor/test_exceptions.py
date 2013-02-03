#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_exceptions.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestExceptions(console.TestHarness):
    
    def test_value_error(self):
        suite.banner(self.test_value_error)
        self.run_test('blah')
        self.assertEquals('? Syntax error', self.results[-3])
        
        
    
