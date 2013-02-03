#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_load_store.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestLoadStore(execution.TestHarness):
        
    def test_lda(self):
        suite.banner(self.test_lda)
        a = self.a
        
        _;      a(lda_imm, 0x42) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.n)
        
    def test_lda_zero(self):
        suite.banner(self.test_lda_zero)
        a = self.a 
        
        _;      a(lda_imm, 0x00) 
        
        self.run_test() 
        self.assertEquals(0x00, self.cpu.a) 
        self.assertTrue(    self.cpu.z)
        self.assertTrue(not self.cpu.n)
        
    def test_lda_signed(self):
        suite.banner(self.test_lda_signed) 
        a = self.a
        
        _;      a(lda_imm, 0xff) 
        
        self.run_test() 
        self.assertEquals(0xff, self.cpu.a) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(    self.cpu.n)
        
    def test_ldx(self):
        suite.banner(self.test_ldx) 
        a = self.a
        
        _;      a(ldx_imm, 0x42) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.x) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.n)
        
    def test_ldx_zero(self):
        suite.banner(self.test_ldx_zero) 
        a = self.a
        
        _;      a(ldx_imm, 0x00) 
        
        self.run_test() 
        self.assertEquals(0x00, self.cpu.x) 
        self.assertTrue(    self.cpu.z)
        self.assertTrue(not self.cpu.n)
        
    def test_ldx_signed(self):
        suite.banner(self.test_ldx_signed) 
        a = self.a
        
        _;      a(ldx_imm, 0xff) 
        
        self.run_test() 
        self.assertEquals(0xff, self.cpu.x) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(    self.cpu.n)
        
    def test_ldy(self):
        suite.banner(self.test_ldy)
        a = self.a
        
        _;      a(ldy_imm, 0x42) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.y) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.n)
        
    def test_ldy_zero(self):
        suite.banner(self.test_ldy_zero)
        a = self.a
        
        _;      a(ldy_imm, 0x00) 
        
        self.run_test() 
        self.assertEquals(0x00, self.cpu.y) 
        self.assertTrue(    self.cpu.z)
        self.assertTrue(not self.cpu.n)
        
    def test_ldy_signed(self):
        suite.banner(self.test_ldy_signed) 
        a = self.a 
        
        _;      a(ldy_imm, 0xff) 
        
        self.run_test() 
        self.assertEquals(0xff, self.cpu.y) 
        self.assertTrue(not self.cpu.z)
        self.assertTrue(    self.cpu.n)
        
    def test_lda_abs(self):
        suite.banner(self.test_lda_abs) 
        a = self.a
        self.mem[0xdddd] = 0x42
                 
        _;      a(lda_abs, 0xdddd)
        
        self.run_test()
        self.assertEquals(0x42, self.cpu.a) 

    def test_ldx_abs(self):
        suite.banner(self.test_ldx_abs) 
        a = self.a
        self.mem[0xdddd] = 0x42
                 
        _;      a(ldx_abs, 0xdddd)
        
        self.run_test()
        self.assertEquals(0x42, self.cpu.x) 
            
    def test_ldy_abs(self):
        suite.banner(self.test_ldy_abs) 
        a = self.a
        self.mem[0xdddd] = 0x42
                 
        _;      a(ldy_abs, 0xdddd)
        
        self.run_test()
        self.assertEquals(0x42, self.cpu.y) 

    def test_sta_abs(self):
        suite.banner(self.test_sta_abs)
        a = self.a
        
        _;      a(lda_imm,  0x42) 
        _;      a(sta_abs,  0xdddd) 
        
        self.run_test()
        self.assertEquals(0x42, self.mem[0xdddd])

    def test_stx_abs(self):
        suite.banner(self.test_stx_abs)
        a = self.a 
        
        _;      a(ldx_imm,  0x42) 
        _;      a(stx_abs,  0xdddd) 
        
        self.run_test()
        self.assertEquals(0x42, self.mem[0xdddd])
        
    def test_sty_abs(self):
        suite.banner(self.test_sty_abs)
        a = self.a
        
        _;      a(ldy_imm,  0x42) 
        _;      a(sty_abs,  0xdddd) 
        
        self.run_test()
        self.assertEquals(0x42, self.mem[0xdddd])
        
    def test_lda_zp(self):
        suite.banner(self.test_lda_zp) 
        a = self.a 
        self.mem[0x01] = 0x42
        
        _;      a(lda_zp,   0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 

    def test_ldx_zp(self):
        suite.banner(self.test_ldx_zp)
        a = self.a
        self.mem[0x01] = 0x42
        
        _;      a(ldx_zp,   0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.x) 
        
    def test_ldy_zp(self):
        suite.banner(self.test_ldy_zp)
        a = self.a
        self.mem[0x01] = 0x42
        
        _;      a(ldy_zp,   0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.y) 
                
    def test_sta_zp(self):
        suite.banner(self.test_sta_zp)
        a = self.a
        
        _;      a(lda_imm,  0x42) 
        _;      a(sta_zp,   0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.mem[0x01])

    def test_stx_zp(self):
        suite.banner(self.test_stx_zp)
        a = self.a
        
        _;      a(ldx_imm,  0x42) 
        _;      a(stx_zp,   0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.mem[0x01])
        
    def test_sty_zp(self):
        suite.banner(self.test_sty_zp)
        a = self.a 
        
        _;      a(ldy_imm,  0x42) 
        _;      a(sty_zp,   0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.mem[0x01])
                
    def test_lda_zpx(self):
        suite.banner(self.test_lda_zpx) 
        a = self.a
        self.mem[0x05] = 0x42
        
        _;      a(ldx_imm, 0x05) 
        _;      a(lda_zpx, 0x00) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 

    def test_ldx_zpy(self):
        suite.banner(self.test_ldx_zpy) 
        a = self.a
        self.mem[0x5] = 0x42
        
        _;      a(ldy_imm, 0x05) 
        _;      a(ldx_zpy, 0x00) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.x) 
                
    def test_ldy_zpx(self):
        suite.banner(self.test_ldy_zpx) 
        a = self.a
        self.mem[0x5] = 0x42
        
        _;      a(ldx_imm, 0x05) 
        _;      a(ldy_zpx, 0x00) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.y) 
        
    def test_lda_abx(self):
        suite.banner(self.test_lda_abx) 
        a = self.a
        self.mem[0xdddd] = 0x42
        
        _;      a(ldx_imm,  0xdd)
        _;      a(lda_abx,  0xdd00)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 

    def test_ldx_aby(self):
        suite.banner(self.test_ldx_aby) 
        a = self.a
        self.mem[0xdddd] = 0x42
        
        _;      a(ldy_imm,  0xdd)
        _;      a(ldx_aby,  0xdd00)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.x) 

    def test_ldy_abx(self):
        suite.banner(self.test_ldy_abx) 
        a = self.a
        self.mem[0xdddd] = 0x42
        
        _;      a(ldx_imm,  0xdd)
        _;      a(ldy_abx,  0xdd00)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.y) 
                
    def test_lda_izx(self):
        suite.banner(self.test_lda_izx)
        a = self.a
        self.mem[0xdddd] = 0x42
        
        _;      a.macro     (ldxy_imm, 0xdddd)
        _;      a.macro     (stxy_zp,  0xa)
        _;      a(ldx_imm,  0x0a)
        _;      a(lda_izx,  0x00)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 
        
    def test_sta_izx(self):
        suite.banner(self.test_sta_izx) 
        a = self.a
        
        _;      a.macro     (ldxy_imm, 0xdddd)
        _;      a.macro     (stxy_zp,  0x0a) 
        _;      a(ldx_imm,  0x0a) 
        _;      a(lda_imm,  0x42)
        _;      a(sta_zpx,  0x00) 
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 
          
    def test_lda_izy(self):
        suite.banner(self.test_lda_izy) 
        a = self.a
        self.mem[0xdddd] = 0x42
        
        _;      a.macro     (ldxy_imm, 0xdd00)
        _;      a.macro     (stxy_zp,  0x01)
        _;      a(ldy_imm,  0xdd) 
        _;      a(lda_izy,  0x1)
        
        self.run_test() 
        self.assertEquals(0x42, self.cpu.a) 
        
    def test_sta_izy(self):
        suite.banner(self.test_sta_izy)
        a = self.a
        
        _;      a.macro     (ldxy_imm, 0xdd00)
        _;      a.macro     (stxy_zp,  0x01)
        _;      a(ldy_imm,  0xdd) 
        _;      a(lda_imm,  0x42)
        _;      a(sta_izy,  0x01)
        
        self.run_test() 
        self.assertEquals(0x42, self.mem[0xdddd])
