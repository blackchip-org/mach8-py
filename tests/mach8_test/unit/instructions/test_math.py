#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_math.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestMath(execution.TestHarness):

    #----------
    # ADC 
    #----------
    def test_adc_flags(self):   
        suite.banner(self.test_adc_flags)       
        a = self.a

        _;      a(clc)
        _;      a(lda_imm,  0x40)
        _;      a(adc_imm,  0x05)
        
        self.run_test()
        self.assertEquals(0x45, self.cpu.a)
        self.assertTrue(not self.cpu.n)
        self.assertTrue(not self.cpu.v)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c) 

    def test_adc_v(self):
        suite.banner(self.test_adc_v) 
        a = self.a 
        
        _;      a(clc)
        _;      a(lda_imm,  0x7f) 
        _;      a(adc_imm,  0x01)
         
        self.run_test()
        self.assertTrue(self.cpu.v) 
        
    def test_adc_v_clear(self):
        suite.banner(self.test_adc_v_clear) 
        a = self.a
        
        _;      a(clc)
        _;      a(lda_imm,  0x81)
        _;      a(adc_imm,  0xff)
         
        self.run_test()
        self.assertEquals(0x80, self.cpu.a) 
        self.assertTrue(not self.cpu.v)
        
    def test_adc_nv(self):
        suite.banner(self.test_adc_nv) 
        a = self.a 
        
        _;      a(clc)
        _;      a(lda_imm,  0x45)
        _;      a(adc_imm,  0x50)
        
        self.run_test()
        self.assertEquals(0x95, self.cpu.a)
        self.assertTrue(    self.cpu.n)
        self.assertTrue(    self.cpu.v)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c)

    def test_adc_clear2(self):
        suite.banner(self.test_adc_clear2) 
        a = self.a 
        
        _;      a(clc) 
        _;      a(lda_imm,  0x95)
        _;      a(adc_imm,  0x0b)
        
        self.run_test()
        self.assertEquals(0xa0, self.cpu.a)
        self.assertTrue(    self.cpu.n)
        self.assertTrue(not self.cpu.v)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c)
        
    def test_adc_wrap(self):
        suite.banner(self.test_adc_wrap) 
        a = self.a 
        
        _;      a(clc)
        _;      a(lda_imm,  0xa0)
        _;      a(adc_imm,  0x60)
        
        self.run_test()
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(not self.cpu.n)
        self.assertTrue(not self.cpu.v) 
        self.assertTrue(    self.cpu.z)
        self.assertTrue(    self.cpu.c)

    def test_adc_16(self):
        suite.banner(self.test_adc_16) 
        a = self.a
        
        _;      a.remark    ('Add $2312')
        _;      a(lda_imm,  0x12)
        _;      a(sta_zp,   0xa0)
        _;      a(lda_imm,  0x23)
        _;      a(sta_zp,   0xa1)
        
        _;      a.remark    ('to $3322')
        _;      a(lda_imm,  0x22)
        _;      a(sta_zp,   0xa2)
        _;      a(lda_imm,  0x33)
        _;      a(sta_zp,   0xa3) 
        
        _;      a.remark    ('Perform addition')
        _;      a(clc)
        _;      a(lda_zp,  0xa0)
        _;      a(adc_zp,  0xa2)
        _;      a(sta_zp,  0xa4)
        _;      a(lda_zp,  0xa1)
        _;      a(adc_zp,  0xa3)
        _;      a(sta_zp,  0xa5)

        _;      a.remark    ('equals $5634')        
        _;      a(ldx_zp,  0xa4)
        _;      a(ldy_zp,  0xa5)
        
        self.run_test()
        self.assertEquals(0x34, self.cpu.x) 
        self.assertEquals(0x56, self.cpu.y)

    def test_adc_bcd(self):
        suite.banner(self.test_adc_bcd) 
        a = self.a

        _;      a(sed)
        _;      a(clc)
        _;      a(lda_imm,  0x32)
        _;      a(sta_abs,  0x8000)
        _;      a(lda_imm,  0x58)
        _;      a(adc_abs,  0x8000)
        
        self.run_test()
        self.assertEquals(0x90, self.cpu.a) 
        
    def test_adc_bcd_carry(self):
        suite.banner(self.test_adc_bcd_carry) 
        a = self.a 
        
        _;      a(sed)
        _;      a(clc) 
        _;      a(lda_imm,  0x90)
        _;      a(ldx_imm,  0x15)
        _;      a(stx_abs,  0x8000)
        _;      a(adc_abs,  0x8000)
        
        self.run_test()
        self.assertEquals(0x05, self.cpu.a) 
        self.assertTrue(self.cpu.c) 

    def test_adc_zpx(self):
        suite.banner(self.test_adc_zpx) 
        a = self.a 
        
        _;      a(clc)
        _;      a(lda_imm,  0x30)
        _;      a(sta_zp,   0xa4)
        _;      a(lda_imm,  0x02)
        _;      a(ldx_imm,  0x04)
        _;      a(adc_zpx,  0xa0)
        
        self.run_test()
        self.assertEquals(0x32, self.cpu.a)

    def test_adc_abs(self):
        suite.banner(self.test_adc_abs) 
        a = self.a 

        _;      a(clc)
        _;      a(lda_imm,  0x10)
        _;      a(sta_abs,  0xaaaa)
        _;      a(lda_imm,  0x02)
        _;      a(adc_abs,  0xaaaa)
        
        self.run_test()
        self.assertEquals(0x12, self.cpu.a) 

    def test_adc_abx(self):
        suite.banner(self.test_adc_abx)
        a = self.a

        _;      a(clc) 
        _;      a(lda_imm,  0x30)
        _;      a(sta_abs,  0xa004)
        _;      a(lda_imm,  0x05)
        _;      a(ldx_imm,  0x04)
        _;      a(adc_abx,  0xa000)
        
        self.run_test()
        self.assertEquals(0x35, self.cpu.a) 

    def test_adc_aby(self):
        suite.banner(self.test_adc_aby) 
        a = self.a
        
        _;      a(clc)
        _;      a(lda_imm,  0x50)
        _;      a(sta_abs,  0xa005)
        _;      a(lda_imm,  0x06)
        _;      a(ldy_imm,  0x05)
        _;      a(adc_aby,  0xa000)
        
        self.run_test()
        self.assertEquals(0x56, self.cpu.a) 

    def test_adc_izx(self):
        suite.banner(self.test_adc_izx) 
        a = self.a 

        _;      a(clc)
        _;      a(lda_imm,  0x55)
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5010)) 
        _;      a.macro     (stxy_zp,   x8(0xfe)) 
        
        _;      a(ldx_imm,  0x0e)
        _;      a(lda_imm,  0x03)
        _;      a(adc_izx,  0xf0)
        
        self.run_test()
        self.assertEquals(0x58, self.cpu.a) 

    def test_adc_izy(self):
        suite.banner(self.test_adc_izy) 
        a = self.a

        _;      a(clc) 
        _;      a(lda_imm,  0x66)
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5000)) 
        _;      a.macro     (stxy_zp,   x8(0xfe)) 
        
        _;      a(lda_imm,  0x03)
        _;      a(ldy_imm,  0x10)
        _;      a(adc_izy,  0xfe)
        
        self.run_test()
        self.assertEquals(0x69, self.cpu.a) 

    #----------
    # SBC 
    #----------
    def test_sbc_flags(self):      
        suite.banner(self.test_sbc_flags)    
        a = self.a
        
        _;      a(sec)
        _;      a(lda_imm,  0x45)
        _;      a(sbc_imm,  0x05)
        
        self.run_test()
        self.assertEquals(0x40, self.cpu.a)
        self.assertTrue(not self.cpu.n)
        self.assertTrue(not self.cpu.v)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(    self.cpu.c) 

    def test_sbc_v_set(self):
        suite.banner(self.test_sbc_v_set) 
        a = self.a 
        
        _;      a(sec)
        _;      a(lda_imm,  0x80) 
        _;      a(sbc_imm,  0x01) 
        
        self.run_test()
        self.assertEquals(0x7f, self.cpu.a) 
        self.assertTrue(self.cpu.v) 
        
    def test_sbc_v_clear(self):
        suite.banner(self.test_sbc_v_clear) 
        a = self.a 
        
        _;      a(sec)
        _;      a(lda_imm,  0x81)
        _;      a(sbc_imm,  0xff) 
        
        self.run_test()
        self.assertTrue(not self.cpu.v)
        
    def test_sbc_n(self):
        suite.banner(self.test_sbc_n)
        a = self.a 
        
        _;      a(sec)
        _;      a(lda_imm,  0x75)
        _;      a(sbc_imm,  0x85)
        
        self.run_test()
        self.assertEquals(0xf0, self.cpu.a)
        self.assertTrue(    self.cpu.n)
        self.assertTrue(    self.cpu.v) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c)

    def test_sbc_v_clear2(self):
        suite.banner(self.test_sbc_v_clear2) 
        a = self.a 
        
        _;      a(sec)
        _;      a(lda_imm,  0xf0)
        _;      a(sbc_imm,  0x10)
        
        self.run_test()
        self.assertEquals(0xe0, self.cpu.a)
        self.assertTrue(    self.cpu.n)
        self.assertTrue(not self.cpu.v)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(    self.cpu.c)
             
    def test_sbc_c_clear(self):
        suite.banner(self.test_sbc_c_clear) 
        a = self.a 
        
        _;      a(sec)
        _;      a(lda_imm,  0x00)
        _;      a(sbc_imm,  0x01)
         
        self.run_test()
        self.assertEquals(0xff, self.cpu.a)
        self.assertTrue(    self.cpu.n)
        self.assertTrue(not self.cpu.v)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c)
           
    def test_sbc_16(self):
        suite.banner(self.test_sbc_16) 
        a = self.a
        
        _;      a.remark    ('From $3322')
        _;      a(lda_imm,  0x22)
        _;      a(sta_zp,   0xa0)
        _;      a(lda_imm,  0x33)
        _;      a(sta_zp,   0xa1)
        
        _;      a.remark    ('subtract $1012')
        _;      a(lda_imm,  0x12)
        _;      a(sta_zp,   0xa2)
        _;      a(lda_imm,  0x10)
        _;      a(sta_zp,   0xa3) 
        
        _;      a.remark    ('Perform subtraction')
        _;      a(sec)
        _;      a(lda_zp,   0xa0)
        _;      a(sbc_zp,   0xa2)
        _;      a(sta_zp,   0xa4)
        _;      a(lda_zp,   0xa1)
        _;      a(sbc_zp,   0xa3)
        _;      a(sta_zp,   0xa5)
        
        _;      a.remark    ('equals $2310')
        _;      a(ldx_zp,   0xa4)
        _;      a(ldy_zp,   0xa5)
        
        self.run_test()
        self.assertEquals(0x10, self.cpu.x) 
        self.assertEquals(0x23, self.cpu.y)

    def test_sbc_bcd(self):
        suite.banner(self.test_sbc_bcd) 
        a = self.a

        _;      a(sed)
        _;      a(sec)
        _;      a(lda_imm,  0x90)
        _;      a(sbc_imm,  0x01)
        
        self.run_test()
        self.assertEquals(0x89, self.cpu.a) 
        
    def test_sbc_bcd_carry(self):
        suite.banner(self.test_sbc_bcd_carry) 
        a = self.a 
        
        _;      a(sed)
        _;      a(sec)
        _;      a(lda_imm,  0x01)
        _;      a(sbc_imm,  0x02)
        
        self.run_test()
        self.assertEquals(0x99, self.cpu.a) 
        self.assertFalse(self.cpu.c) 

    def test_sbc_zpx(self):
        suite.banner(self.test_sbc_zpx) 
        a = self.a
        
        _;      a(sec)
        _;      a(lda_imm,  0x04)
        _;      a(sta_zp,   0x15)
        _;      a(lda_imm,  0x38)
        _;      a(ldx_imm,  0x05)
        _;      a(sbc_zpx,  0x10)
        
        self.run_test()
        self.assertEquals(0x34, self.cpu.a)

    def test_sbc_abs(self):
        suite.banner(self.test_sbc_abs) 
        a = self.a
        
        _;      a(sec) 
        _;      a(lda_imm,  0x06)
        _;      a(sta_abs,  0x8000)
        _;      a(lda_imm,  0x77)
        _;      a(sbc_abs,  0x8000)
        
        self.run_test()
        self.assertEquals(0x71, self.cpu.a) 

    def test_sbc_abx(self):
        suite.banner(self.test_sbc_abx) 
        a = self.a 
  
        _;      a(sec)       
        _;      a(lda_imm,  0x02)
        _;      a(sta_abs,  0x8033)
        _;      a(lda_imm,  0x80)
        _;      a(ldx_imm,  0x33)
        _;      a(sbc_abx,  0x8000)
        
        self.run_test()
        self.assertEquals(0x7e, self.cpu.a) 

    def test_sbc_aby(self):
        suite.banner(self.test_sbc_aby) 
        a = self.a 

        _;      a(sec) 
        _;      a(lda_imm,  0x03)
        _;      a(sta_abs,  0x8044)
        _;      a(lda_imm,  0x80)
        _;      a(ldy_imm,  0x44)
        _;      a(sbc_aby,  0x8000)
        
        self.run_test()
        self.assertEquals(0x7d, self.cpu.a) 

    def test_sbc_izx(self):
        suite.banner(self.test_sbc_izx) 
        a = self.a
        
        _;      a(sec) 
        _;      a(lda_imm,  0x03)
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5010))
        _;      a.macro     (stxy_zp,   x8(0xfe)) 
        
        _;      a(ldx_imm,  0x0e)
        _;      a(lda_imm,  0x55)
        _;      a(sbc_izx,  0xf0)
        
        self.run_test()
        self.assertEquals(0x52, self.cpu.a) 

    def test_sbc_izy(self):
        suite.banner(self.test_sbc_izy) 
        a = self.a 

        _;      a(sec) 
        _;      a(lda_imm,  0x03)
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5000))
        _;      a.macro     (stxy_zp,   x8(0xfe))
        
        _;      a(lda_imm,  0x66)
        _;      a(ldy_imm,  0x10)
        _;      a(sbc_izy,  0xfe)
        
        self.run_test()
        self.assertEquals(0x63, self.cpu.a) 

    