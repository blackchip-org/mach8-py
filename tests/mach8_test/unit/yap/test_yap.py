#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_yap.py 130 2012-01-28 02:16:54Z mcgann $
#------------------------------------------------------------------------------
from mach8.yap import * 
from mach8_test import suite
import mach8_test.harness.yap

class TestPrint(mach8_test.harness.yap.TestHarness):
    
    def test_incomplete(self):
        suite.banner(self.test_incomplete) 
        
        _;  NEW()
        _;      PRINTLN('Hello world')
        
        self.run_test() 
        self.assertEquals('? Program incomplete error\n', 
                          self.output.getvalue()) 