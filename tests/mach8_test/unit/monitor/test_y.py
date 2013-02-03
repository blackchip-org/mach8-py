#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_y.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestY(console.TestHarness):
    
    def test_y(self):
        suite.banner(self.test_y)
        self.run_test("""
a.label('foo', 1234)
y('foo')""")
        self.assertEquals('1234', self.results[-3])
        
    def test_y_no_label(self):
        suite.banner(self.test_y_no_label)
        self.run_test("y('foo')")
        self.assertEquals('? Unknown symbol', self.results[-3])
        