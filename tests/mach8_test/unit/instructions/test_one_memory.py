#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_one_memory.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestOneMemory(execution.TestHarness):
    
    #-----
    # INC
    #-----
    def test_inc_zp(self):
        suite.banner(self.test_inc_zp) 
        a = self.a

        _;      a(lda_imm,  0x88)
        _;      a(sta_zp,   0x12)
        _;      a(inc_zp,   0x12)
        _;      a(ldx_zp,   0x12)
        
        self.run_test()
        self.assertEquals(0x89, self.cpu.x)
        self.assertTrue(self.cpu.n and not self.cpu.z)

    def test_inc_zpx(self):
        suite.banner(self.test_inc_zpx) 
        a = self.a 

        _;      a(lda_imm,  0x22)
        _;      a(sta_zp,   0x55)
        _;      a(ldx_imm,  0x05)
        _;      a(inc_zpx,  0x50)
        _;      a(ldy_zp,   0x55)
        
        self.run_test()
        self.assertEquals(0x23, self.cpu.y)
        self.assertTrue(not self.cpu.n and not self.cpu.z)

    def test_inc_abs(self):
        suite.banner(self.test_inc_abs) 
        a = self.a
        
        _;      a(lda_imm,  0x33)
        _;      a(sta_abs,  0x8000)
        _;      a(inc_abs,  0x8000)
        _;      a(ldx_abs,  0x8000)
        
        self.run_test() 
        self.assertEquals(0x34, self.cpu.x)

    def test_inc_abx(self):
        suite.banner(self.test_inc_abx) 
        a = self.a
        
        _;      a(lda_imm,  0x34)
        _;      a(sta_abs,  0x8000) 
        _;      a(ldx_imm,  0x03)
        _;      a(inc_abx,  0x7ffd)
        _;      a(ldy_abs,  0x8000)
        
        self.run_test() 
        self.assertEquals(0x35, self.cpu.y)

    def test_inc_wrap(self):
        suite.banner(self.test_inc_wrap) 
        a = self.a

        _;      a(lda_imm,  0xff)
        _;      a(sta_abs,  0x8002)
        _;      a(inc_abs,  0x8002)
        _;      a(ldx_abs,  0x8002)
        
        self.run_test() 
        self.assertEquals(0x00, self.cpu.x)

    #-----
    # DEC 
    #-----
    def test_dec_zp(self):
        suite.banner(self.test_dec_zp) 
        a = self.a

        _;      a(lda_imm,  0x88)
        _;      a(sta_zp,   0x12)
        _;      a(dec_zp,   0x12)
        _;      a(ldx_zp,   0x12)
        
        self.run_test()
        self.assertEquals(0x87, self.cpu.x)
        self.assertTrue(self.cpu.n and not self.cpu.z)

    def test_dec_zpx(self):
        suite.banner(self.test_dec_zpx) 
        a = self.a

        _;      a(lda_imm,  0x22)
        _;      a(sta_zp,   0x55)
        _;      a(ldx_imm,  0x05)
        _;      a(dec_zpx,  0x50)
        _;      a(ldy_zp,   0x55)
        
        self.run_test()
        self.assertEquals(0x21, self.cpu.y)
        self.assertTrue(not self.cpu.n and not self.cpu.z)

    def test_dec_abs(self):
        suite.banner(self.test_dec_abs) 
        a = self.a
        
        _;      a(lda_imm,  0x33)
        _;      a(sta_abs,  0x8000)
        _;      a(dec_abs,  0x8000)
        _;      a(ldx_abs,  0x8000)
        
        self.run_test() 
        self.assertEquals(0x32, self.cpu.x)

    def test_dec_abx(self):
        suite.banner(self.test_dec_abx) 
        a = self.a

        _;      a(lda_imm,  0x34)
        _;      a(sta_abs,  0x8000) 
        _;      a(ldx_imm,  0x03)
        _;      a(dec_abx,  0x7ffd)
        _;      a(ldy_abs,  0x8000)
        
        self.run_test() 
        self.assertEquals(0x33, self.cpu.y)

    def test_dec_wrap(self):
        suite.banner(self.test_dec_wrap) 
        a = self.a 

        _;      a(lda_imm,  0x00)
        _;      a(sta_abs,  0x8002)
        _;      a(dec_abs,  0x8002)
        _;      a(ldx_abs,  0x8002)

        self.run_test() 
        self.assertEquals(0xff, self.cpu.x)
    