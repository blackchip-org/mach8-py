#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_bit_op.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution
from mach8 import vm 

class TestBitOp(execution.TestHarness):
            
    #----------
    # AND
    #----------
    def test_and_imm(self):
        suite.banner(self.test_and_imm) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(and_imm,  b8(0b00100110)) 
        
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a) 

    def test_and_z(self):
        suite.banner(self.test_and_z) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(and_imm,  b8(0b01010100)) 
        
        self.run_test()
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(self.cpu.z)

    def test_and_n(self):
        suite.banner(self.test_and_n) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b10001111)) 
        _;      a(and_imm,  b8(0b10000000)) 
        
        self.run_test() 
        self.assertTrue(self.cpu.n) 

    def test_and_zp(self):
        suite.banner(self.test_and_zp) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_zp,   0x44)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_zp,   0x44) 
        
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a) 

    def test_and_zpx(self):
        suite.banner(self.test_and_zpx) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_zp,   0x88)
        _;      a(ldx_imm,  0x08)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_zpx,  0x80)
         
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a)

    def test_and_abs(self):
        suite.banner(self.test_and_abs) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_abs,  0x8000)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_abs,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a)

    def test_and_abx(self):
        suite.banner(self.test_and_abx) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_abs,  0x8044)
        _;      a(ldx_imm,  0x44)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_abx,  0x8000) 
        
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a)

    def test_and_aby(self):
        suite.banner(self.test_and_aby) 
        a = self.a
        
        _;      a(ldx_imm,  b8(0b00101010)) 
        _;      a(stx_abs,  0x8022)
        _;      a(ldy_imm,  0x22)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_aby,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a)

    def test_and_izx(self):
        suite.banner(self.test_and_izx) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5010))
        _;      a.macro     (stxy_zp,   x8(0xfe)) 
        
        _;      a(ldx_imm,  0x0e)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_izx,  0xf0) 
        
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a)

    def test_and_izy(self):
        suite.banner(self.test_and_izy) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5000))
        _;      a.macro     (stxy_zp,   x8(0xfe))
        
        _;      a(ldy_imm,  0x10)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(and_izy,  0xfe) 
        
        self.run_test()
        self.assertEquals(0b00100010, self.cpu.a)

    #----------
    # EOR
    #----------
    def test_eor_imm(self):
        suite.banner(self.test_eor_imm)     
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010))
        _;      a(eor_imm,  b8(0b00100110))
        
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a) 

    def test_eor_z(self):
        suite.banner(self.test_eor_z) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010))
        _;      a(eor_imm,  b8(0b00101010))
        
        self.run_test()
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(self.cpu.z)
        self.assertFalse(self.cpu.n)

    def test_eor_n(self):
        suite.banner(self.test_eor_n) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00010100)) 
        _;      a(eor_imm,  b8(0b10010100)) 
        
        self.run_test() 
        self.assertFalse(self.cpu.z) 
        self.assertTrue(self.cpu.n) 

    def test_eor_zp(self):
        suite.banner(self.test_eor_zp) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_zp,   0x44)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_zp,   0x44)
         
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a) 

    def test_eor_zpx(self):
        suite.banner(self.test_eor_zpx) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_zp,   0x88)
        _;      a(ldx_imm,  0x08)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_zpx,  0x80) 
        
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a)

    def test_eor_abs(self):
        suite.banner(self.test_eor_abs) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_abs,  0x8000)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_abs,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a)

    def test_eor_abx(self):
        suite.banner(self.test_eor_abx) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_abs,  0x8044)
        _;      a(ldx_imm,  0x44)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_abx,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a)

    def test_eor_aby(self):
        suite.banner(self.test_eor_aby) 
        a = self.a
        
        _;      a(ldx_imm,  b8(0b00101010)) 
        _;      a(stx_abs,  0x8022)
        _;      a(ldy_imm,  0x22)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_aby,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a)

    def test_eor_izx(self):
        suite.banner(self.test_eor_izx) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5010))
        _;      a.macro     (stxy_zp,  0xfe)
        _;      a(ldx_imm,  0x0e)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_izx,  0xf0)
         
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a)

    def test_eor_izy(self):
        suite.banner(self.test_eor_izy) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5000))
        _;      a.macro     (stxy_zp,   x8(0xfe))
        
        _;      a(ldy_imm,  0x10)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(eor_izy,  0xfe) 
        
        self.run_test()
        self.assertEquals(0b00001100, self.cpu.a)

    #----------
    # ORA
    #----------
    def test_ora_imm(self):
        suite.banner(self.test_ora_imm)   
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010))
        _;      a(ora_imm,  b8(0b00100110))
        
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a) 

    def test_ora_z(self):
        suite.banner(self.test_ora_z) 
        a = self.a
        
        _;      a(lda_imm,  0)
        _;      a(eor_imm,  0)
        
        self.run_test()
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(self.cpu.z)
        self.assertFalse(self.cpu.n)

    def test_ora_n(self):
        suite.banner(self.test_ora_n)
        a = self.a
        
        _;      a(lda_imm,  b8(0b10010100)) 
        _;      a(ora_imm,  b8(0b10000100)) 
        
        self.run_test() 
        self.assertFalse(self.cpu.z) 
        self.assertTrue(self.cpu.n) 

    def test_ora_zp(self):
        suite.banner(self.test_ora_zp)
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_zp,   0x44)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_zp,   0x44)
         
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a) 

    def test_ora_zpx(self):
        suite.banner(self.test_ora_zpx) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_zp,   0x88)
        _;      a(ldx_imm,  0x08)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_zpx,  0x80)
         
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a)

    def test_ora_abs(self):
        suite.banner(self.test_ora_abs)
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_abs,  0x8000)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_abs,  0x8000) 
        
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a)

    def test_ora_abx(self):
        suite.banner(self.test_ora_abx) 
        a = self.a
        
        _;      a(ldy_imm,  b8(0b00101010)) 
        _;      a(sty_abs,  0x8044)
        _;      a(ldx_imm,  0x44)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_abx,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a)

    def test_ora_aby(self):
        suite.banner(self.test_ora_aby) 
        a = self.a
        
        _;      a(ldx_imm,  b8(0b00101010)) 
        _;      a(stx_abs,  0x8022)
        _;      a(ldy_imm,  0x22)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_aby,  0x8000)
         
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a)

    def test_ora_izx(self):
        suite.banner(self.test_ora_izx) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010))
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5010))
        _;      a.macro     (stxy_zp,   x8(0xfe))
        
        _;      a(ldx_imm,  0x0e)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_izx,  0xf0)
         
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a)

    def test_ora_izy(self):
        suite.banner(self.test_ora_izy) 
        a = self.a
        
        _;      a(lda_imm,  b8(0b00101010)) 
        _;      a(sta_abs,  0x5010)
        _;      a.macro     (ldxy_imm, x16(0x5000)) 
        _;      a.macro     (stxy_zp,   x8(0xfe))
        _;      a(ldy_imm,  0x10)
        _;      a(lda_imm,  b8(0b00100110)) 
        _;      a(ora_izy,  0xfe)
         
        self.run_test()
        self.assertEquals(0b00101110, self.cpu.a)
        