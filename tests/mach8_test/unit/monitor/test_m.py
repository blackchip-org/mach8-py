#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_m.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestM(console.TestHarness):
    
    def test_range(self):
        suite.banner(self.test_range)
        self.run_test('m(0x5000, 0x50ff)')
        self.assertTrue(self.results[-18].startswith('$5000'))
        self.assertTrue(self.results[-3].startswith('$50f0'))
        
    def test_range_labels(self):
        suite.banner(self.test_range_labels) 
        self.run_test("""
a.label('test.start', 0x5000)
a.label('test.end', 0x50ff)
m('test.start', 'test.end')""")
        self.assertTrue(self.results[-18].startswith('$5000'))
        self.assertTrue(self.results[-3].startswith('$50f0'))
           
    def test_begin_only(self):
        suite.banner(self.test_begin_only)
        self.run_test('m(0x5000)')
        self.assertTrue(self.results[-18].startswith('$5000'))
        self.assertTrue(self.results[-3].startswith('$50f0'))  
        
    def test_end_only(self):
        suite.banner(self.test_end_only) 
        self.run_test("""\
m(0x5000, 0x50ff)
m(end=0x51ff)""")
        self.assertTrue(self.results[-18].startswith('$5100'))
        self.assertTrue(self.results[-3].startswith('$51f0')) 
        
    def test_continue(self):
        suite.banner(self.test_continue) 
        self.run_test("""\
m(0x5000, 0x50ff)
m""")
        self.assertTrue(self.results[-18].startswith('$5100'))
        self.assertTrue(self.results[-3].startswith('$51f0')) 
        
    def test_wrap_around(self):
        suite.banner(self.test_wrap_around)
        self.run_test('m(0xff00, 0x100ff)')
        self.assertTrue(self.results[-3].startswith('$00f0'))

         
                
        