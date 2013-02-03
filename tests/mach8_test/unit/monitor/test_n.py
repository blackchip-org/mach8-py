#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_n.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestN(console.TestHarness):
    
    def test_n(self):
        suite.banner(self.test_n)
        self.run_test("""
a(lda_imm, 0x11)
a(lda_imm, 0x22) 
s('PROGRAM_START')
n
s
n""")
        self.assertEquals('$2000: a9 11     lda #$11', self.results[-8])
        self.assertEquals('$2002: a9 22     lda #$22', self.results[-3])
        
