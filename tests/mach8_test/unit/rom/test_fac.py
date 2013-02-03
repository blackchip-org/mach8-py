#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_fac.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution
from mach8 import aliases, memmap, vm 

f0_start = aliases.FAC0 
f0_end = f0_start + aliases.SIZEOF_FAC

f1_start = aliases.FAC1 
f1_end = f1_start + aliases.SIZEOF_FAC  

fm_start = 0x8000
fm_end = 0x8000 + aliases.SIZEOF_FAC

class TestAdmin(execution.TestHarness):
    
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
        _;      a(jsr,      'ZFAC0')
        
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
        _;      a(jsr,      'ZFAC1')
        
        self.run_test() 
        self.assertEquals(0, self.mem[memmap.FAC1_SIGN])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA + 1])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA + 2])
        self.assertEquals(0, self.mem[memmap.FAC1_MANTISSA + 3])
        self.assertEquals(0, self.mem[memmap.FAC1_EXPONENT])
        
    def test_mem2fac0(self):
        suite.banner(self.test_mem2fac0)
        a = self.a

        self.mem[aliases.FAC0 + 6::2] = 0xbeef
                
        _;      a.macro     (fac, -1.234567e-89, 0x8000)
        _;      a.macro     (ldxy_imm, 0x8000)
        _;      a(jsr,      'MEM2FAC0')

        self.run_test() 
        self.assertEquals(-1.234567e-89, vm.fac2py(self.mem[f0_start:f0_end]))
        self.assertEquals(0xbeef, self.mem[aliases.FAC0 + 6::2])
        
    def test_mem2fac1(self):
        suite.banner(self.test_mem2fac1)
        a = self.a

        # No overrun test -- FAC_PTR is there
                
        _;      a.macro     (fac, -1.234567e-89, 0x8000)
        _;      a.macro     (ldxy_imm, 0x8000)
        _;      a(jsr,      'MEM2FAC1')

        self.run_test() 
        self.assertEquals(-1.234567e-89, vm.fac2py(self.mem[f1_start:f1_end]))
        
    def test_fac2mem0(self):
        suite.banner(self.test_fac2mem0) 
        a = self.a
        
        self.mem[0x8006::2] = 0xbeef
        
        _;      a.macro     (fac0, -1.234567e-89)
        _;      a.macro     (ldxy_imm, fm_start) 
        _;      a(jsr,      'FAC2MEM0')

        self.run_test() 
        self.assertEquals(-1.234567e-89, vm.fac2py(self.mem[fm_start:fm_end]))
        self.assertEquals(0xbeef, self.mem[0x8006::2])
        
    def test_fac2mem1(self):
        suite.banner(self.test_fac2mem1) 
        a = self.a
        
        self.mem[0x8006::2] = 0xbeef
        
        _;      a.macro     (fac1, -1.234567e-89)
        _;      a.macro     (ldxy_imm, fm_start) 
        _;      a(jsr,      'FAC2MEM1')

        self.run_test() 
        self.assertEquals(-1.234567e-89, vm.fac2py(self.mem[fm_start:fm_end]))
        self.assertEquals(0xbeef, self.mem[0x8006::2])
        
    def test_facop(self):
        suite.banner(self.test_facop) 
        a = self.a 
        
        _;      a.macro     (fac0, 8) 
        _;      a.macro     (fac1, 7) 
        _;      a(lda_imm,  'FPU_ADD')
        _;      a(jsr,      'FACOP')
        _;      a(lda_zp,   'FPU_STATUS')
        
        self.run_test() 
        self.assertEquals(15, vm.fac2py(self.mem[f0_start:f0_end])) 
        self.assertEquals(0, self.cpu.a)
        
    def test_facop_invalid(self):
        suite.banner(self.test_facop_invalid) 
        a = self.a
        
        _;      a.macro     (ldxy_imm, 'test.abort')
        _;      a.macro     (stxy_abs, 'YAP_ABORT_VECTOR')
        _;      a.macro     (fac0, 8) 
        _;      a.macro     (fac1, 0) 
        _;      a(lda_imm,  'FPU_DIV')
        _;      a(jsr,      'FACOP')
        _;      a(lda_zp,   'ERRNO')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.abort')
        _;      a(rts) 
        
        self.run_test()         
        self.assertEquals(aliases.ERR_FPU_DIVISION_BY_ZERO, self.cpu.a) 
        # Make sure this got cleared out
        self.assertEquals(0, self.mem[memmap.FPU_STATUS])
        
        