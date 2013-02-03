#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_g.py 98 2011-12-12 23:10:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestG(console.TestHarness):
    
    def test(self):
        suite.banner(self.test) 
        self.run_test("""
a(lda_imm, 0x11) 
a(brk)
a(nop)
a(lda_imm, 0x22) 
a(brk)
a(nop)
a(lda_imm, 0x33) 
r
g""") 
        self.assertEquals('2007 30 22 00 00 fd  . . * * . . . .', 
                          self.results[-3])
        