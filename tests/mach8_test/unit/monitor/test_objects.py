#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_objects.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestObjects(console.TestHarness):
    """
    Make sure the objects are there and are the proper type
    """
    
    def test_comp(self):
        suite.banner(self.test_comp) 
        self.run_test('repr(comp)')
        self.assertTrue(self.results[-3].startswith("'<mach8.mach.Computer "))

    def test_conf(self):
        suite.banner(self.test_comp) 
        self.run_test('repr(conf)')
        self.assertTrue(self.results[-3]
                        .startswith("'<mach8.monitor.Configuration "))  
        
    def test_cpu(self):
        suite.banner(self.test_comp) 
        self.run_test('repr(cpu)')
        self.assertTrue(self.results[-3].startswith("'<mach8.x6502.CPU "))

    def test_meta(self):
        suite.banner(self.test_comp) 
        self.run_test('repr(meta)')
        self.assertTrue(self.results[-3]
                        .startswith("'<mach8.tools.MetaSource "))

        
      
