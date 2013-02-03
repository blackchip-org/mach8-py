#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_print.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.yap import * 
from mach8_test import suite
import mach8_test.harness.yap

class TestPrint(mach8_test.harness.yap.TestHarness):
            
    def test_println(self):
        suite.banner(self.test_println) 
        
        _;  NEW()
        _;      PRINTLN('Hello world!')
        _;  DONE() 
        
        self.run_test() 
        self.assertEquals('Hello world!\n', self.output.getvalue()) 

    def test_print(self):
        suite.banner(self.test_print) 
        
        _;  NEW()
        _;      PRINT('Hello world!')
        _;  DONE() 
        
        self.run_test() 
        self.assertEquals('Hello world!', self.output.getvalue()) 
        
    def test_print_multi(self):
        suite.banner(self.test_print_multi) 
        
        _;  NEW()
        _;      PRINT('This is ', 'a test ', 42) 
        _;  DONE() 
        
        self.run_test() 
        self.assertEquals('This is a test 42', self.output.getvalue()) 
        