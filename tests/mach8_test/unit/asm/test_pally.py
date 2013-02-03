#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011-2012, Reprint what you like.
#
# $Id: test_pally.py 131 2012-01-28 02:18:29Z mcgann $
#------------------------------------------------------------------------------
from asm import pally
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestPally(execution.TestHarness):
            
    def test_true(self):
        suite.banner(self.test_true) 
        a = self.a 
        
        _;      a.macro     (ldxy_imm, 'pally_string')
        _;      a(jsr,      'is_pally')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('pally_string')
        _;      a.data      ('1234321', 0) 

        pally.assemble(a)         
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        
    def test_false(self):
        suite.banner(self.test_false) 
        a = self.a 
        
        _;      a.macro     (ldxy_imm, 'pally_string')
        _;      a(jsr,      'is_pally')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('pally_string')
        _;      a.data      ('1234x21', 0) 

        pally.assemble(a)         
        self.run_test() 
        self.assertEquals(1, self.cpu.a) 
        
    def test_empty(self):
        suite.banner(self.test_false) 
        a = self.a 
        
        _;      a.macro     (ldxy_imm, 'pally_string')
        _;      a(jsr,      'is_pally')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('pally_string')
        _;      a.data      (0) 

        pally.assemble(a)         
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 

        