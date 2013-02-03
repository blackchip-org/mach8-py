#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_branch.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestBranch(execution.TestHarness):
    
    def test_bra(self):
        suite.banner(self.test_bra)   
        a = self.a
        
        _;      a(bra,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(lda_imm,  0xbb)
        
        self.run_test()
        self.assertEquals(0xbb, self.cpu.a) 

    def test_bne_true(self):
        suite.banner(self.test_bne_true) 
        a = self.a
        
        _;      a(lda_imm,  1)
        _;      a(bne,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 

    def test_bne_false(self):
        suite.banner(self.test_bne_false) 
        a = self.a
        
        _;      a(lda_imm,  0)
        _;      a(bne,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
                
    def test_beq(self):
        suite.banner(self.test_beq) 
        a = self.a
        
        _;      a(lda_imm,  0)
        _;      a(beq,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 

    def test_beq_false(self):
        suite.banner(self.test_beq_false) 
        a = self.a
        
        _;      a(lda_imm,  1)
        _;      a(beq,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
                
    def test_bpl(self):
        suite.banner(self.test_bpl)
        a = self.a
        
        _;      a(lda_imm,  1)
        _;      a(bpl,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 
        
    def test_bpl_false(self):
        suite.banner(self.test_bpl_false)
        a = self.a
        
        _;      a(lda_imm,  0xff)
        _;      a(bpl,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
        
    def test_bmi(self):
        suite.banner(self.test_bmi) 
        a = self.a
        
        _;      a(lda_imm,  0xff)
        _;      a(bmi,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 

    def test_bmi_false(self):
        suite.banner(self.test_bmi_false) 
        a = self.a
        
        _;      a(lda_imm,  1)
        _;      a(bmi,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
        
    def test_bvc(self):
        suite.banner(self.test_bvc) 
        a = self.a
        
        _;      a(clc) 
        _;      a(lda_imm,  0xff)
        _;      a(adc_imm,  0x01)    
        _;      a(bvc,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 
        
    def test_bvc_false(self):
        suite.banner(self.test_bvc_false)
        a = self.a
        
        _;      a(clc)
        _;      a(lda_imm,  0x7f)
        _;      a(adc_imm,  0x01)    
        _;      a(bvc,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
        
    def test_bvs(self):
        suite.banner(self.test_bvs) 
        a = self.a
        
        _;      a(clc)
        _;      a(lda_imm,  0x7f)
        _;      a(adc_imm,  0x01)    
        _;      a(bvs,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 
        
    def test_bvs_false(self):
        suite.banner(self.test_bvs_false) 
        a = self.a
        
        _;      a(clc) 
        _;      a(lda_imm,  0xff)
        _;      a(adc_imm,  0x01)    
        _;      a(bvs,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
        
    def test_bcc(self):
        suite.banner(self.test_bcc) 
        a = self.a
        
        _;      a(clc) 
        _;      a(lda_imm,  0x00)
        _;      a(adc_imm,  0x01)    
        _;      a(bcc,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 
        
    def test_bcc_false(self):
        suite.banner(self.test_bcc_false) 
        a = self.a
        
        _;      a(clc) 
        _;      a(lda_imm,  0xff)
        _;      a(adc_imm,  0x01)    
        _;      a(bcc,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
        
    def test_bcs(self):
        suite.banner(self.test_bcs) 
        a = self.a
        
        _;      a(clc) 
        _;      a(lda_imm,  0xff)
        _;      a(adc_imm,  0x01)    
        _;      a(bcs,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xbb, self.cpu.x) 
        
    def test_bcs_false(self):
        suite.banner(self.test_bcs_false) 
        a = self.a
        
        _;      a(clc) 
        _;      a(lda_imm,  0x00)
        _;      a(adc_imm,  0x01)    
        _;      a(bcs,      'test.exit')
        
        _;      a(ldx_imm,  0xaa)
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.exit')
        _;      a(ldx_imm,  0xbb)

        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
