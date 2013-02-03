#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_text.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8 import memmap
from mach8_test import suite
from mach8_test.harness import execution
from mach8 import vm 

class TestText(execution.TestHarness):
    
    def test_txtrst(self):
        suite.banner(self.test_txtrst)
        a = self.a 
        
        _;      a.macro     (ldxy_imm, x16(0xffff)) 
        _;      a.macro     (stxy_zp,  'TEXT_WORK_PTR')
        _;      a(jsr,      'TXTRST')
        _;      a.macro     (ldxy_zp, 'TEXT_WORK_PTR')
        
        self.run_test() 
        self.assertEquals(vm.lb(memmap.TEXT_WORK), self.cpu.x)
        self.assertEquals(vm.hb(memmap.TEXT_WORK), self.cpu.y) 
        
    def test_chrput(self):
        suite.banner(self.test_chrput) 
        a = self.a 
        
        _;      a(jsr,      'TXTRST')
        _;      a(lda_imm,  lb(0x1234))
        _;      a(jsr,      'CHRPUT')
        _;      a(lda_imm,  hb(0x1234))
        _;      a(jsr,      'CHRPUT')
        _;      a.macro     (ldxy_abs, 'TEXT_WORK')
        
        self.run_test() 
        self.assertEquals(0x34, self.cpu.x)
        self.assertEquals(0x12, self.cpu.y) 

    def test_txtout(self):
        suite.banner(self.test_txtout) 
        a = self.a 
        
        _;      a(ldx_imm,  0)
        
        _;  a('test.loop')
        _;      a(lda_abx,  'test.str')
        _;      a(sta_abx,  'TEXT_WORK')
        _;      a(beq,      'test.done')
        _;      a(inx)
        _;      a(bra,      'test.loop')
        
        _;  a('test.done')
        _;      a(jsr,      'TXTOUT')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.str')
        _;      a.data      ('123456')
        
        self.run_test()         
        self.assertEquals('123456', self.output.getvalue()) 
        
        