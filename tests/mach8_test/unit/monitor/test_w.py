#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_w.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestW(console.TestHarness):
    
    def test_add_watch(self):
        suite.banner(self.test_add_watch)
        self.run_test("""
w(0x4000)
mem[0x4000] = 0x42""")
        self.assertEquals('mem $4000 <-= $42', self.results[-3])

    def test_add_watch_label(self):
        suite.banner(self.test_add_watch_label)
        self.run_test("""
a.label('test.label', 0x4000)
w('test.label')
mem[0x4000] = 0x42""")
        self.assertEquals('mem $4000 <-= $42: test.label', self.results[-3])
                
    def test_remove_watch(self):
        suite.banner(self.test_remove_watch)
        self.run_test("""
w(0x4000)
w(0x4000)
mem[0x4000] = 0x42""")
        self.assertEquals('mach8>', self.results[-2]) 
        
    def test_list_watches(self):
        suite.banner(self.test_list_watches) 
        self.run_test("""
w(0x4000) 
w(0x3000)
w(0x5000)
a.label('foo', 0x4000)
a.label('bar', 0x4000)
a.label('baz', 0x5000) 
w""")       
        self.assertEquals('$3000', self.results[-5])
        self.assertEquals('$4000: bar, foo', self.results[-4])
        self.assertEquals('$5000: baz', self.results[-3])
        
    def test_clear_watches(self):
        suite.banner(self.test_clear_watches)
        self.run_test("""
w(0x4000) 
w(0x3000)
w(0x5000)
w(0)
w""")
        self.assertEquals('mach8> w', self.results[-3])
        self.assertEquals('mach8>', self.results[-2])
         
        
        