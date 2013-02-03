#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_jsr.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestJSR(execution.TestHarness):
    
    def test_jsr_rts(self):
        suite.banner(self.test_jsr_rts)
        a = self.a 
        
        _;      a(jsr,      'test.jsr')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.jsr')
        _;      a(lda_imm,  0x42) 
        _;      a(rts) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 