#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_memory.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestMemory(execution.TestHarness):
    
    def test_malloc(self):
        suite.banner(self.test_malloc) 
        a = self.a 
        
        _;      a.macro    (ldxy_imm, 0x8000)
        _;      a.macro    (stxy_zp,  'HEAP_PTR')
        _;      a(lda_imm, 0x04) 
        _;      a(jsr,     'MALLOC')
        _;      a.macro    (ldxy_zp,  'HEAP_PTR')
        
        self.run_test() 
        self.assertEquals(0xfc, self.cpu.x) 
        self.assertEquals(0x7f, self.cpu.y)

    def test_bzero(self):
        suite.banner(self.test_bzero)
        a = self.a 
        
        self.mem[0x8000:0x8008:2] = (0xdead, 0xbeef, 0xdead, 0xbeef) 
        
        _;      a.macro     (ldxy_imm, 0x1234)
        _;      a.macro     (stxy_abs, add(x16(0x8000), 2)) 
        _;      a.macro     (ldxy_imm, 0x5678)
        _;      a.macro     (stxy_abs, add(x16(0x8000), 4)) 
        
        _;      a.macro     (ldxy_imm, add(x16(0x8000), 2)) 
        _;      a(lda_imm,  4) 
        _;      a(jsr,      'BZERO')
        
        self.run_test() 
        words = self.mem[0x8000:0x8008:2]
        self.assertEquals([0xdead, 0, 0, 0xbeef], words) 
        
    def test_memcpy(self):
        suite.banner(self.test_memcpy) 
        a = self.a 
        
        self.mem[0x8000 + 6::2] = 0xbeef
        
        _;      a.macro     (ldxy_imm, 'test.str')
        _;      a.macro     (stxy_zp,  'R1')
        _;      a.macro     (ldxy_imm, x16(0x8000)) 
        _;      a.macro     (stxy_zp,  'R3')
        _;      a(lda_imm,  6)
        _;      a(jsr,      'MEMCPY')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.str')
        _;      a.data      ('123456', x16(0xdead))
        
        self.run_test() 
        
        value = ''.join(map(chr, self.mem[0x8000:0x8006]))
        self.assertEquals('123456', value)
        self.assertEquals(0xbeef, self.mem[0x8000 + 6::2])
        