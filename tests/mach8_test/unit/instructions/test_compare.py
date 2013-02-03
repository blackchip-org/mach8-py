#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_compare.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestCompare(execution.TestHarness):
    
    #----------
    # CMP
    #----------
    def test_cmp_imm_zc(self):
        suite.banner(self.test_cmp_imm_zc) 
        a = self.a
        
        _;      a(lda_imm,  0x22)
        _;      a(cmp_imm,  0x22)
        
        self.run_test()
        self.assertTrue(    self.cpu.z)
        self.assertTrue(    self.cpu.c) 
        self.assertTrue(not self.cpu.n)
        
    def test_cmp_imm_n(self):
        suite.banner(self.test_cmp_imm_n) 
        a = self.a   
        
        _;      a(lda_imm,  0xaa)
        _;      a(cmp_imm,  0xbb)
        
        self.run_test()
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c) 
        self.assertTrue(    self.cpu.n)
        
    def test_cmp_imm_c(self):
        suite.banner(self.test_cmp_imm_c) 
        a = self.a   
        
        _;      a(lda_imm,  0x23)
        _;      a(cmp_imm,  0x22)
        
        self.run_test()
        self.assertTrue(not self.cpu.z) 
        self.assertTrue(    self.cpu.c) 
        self.assertTrue(not self.cpu.n)

    def test_cmp_zp(self):
        suite.banner(self.test_cmp_zp) 
        a = self.a
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_zp,   0xdd)
        _;      a(cmp_zp,   0xdd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cmp_zpx(self):
        suite.banner(self.test_cmp_zpx) 
        a = self.a
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_zp,   0xdd)
        _;      a(ldx_imm,  0x0d)
        _;      a(cmp_zp,   0xdd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)
        
    def test_cmp_abs(self):
        suite.banner(self.test_cmp_abs) 
        a = self.a 
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_abs,  0xdddd)
        _;      a(cmp_abs,  0xdddd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cmp_abx(self):
        suite.banner(self.test_cmp_abx) 
        a = self.a 
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_abs,  0xdddd)
        _;      a(ldx_imm,  0xdd)
        _;      a(cmp_abx,  0xdd00)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cmp_aby(self):
        suite.banner(self.test_cmp_aby) 
        a = self.a 
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_abs,  0xdddd)
        _;      a(ldy_imm,  0xdd)
        _;      a(cmp_aby,  0xdd00)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cmp_izx(self):
        suite.banner(self.test_cmp_izx) 
        a = self.a 
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_abs,  0xdddd)
        
        _;      a.macro     (ldxy_imm, x16(0xdddd))
        _;      a.macro     (stxy_zp,  x8(0x04))
        
        _;      a(ldx_imm,  0x04)
        _;      a(cmp_izx,  0x00)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cmp_izy(self):
        suite.banner(self.test_cmp_izy) 
        a = self.a   
        
        _;      a(lda_imm,  0x22)
        _;      a(sta_abs,  0xdddd)
        
        _;      a.macro     (ldxy_imm, x16(0xdd00))
        _;      a.macro     (stxy_zp,  0x01)
        
        _;      a(ldy_imm,  0xdd)
        _;      a(cmp_izy,  0x01)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    #----------
    # CPX
    #----------
    def test_cpx_imm_zc(self):
        suite.banner(self.test_cpx_imm_zc) 
        a = self.a
        
        _;      a(ldx_imm,  0x22)
        _;      a(cpx_imm,  0x22)
        
        self.run_test()
        self.assertTrue(    self.cpu.z)
        self.assertTrue(    self.cpu.c) 
        self.assertTrue(not self.cpu.n)
        
    def test_cpx_imm_n(self):
        suite.banner(self.test_cpx_imm_n) 
        a = self.a
        
        _;      a(ldx_imm,  0xaa)
        _;      a(cpx_imm,  0xbb)
        
        self.run_test()
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c) 
        self.assertTrue(    self.cpu.n)
        
    def test_cpx_imm_c(self):
        suite.banner(self.test_cpx_imm_c) 
        a = self.a
        
        _;      a(ldx_imm,  0x23)
        _;      a(cpx_imm,  0x22)
        
        self.run_test()
        self.assertTrue(not self.cpu.z) 
        self.assertTrue(    self.cpu.c) 
        self.assertTrue(not self.cpu.n)

    def test_cpx_zp(self):
        suite.banner(self.test_cpx_zp) 
        a = self.a
        
        _;      a(ldx_imm,  0x22)
        _;      a(stx_zp,   0xdd)
        _;      a(cpx_zp,   0xdd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cpx_abs(self):
        suite.banner(self.test_cpx_abs) 
        a = self.a
        
        _;      a(ldx_imm,  0x22)
        _;      a(stx_abs,  0xdddd)
        _;      a(cpx_abs,  0xdddd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    #----------
    # CPY 
    #----------
    def test_cpy_imm_zc(self):
        suite.banner(self.test_cpy_imm_zc) 
        a = self.a
        
        _;      a(ldy_imm,  0x22)
        _;      a(cpy_imm,  0x22)
        
        self.run_test()
        self.assertTrue(    self.cpu.z)
        self.assertTrue(    self.cpu.c) 
        self.assertTrue(not self.cpu.n)
        
    def test_cpy_imm_n(self):
        suite.banner(self.test_cpy_imm_n) 
        a = self.a
        
        _;      a(ldy_imm,  0xaa)
        _;      a(cpy_imm,  0xbb)
        
        self.run_test()
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.c) 
        self.assertTrue(    self.cpu.n)
        
    def test_cpy_imm_c(self):
        suite.banner(self.test_cpy_imm_c) 
        a = self.a
        
        _;      a(ldy_imm,  0x23)
        _;      a(cpy_imm,  0x22)
        
        self.run_test()
        self.assertTrue(not self.cpu.z) 
        self.assertTrue(    self.cpu.c) 
        self.assertTrue(not self.cpu.n)

    def test_cpy_zp(self):
        suite.banner(self.test_cpy_zp) 
        a = self.a  
        
        _;      a(ldy_imm,  0x22)
        _;      a(sty_zp,   0xdd)
        _;      a(cpy_zp,   0xdd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)

    def test_cpy_abs(self):
        suite.banner(self.test_cpy_abs) 
        a = self.a  
        
        _;      a(ldy_imm,  0x22)
        _;      a(sty_abs,  0xdddd)
        _;      a(cpy_abs,  0xdddd)
        
        self.run_test()
        self.assertTrue(self.cpu.z)
