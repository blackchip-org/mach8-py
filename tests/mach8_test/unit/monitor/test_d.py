#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_d.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestC(console.TestHarness):
    
    def test_range(self):
        suite.banner(self.test_range)
        self.run_test('d(0x5000, 0x500f)')
        self.assertEquals('$5000: 00        brk', self.results[-18])
        self.assertEquals('$500f: 00        brk', self.results[-3])
        self.assertEquals('mach8>', self.results[-2])
        
    def test_no_end(self):
        suite.banner(self.test_no_end)
        self.run_test("""\
conf.lines = 5
d(0x5000)""")
        self.assertEquals('$5005: 00        brk', self.results[-3])
        self.assertEquals('mach8>', self.results[-2])
        
    def test_no_start(self):
        suite.banner(self.test_no_start) 
        self.run_test("""\
d(0x5000, 0x5003)
d(end=0x5006)
""")
        self.assertTrue(self.results[-12].startswith('mach8>'))
        self.assertTrue(self.results[-7].startswith('mach8>'))
        self.assertEquals('$5006: 00        brk', self.results[-4])
        self.assertTrue(self.results[-3].startswith('mach8>'))
        
    def test_continue(self):
        suite.banner(self.test_continue) 
        self.run_test("""\
conf.lines = 4
d(0x5000)
d""")
        self.assertTrue(self.results[-8].startswith('mach8>'))
        self.assertEquals('$5009: 00        brk', self.results[-3])
        self.assertTrue(self.results[-2].startswith('mach8>'))

    def test_labels(self):
        suite.banner(self.test_labels) 
        self.run_test("""\
a('test.begin')
a(brk)
a('test.end')
a(nop)
d('test.begin', 'test.end')""")
        self.assertEquals('$2000: 00        brk', self.results[-5])
        self.assertEquals('$2001: ea        nop', self.results[-3])

        


        
        