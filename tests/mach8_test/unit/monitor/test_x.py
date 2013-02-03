#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_x.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestX(console.TestHarness):
    
    def test_x(self):
        suite.banner(self.test_x)
        self.run_test("""
a(jsr, 'test.1') 
a(brk)
a(nop)
a('test.1')
a(lda_imm, 0x11)
a(lda_imm, 0x22)
a(lda_imm, 0x33) 
a(rts) 
s('PROGRAM_START')
s
x""")
        self.assertEquals('$2003: 00        brk', self.results[-3])
        
    def test_x_to_monitor(self):
        suite.banner(self.test_x_to_monitor) 
        self.run_test("""
a(lda_imm, 0x11)
a(lda_imm, 0x22)
a(lda_imm, 0x33) 
a(rts) 
s('PROGRAM_START')
x""")
