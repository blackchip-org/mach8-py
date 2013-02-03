#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_l.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestB(console.TestHarness):
    
    def test_asm(self):
        suite.banner(self.test_asm) 
        self.run_test("""\
l('asm.hello')
r""")
        self.assertEquals('Hello world!', self.results[-4])
        
    def test_not_found(self):
        suite.banner(self.test_not_found) 
        self.run_test("l('foobar')")
        self.assertEquals('? File not found', self.results[-3])
        
    def test_invalid(self):
        suite.banner(self.test_invalid) 
        self.run_test("l('mach8.vm')")
        self.assertEquals('? Invalid program', self.results[-3])

        