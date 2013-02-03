#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_k.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestK(console.TestHarness):
    
    def test_k(self):
        suite.banner(self.test_k)
        self.run_test("""
a(lda_imm, 0x11)
a(jsr, 'test.1') 
a(brk)
a(nop)
a('test.1')
a(lda_imm, 0x22)
a(rts) 
s('PROGRAM_START')
s
k""")
        self.assertEquals('$2005: 00        brk', self.results[-3])

    def test_k_no_jsr(self):
        suite.banner(self.test_k_no_jsr) 
        self.run_test("""
a(lda_imm, 0x11)
a(lda_imm, 0x22)
a(brk)
a(nop)
s('PROGRAM_START')
k""")
        self.assertEquals('$2002: a9 22     lda #$22', self.results[-3])

