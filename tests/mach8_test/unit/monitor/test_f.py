#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_f.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestF(console.TestHarness):
    
    def test(self):
        suite.banner(self.test) 
        self.run_test("""
a.label('test.one', 0x2011)
a.label('test.two', 0x2022) 
a.label('best.three', 0x2033) 
f('test')""")
        self.assertEquals('$2011 = test.one', self.results[-4])
        self.assertEquals('$2022 = test.two', self.results[-3])
        self.assertEquals('mach8>', self.results[-2])

        