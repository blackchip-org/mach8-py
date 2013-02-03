#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_shift.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestShift(execution.TestHarness):
    
    #---------
    # ASL
    #---------
    def test_asl_acc(self):
        suite.banner(self.test_asl_acc)
        a = self.a

        _;      a(lda_imm,  64)
        _;      a(asl_acc)
        
        self.run_test()
        self.assertEquals(128, self.cpu.a)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(    self.cpu.n) 
        self.assertTrue(not self.cpu.c)

    def test_asl_shift_out(self):
        suite.banner(self.test_asl_shift_out) 
        a = self.a 
        
        _;      a(lda_imm,  128)
        _;      a(asl_acc) 
        
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(    self.cpu.z)
        self.assertTrue(not self.cpu.n) 
        self.assertTrue(    self.cpu.c)
        
    def test_asl_zp(self):
        suite.banner(self.test_asl_zp) 
        a = self.a
        
        _;      a(lda_imm,  8)
        _;      a(sta_zp,   0x44)
        _;      a(asl_zp,   0x44)
        _;      a(lda_zp,   0x44)
        
        self.run_test() 
        self.assertEquals(16, self.cpu.a) 

    def test_asl_zpx(self):
        suite.banner(self.test_asl_zpx) 
        a = self.a

        _;      a(lda_imm,  16)
        _;      a(sta_zp,   0x88)
        _;      a(ldx_imm,  0x08)
        _;      a(asl_zpx,  0x80) 
        _;      a(lda_zp,   0x88)
        
        self.run_test() 
        self.assertEquals(32, self.cpu.a) 

    def test_asl_abs(self):
        suite.banner(self.test_asl_abs)
        a = self.a
        
        _;      a(lda_imm,  4) 
        _;      a(sta_abs,  0x6000)
        _;      a(asl_abs,  0x6000)
        _;      a(lda_abs,  0x6000)
        
        self.run_test() 
        self.assertEquals(8, self.cpu.a) 

    def test_asl_abx(self):
        suite.banner(self.test_asl_abx) 
        a = self.a
        
        _;      a(lda_imm,  2) 
        _;      a(sta_abs,  0x6040) 
        _;      a(ldx_imm,  0x40) 
        _;      a(asl_abx,  0x6000)
        _;      a(lda_abs,  0x6040) 
        
        self.run_test() 
        self.assertEquals(4, self.cpu.a) 

    #---------
    # LSR
    #---------
    def test_lsr_acc(self):
        suite.banner(self.test_lsr_acc) 
        a = self.a
        
        _;      a(lda_imm,  64)
        _;      a(lsr_acc)

        self.run_test()
        self.assertEquals(32, self.cpu.a)
        self.assertTrue(not self.cpu.z)
        self.assertTrue(not self.cpu.n) 
        self.assertTrue(not self.cpu.c)

    def test_lsr_shift_out(self):
        suite.banner(self.test_lsr_shift_out) 
        a = self.a
        
        _;      a(lda_imm,  1)
        _;      a(lsr_acc)
         
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(    self.cpu.z)
        self.assertTrue(not self.cpu.n) 
        self.assertTrue(    self.cpu.c)
        
    def test_lsr_zp(self):
        suite.banner(self.test_lsr_zp) 
        a = self.a 

        _;      a(lda_imm,  8)
        _;      a(sta_zp,   0x44)
        _;      a(lsr_zp,   0x44)
        _;      a(lda_zp,   0x44)
        
        self.run_test() 
        self.assertEquals(4, self.cpu.a) 

    def test_lsr_zpx(self):
        suite.banner(self.test_lsr_zpx) 
        a = self.a 

        _;      a(lda_imm,  16)
        _;      a(sta_zp,   0x88)
        _;      a(ldx_imm,  0x08)
        _;      a(lsr_zpx,  0x80) 
        _;      a(lda_zp,   0x88)
        
        self.run_test() 
        self.assertEquals(8, self.cpu.a) 

    def test_lsr_abs(self):
        suite.banner(self.test_lsr_abs) 
        a = self.a 

        _;      a(lda_imm,  4) 
        _;      a(sta_abs,  0x6000)
        _;      a(lsr_abs,  0x6000)
        _;      a(lda_abs,  0x6000)
        
        self.run_test() 
        self.assertEquals(2, self.cpu.a) 

    def test_lsr_abx(self):
        suite.banner(self.test_lsr_abx) 
        a = self.a 
        
        _;      a(lda_imm,  2) 
        _;      a(sta_abs,  0x6040) 
        _;      a(ldx_imm,  0x40) 
        _;      a(lsr_abx,  0x6000)
        _;      a(lda_abs,  0x6040)
         
        self.run_test() 
        self.assertEquals(1, self.cpu.a) 

    #---------
    # ROL
    #---------
    def test_rol_acc(self):
        suite.banner(self.test_ror_acc) 
        a = self.a

        _;      a(lda_imm,  0)
        _;      a(sec)
        _;      a(rol_acc)
        
        self.run_test()
        self.assertEquals(1, self.cpu.a) 
        self.assertTrue(not self.cpu.z and not self.cpu.n and not self.cpu.c) 
        
    def test_rol_through(self):
        suite.banner(self.test_rol_through) 
        a = self.a
        
        _;      a(lda_imm,  0)
        _;      a(sec)
        _;      a(rol_acc)
        _;      a(rol_acc)
        _;      a(rol_acc) 
        _;      a(rol_acc)       
        _;      a(rol_acc)
        _;      a(rol_acc)
        _;      a(rol_acc) 
        _;      a(rol_acc)  
        
        self.run_test() 
        self.assertEquals(128, self.cpu.a) 
        self.assertTrue(not self.cpu.z and self.cpu.n and not self.cpu.c)   
        
    def test_rol_out(self):
        suite.banner(self.test_rol_out)
        a = self.a
        
        _;      a(lda_imm,  128)
        _;      a(rol_acc)
         
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(self.cpu.z and not self.cpu.n and self.cpu.c)

    def test_rol_zp(self):
        suite.banner(self.test_rol_zp) 
        a = self.a
         
        _;      a(clc) 
        _;      a(lda_imm,  8) 
        _;      a(sta_zp,   0x44) 
        _;      a(rol_zp,   0x44)
        _;      a(lda_zp,   0x44)
        
        self.run_test() 
        self.assertEquals(16, self.cpu.a)
        
    def test_rol_zpx(self): 
        suite.banner(self.test_rol_zpx) 
        a = self.a 

        _;      a(lda_imm,  16) 
        _;      a(sta_zp,   0x88) 
        _;      a(ldx_imm,  0x08) 
        _;      a(rol_zpx,  0x80) 
        _;      a(ldy_zp,   0x88)
         
        self.run_test() 
        self.assertEquals(32, self.cpu.y) 
        
    def test_rol_abs(self):
        suite.banner(self.test_rol_abs)
        a = self.a

        _;      a(lda_imm,  4) 
        _;      a(sta_abs,  0x6000)
        _;      a(rol_abs,  0x6000)
        _;      a(ldx_abs,  0x6000)
        
        self.run_test() 
        self.assertEquals(8, self.cpu.x)
        
    def test_rol_abx(self):
        suite.banner(self.test_rol_abx) 
        a = self.a
        
        _;      a(lda_imm,  2) 
        _;      a(sta_abs,  0x6040) 
        _;      a(ldx_imm,  0x40) 
        _;      a(rol_abx,  0x6000)
        _;      a(ldy_abs,  0x6040)
         
        self.run_test() 
        self.assertEquals(4, self.cpu.y)

    #---------
    # ROR
    #---------
    def test_ror_acc(self):
        suite.banner(self.test_ror_acc) 
        a = self.a

        _;      a(lda_imm,  0) 
        _;      a(sec) 
        _;      a(ror_acc)
        
        self.run_test()
        self.assertEquals(128, self.cpu.a) 
        self.assertTrue(not self.cpu.z and self.cpu.n and not self.cpu.c) 
        
    def test_ror_through(self):
        suite.banner(self.test_ror_through) 
        a = self.a
        
        _;      a(sec) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        _;      a(ror_acc) 
        
        self.run_test() 
        self.assertEquals(1, self.cpu.a) 
        self.assertTrue(not self.cpu.z and not self.cpu.n and not self.cpu.c) 
                
    def test_ror_out(self):
        suite.banner(self.test_ror_out) 
        a = self.a

        _;      a(lda_imm,  1) 
        _;      a(ror_acc) 
        
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        self.assertTrue(self.cpu.z and not self.cpu.n and self.cpu.c)
        
    def test_ror_zp(self):
        suite.banner(self.test_ror_zp) 
        a = self.a

        _;      a(lda_imm,  8) 
        _;      a(sta_zp,   0x44)
        _;      a(ror_zp,   0x44)
        _;      a(ldx_zp,   0x44) 
        
        self.run_test() 
        self.assertEquals(4, self.cpu.x) 
        
    def test_ror_zpx(self):
        suite.banner(self.test_ror_zpx) 
        a = self.a

        _;      a(lda_imm,  16) 
        _;      a(sta_zp,   0x88) 
        _;      a(ldx_imm,  0x08) 
        _;      a(ror_zpx,  0x80) 
        _;      a(ldy_zp,   0x88)
         
        self.run_test() 
        self.assertEquals(8, self.cpu.y) 
        
    def test_ror_abs(self):
        suite.banner(self.test_ror_abs) 
        a = self.a
        
        _;      a(lda_imm,  4) 
        _;      a(sta_abs,  0x6000)
        _;      a(ror_abs,  0x6000)
        _;      a(ldx_abs,  0x6000)
        
        self.run_test() 
        self.assertEquals(2, self.cpu.x) 
        
    def test_ror_abx(self):
        suite.banner(self.test_ror_abx) 
        a = self.a

        _;      a(lda_imm,  2) 
        _;      a(sta_abs,  0x6040) 
        _;      a(ldx_imm,  0x40) 
        _;      a(ror_abx,  0x6000)
        _;      a(ldy_abs,  0x6040)
        
        self.run_test() 
        self.assertEquals(1, self.cpu.y) 

