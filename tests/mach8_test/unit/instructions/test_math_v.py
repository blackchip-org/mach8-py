#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_math_v.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestMathV(execution.TestHarness):
    
    def test_adc_v1(self):
        suite.banner(self.test_adc_v1) 
        a = self.a
        
        _;      a.remark    ('1 + 1 = 2, returns V = 0')
        _;      a(clc) 
        _;      a(lda_imm,  0x01) 
        _;      a(adc_imm,  0x01) 
        
        self.run_test()
        self.assertEquals(0x02, self.cpu.a) 
        self.assertFalse(self.cpu.v) 
        self.assertFalse(self.cpu.c) 
    
    def test_adc_v2(self):
        suite.banner(self.test_adc_v2) 
        a = self.a
        
        _;      a.remark    ('1 + -1 = 0, returns V = 0')
        _;      a(clc) 
        _;      a(lda_imm,  0x01) 
        _;      a(adc_imm,  0xff)
         
        self.run_test() 
        self.assertEquals(0x00, self.cpu.a) 
        self.assertFalse(self.cpu.v) 
        self.assertTrue(self.cpu.c) 
        
    def test_adc_v3(self):
        suite.banner(self.test_adc_v3) 
        a = self.a 
        
        _;      a.remark    ('127 + 1 = 128, returns V = 1')
        _;      a(clc) 
        _;      a(lda_imm,  0x7f) 
        _;      a(adc_imm,  0x01) 
        
        self.run_test() 
        self.assertEquals(0x80, self.cpu.a) 
        self.assertTrue(self.cpu.v) 
        self.assertFalse(self.cpu.c) 
        
    def test_adc_v4(self):
        suite.banner(self.test_adc_v4) 
        a = self.a 
        
        _;      a.remark    ('-128 + -1 = -129, returns V = 1')
        _;      a(clc) 
        _;      a(lda_imm,  0x80) 
        _;      a(adc_imm,  0xff) 
        
        self.run_test() 
        self.assertEquals(0x7f, self.cpu.a) 
        self.assertTrue(self.cpu.v) 
        self.assertTrue(self.cpu.c) 
           
    def test_sbc_v1(self):
        suite.banner(self.test_sbc_v1) 
        a = self.a
        
        _;      a.remark    ('0 - 1 = -1, returns V = 0')
        _;      a(sec) 
        _;      a(lda_imm,  0x00)
        _;      a(sbc_imm,  0x01) 
        
        self.run_test() 
        self.assertEquals(0xff, self.cpu.a) 
        self.assertFalse(self.cpu.v) 
        
    def test_sbc_v2(self):
        suite.banner(self.test_sbc_v2) 
        a = self.a 

        _;      a.remark    ('-128 - 1 = -129, returns V = 1')
        _;      a(sec) 
        _;      a(lda_imm,  0x80)
        _;      a(sbc_imm,  0x01)
         
        self.run_test() 
        self.assertEquals(0x7f, self.cpu.a) 
        self.assertTrue(self.cpu.v)
        
    def test_sbc_v3(self):
        suite.banner(self.test_sbc_v3) 
        a = self.a 

        _;      a.remark    ('127 - -1 = 128, returns V = 1')
        _;      a(sec) 
        _;      a(lda_imm,  0x7f)
        _;      a(sbc_imm,  0xff) 
        
        self.run_test() 
        self.assertEquals(0x80, self.cpu.a) 
        self.assertTrue(self.cpu.v)
        
    