#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_jmp.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestJMP(execution.TestHarness):
    
    def test_jmp_abs(self):
        suite.banner(self.test_jmp_abs) 
        a = self.a 

        _;      a(jmp_abs,  'test.exit')
        _;      a(brk)
        
        _;  a('test.exit')
        _;      a(lda_imm,  0x42)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a);

    def test_jmp_ind(self):
        suite.banner(self.test_jmp_ind) 
        a = self.a
        
        _;      a.macro     (ldxy_imm, 'test.exit')
        _;      a.macro     (stxy_zp,  0x1)
        _;      a(jmp_ind,  0x1)
        _;      a(brk)
        
        _;  a('test.exit')
        _;      a(lda_imm,  0x42)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 
