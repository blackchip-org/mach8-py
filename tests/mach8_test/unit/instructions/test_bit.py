#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_bit.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution
from mach8 import vm 

class TestBit(execution.TestHarness):
    
    def test_bit_zp_match(self):         
        suite.banner(self.test_bit_zp_match)   
        a = self.a
        
        _;      a(lda_imm,  vm.BIT2 | vm.BIT3)
        _;      a(sta_zp,   0x33)
        _;      a(lda_imm,  vm.BIT2) 
        _;      a(bit_zp,   0x33) 
        
        self.run_test()
        self.assertTrue(not self.cpu.z)
        
    def test_bit_zp_no_match(self):
        suite.banner(self.test_bit_zp_no_match) 
        a = self.a
        
        _;      a(lda_imm,  vm.BIT2 | vm.BIT3)
        _;      a(sta_zp,   0x33)
        _;      a(lda_imm,  vm.BIT1) 
        _;      a(bit_zp,   0x33) 
        
        self.run_test() 
        self.assertTrue(self.cpu.z) 
        
    def test_bit_zp_n(self):
        suite.banner(self.test_bit_zp_n) 
        a = self.a
        
        _;      a(lda_imm,  vm.BIT7) 
        _;      a(sta_zp,   0x33)
        _;      a(lda_imm,  vm.BIT1) 
        _;      a(bit_zp,   0x33)
        
        self.run_test() 
        self.assertTrue(self.cpu.z and self.cpu.n) 
        
    def test_bit_zp_v(self):
        suite.banner(self.test_bit_zp_v) 
        a = self.a
        
        _;      a(lda_imm,  vm.BIT6) 
        _;      a(sta_zp,   0x33)
        _;      a(lda_imm,  0)
        _;      a(bit_zp,   0x33)

        self.run_test()
        self.assertTrue(self.cpu.z and self.cpu.v) 
        
    def test_bit_abs(self):
        suite.banner(self.test_bit_abs)
        a = self.a
        
        _;      a(lda_imm,  vm.BIT2 | vm.BIT3) 
        _;      a(sta_abs,  0x3344)
        _;      a(lda_imm,  vm.BIT2) 
        _;      a(bit_abs,  0x3344)
         
        self.run_test()
        self.assertTrue(not self.cpu.z) 
        
    def test_bit_abx(self):
        suite.banner(self.test_bit_abx)
        a = self.a
        
        _;      a(lda_imm,  vm.BIT2 | vm.BIT3) 
        _;      a(sta_abs,  0x3344)
        _;      a(lda_imm,  vm.BIT2)
        _;      a(ldx_imm,  0x44) 
        _;      a(bit_abx,  0x3300)
         
        self.run_test()
        self.assertTrue(not self.cpu.z) 

    def test_bit_zpx(self):
        suite.banner(self.test_bit_zpx) 
        a = self.a
        
        _;      a(lda_imm,  vm.BIT2 | vm.BIT3) 
        _;      a(sta_zp,   0x44)
        _;      a(lda_imm,  vm.BIT2)
        _;      a(ldx_imm,  0x04) 
        _;      a(bit_zpx,  0x40)
         
        self.run_test()
        self.assertTrue(not self.cpu.z) 
