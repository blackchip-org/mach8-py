#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_macros.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8 import aliases, memmap, vm
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestMacros(execution.TestHarness):
    
    def test_fac0(self):
        suite.banner(self.test_fac0) 
        a = self.a 
        
        _;      a.macro     (fac0, -1.2345678e23)
        
        self.run_test() 
        self.assertEquals(aliases.SIGN_MANTISSA, self.mem[memmap.FAC0_SIGN])
        
        
    def test_inc_word_zp(self):
        suite.banner(self.test_inc_word_zp)
        a = self.a 
        
        _;      a(lda_imm,  0xff)
        _;      a(sta_zp,   'R1')
        _;      a(lda_imm,  0x7f)
        _;      a(sta_zp,   'R2')
        
        _;      a.macro     (inc_zp_word, 'R1')
        _;      a(ldx_zp,   'R1')
        _;      a(ldy_zp,   'R2')
        
        self.run_test() 
        self.assertEquals(0x8000, vm.word(self.cpu.x, self.cpu.y)) 
        
    def test_inxy(self):
        suite.banner(self.test_inxy)
        a = self.a 
        
        _;      a(ldx_imm,  0xfe) 
        _;      a(ldy_imm,  0x01) 
        _;      a.macro     (inxy) 
        
        self.run_test() 
        self.assertEquals(0xff, self.cpu.x) 
        self.assertEquals(0x01, self.cpu.y) 

    def test_inxy_carry(self):
        suite.banner(self.test_inxy_carry)
        a = self.a 
        
        _;      a(ldx_imm,  0xff) 
        _;      a(ldy_imm,  0x01) 
        _;      a.macro     (inxy) 
        
        self.run_test() 
        self.assertEquals(0x00, self.cpu.x) 
        self.assertEquals(0x02, self.cpu.y) 
           
    def test_ldxy_abs(self):
        suite.banner(self.test_ldxy_zp) 
        a = self.a 
        
        _;      a(lda_imm,  0x34) 
        _;      a(sta_abs,  0x5000)
        _;      a(lda_imm,  0x12)
        _;      a(sta_abs,  0x5001) 
        _;      a.macro     (ldxy_abs, x16(0x5000)) 
        
        self.run_test() 
        self.assertEquals(0x34, self.cpu.x) 
        self.assertEquals(0x12, self.cpu.y)
             
    def test_ldxy_imm(self):
        suite.banner(self.test_ldxy_imm) 
        a = self.a 
        
        _;      a.macro     (ldxy_imm, x16(0x1234)) 
        
        self.run_test() 
        self.assertEquals(0x34, self.cpu.x) 
        self.assertEquals(0x12, self.cpu.y)
    
    def test_ldxy_zp(self):
        suite.banner(self.test_ldxy_zp) 
        a = self.a 
        
        _;      a(lda_imm,  0x34) 
        _;      a(sta_zp,   0xfe)
        _;      a(lda_imm,  0x12)
        _;      a(sta_zp,   0xff) 
        _;      a.macro     (ldxy_zp, x8(0xfe)) 
        
        self.run_test() 
        self.assertEquals(0x34, self.cpu.x) 
        self.assertEquals(0x12, self.cpu.y)
        
    def test_lsr_nibble(self):
        suite.banner(self.test_lsr_nibble) 
        a = self.a 
        
        _;      a(lda_imm,  x8(0xf0))
        _;      a.macro     (lsr_nibble) 
        
        self.run_test()
        self.assertEquals(0x0f, self.cpu.a)
        
    def test_primm(self):
        suite.banner(self.test_primm) 
        a = self.a 
        
        _;      a.macro     (primm, '!' * 254) 
        
        self.run_test() 
        self.assertEquals(254, len(self.output.getvalue())) 

    def test_primm_1(self):
        suite.banner(self.test_primm_1) 
        a = self.a 
        
        _;      a.macro     (primm, '!' * 300) 
        
        self.run_test()
        self.assertEquals(300, len(self.output.getvalue())) 
        
        
    def test_stxy_zp(self):
        suite.banner(self.test_stxy_zp) 
        a = self.a 
        
        _;      a(ldx_imm,  0x34) 
        _;      a(ldy_imm,  0x12) 
        _;      a.macro     (stxy_zp, x8(0x01)) 
        
        self.run_test() 
        self.assertEquals(0x34, self.mem[0x01])
        self.assertEquals(0x12, self.mem[0x02])
        
    def test_stxy_abs(self):
        suite.banner(self.test_stxy_abs) 
        a = self.a 
        
        _;      a(ldx_imm,  0x34) 
        _;      a(ldy_imm,  0x12) 
        _;      a.macro     (stxy_abs, x8(0x5000)) 
        
        self.run_test() 
        self.assertEquals(0x34, self.mem[0x5000])
        self.assertEquals(0x12, self.mem[0x5001])

    def test_zfac0(self):
        suite.banner(self.test_zfac0) 
        a = self.a 
        
        _;      a(lda_imm,  0xff) 
        _;      a(sta_zp,   'FAC0_SIGN')
        _;      a(sta_zp,   'FAC0_MANTISSA')
        _;      a(sta_zp,   add('FAC0_MANTISSA', 1))
        _;      a(sta_zp,   add('FAC0_MANTISSA', 2))
        _;      a(sta_zp,   add('FAC0_MANTISSA', 3))
        _;      a(sta_zp,   add('FAC0_MANTISSA', 4))
        _;      a(sta_zp,   'FAC0_EXPONENT')
        _;      a.macro     (zfac0) 
        
        self.run_test() 
        self.assertEquals(0, self.mem[memmap.FAC0_SIGN])
        self.assertEquals(0, self.mem[memmap.FAC0_MANTISSA])
        self.assertEquals(0, self.mem[memmap.FAC0_MANTISSA + 1])
        self.assertEquals(0, self.mem[memmap.FAC0_MANTISSA + 2])
        self.assertEquals(0, self.mem[memmap.FAC0_MANTISSA + 3])
        self.assertEquals(0, self.mem[memmap.FAC0_EXPONENT])
        
    def test_zfac1(self):
        suite.banner(self.test_zfac1) 
        a = self.a 
        
        _;      a(lda_imm,  0xff) 
        _;      a(sta_zp,   'FAC1_SIGN')
        _;      a(sta_zp,   'FAC1_MANTISSA')
        _;      a(sta_zp,   add('FAC1_MANTISSA', 1))
        _;      a(sta_zp,   add('FAC1_MANTISSA', 2))
        _;      a(sta_zp,   add('FAC1_MANTISSA', 3))
        _;      a(sta_zp,   add('FAC1_MANTISSA', 4))
        _;      a(sta_zp,   'FAC1_EXPONENT')
        _;      a.macro     (zfac1) 
        
        self.run_test() 
        self.assertEquals(0, self.mem[memmap.FAC1_SIGN])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA + 1])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA + 2])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA + 3])
        self.assertEquals(0, self.mem[memmap.FAC1_EXPONENT])
        
