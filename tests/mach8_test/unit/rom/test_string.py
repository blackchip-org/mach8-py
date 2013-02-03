#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_string.py 130 2012-01-28 02:16:54Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8 import memmap
from mach8_test import suite
from mach8_test.harness import execution
from mach8 import vm 

class TestString(execution.TestHarness):
    
    def test_strlen(self):
        suite.banner(self.test_strlen)
        a = self.a
                
        _;      a.macro     (ldxy_imm, 'test.message')     
        _;      a(jsr,      'STRLEN')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.message')
        _;      a.data      ('12345678', 0) 
        
        self.run_test() 
        self.assertEquals(8, self.cpu.a) 
           
    def test_strlen_zero(self):
        suite.banner(self.test_strlen_zero)
        a = self.a
                
        _;      a.macro     (ldxy_imm, 'test.message') 
        _;      a(jsr,      'STRLEN')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.message')
        _;      a.data      (0) 
        
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        
    def test_strcpy(self):
        suite.banner(self.test_strcpy) 
        a = self.a 
                
        self.mem[0x8007::2] = 0xdead
        
        _;      a(ldx_imm, lb('test.answer'))
        _;      a(ldy_imm, hb('test.answer')) 
        _;      a.macro    (stxy_zp,  'R1')
        _;      a.macro    (ldxy_imm, 0x8000)
        _;      a.macro    (stxy_zp,  'R3')
        _;      a(jsr,     'STRCPY')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.answer')
        _;      a.data     ('123456', 0, 0xbeef)
        
        self.run_test() 
        value = ''.join(map(chr, self.mem[0x8000:0x8006]))
        self.assertEquals('123456', value) 
        self.assertEquals(0xdead, self.mem[0x8007::2])
        
    def test_strcmp_equals(self):
        suite.banner(self.test_strcmp_equals)
        a = self.a
        
        _;      a.macro    (ldxy_imm, 'test.str1')
        _;      a.macro    (stxy_zp,  'R1')
        _;      a.macro    (ldxy_imm, 'test.str2')
        _;      a.macro    (stxy_zp,  'R3')
        _;      a(jsr,     'STRCMP')
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.str1')
        _;      a.data     ('12345', 0)
        _;  a('test.str2')
        _;      a.data     ('12345', 0)
        
        self.run_test() 
        self.assertEquals(0, self.cpu.a) 
        
    def test_strcmp_not_equals(self):
        suite.banner(self.test_strcmp_not_equals)
        a = self.a
        
        _;      a.macro    (ldxy_imm, 'test.str1')
        _;      a.macro    (stxy_zp,  'R1')
        _;      a.macro    (ldxy_imm, 'test.str2')
        _;      a.macro    (stxy_zp,  'R3')
        _;      a(jsr,     'STRCMP')
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.str1')
        _;      a.data     ('1234*', 0)
        _;  a('test.str2')
        _;      a.data     ('12345', 0)
        
        self.run_test() 
        self.assertEquals(1, self.cpu.a) 
        
    def test_strcmp_not_equals_short_1(self):
        suite.banner(self.test_strcmp_not_equals_short_1)
        a = self.a 
        
        _;      a.macro    (ldxy_imm, 'test.str1')
        _;      a.macro    (stxy_zp,  'R1')
        _;      a.macro    (ldxy_imm, 'test.str2')
        _;      a.macro    (stxy_zp,  'R3')
        _;      a(jsr,     'STRCMP')
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.str1')
        _;      a.data     ('1234', 0)
        _;  a('test.str2')
        _;      a.data     ('12345', 0)
        
        self.run_test() 
        self.assertEquals(1, self.cpu.a) 
        
    def test_strcmp_not_equals_short_2(self):
        suite.banner(self.test_strcmp_not_equals_short_2) 
        a = self.a 
        
        _;      a.macro    (ldxy_imm, 'test.str1')
        _;      a.macro    (stxy_zp,  'R1')
        _;      a.macro    (ldxy_imm, 'test.str2')
        _;      a.macro    (stxy_zp,  'R3')
        _;      a(jsr,     'STRCMP')
        _;      a(brk)
        _;      a(nop) 
        
        _;  a('test.str1')
        _;      a.data     ('12345', 0)
        _;  a('test.str2')
        _;      a.data     ('1234', 0)
        
        self.run_test() 
        self.assertEquals(1, self.cpu.a) 
        
    def test_strcat(self):
        suite.banner(self.test_strcat)
        a = self.a
        
        self.mem[memmap.HEAP - 1::2] = 0xdead
        self.mem[memmap.HEAP + 1::2] = 0xbeef 
        
        _;      a.macro   (ldxy_imm, 'test.str1')
        _;      a.macro   (stxy_zp,  'R1')
        _;      a.macro   (ldxy_imm, 'test.str2')
        _;      a.macro   (stxy_zp,  'R3')
        _;      a(jsr,    'STRCAT')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.str1')
        _;      a.data('123', 0) 
        _;  a('test.str2')
        _;      a.data('4567', 0)  
        
        self.run_test() 
        ptr = self.mem[memmap.R1::2]
        value = ''.join(map(chr, self.mem[ptr:ptr + 8])) 
        self.assertEquals('1234567\x00', value) 
        self.assertEquals(0xbeef, self.mem[memmap.HEAP + 1::2])

    def test_findmsg_first(self):
        suite.banner(self.test_findmsg_first)
        a = self.a        
        
        _;      a.macro     (ldxy_imm, 'test.table')
        _;      a(lda_imm,  0)
        _;      a(jsr,      'FINDMSG')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.table')
        _;  a('answer')
        _;      a.data      ('123456', 0)
        _;      a.data      ('000000', 0)
        _;      a.data      ('000000', 0)
                
        self.run_test() 
        ptr = self.meta.lookup('answer')
        self.assertEquals(vm.lb(ptr), self.cpu.x) 
        self.assertEquals(vm.hb(ptr), self.cpu.y) 
        
    def test_findmsg_second(self):
        suite.banner(self.test_findmsg_second) 
        a = self.a
        
        _;      a.macro     (ldxy_imm, 'test.table')
        _;      a(lda_imm,  1)
        _;      a(jsr,      'FINDMSG')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.table')
        _;      a.data      ('000000', 0)
        _;  a('answer')
        _;      a.data      ('123456', 0)
        _;      a.data      ('000000', 0)
                
        self.run_test() 
        ptr = self.meta.lookup('answer')
        self.assertEquals(vm.lb(ptr), self.cpu.x) 
        self.assertEquals(vm.hb(ptr), self.cpu.y) 
        
    def test_findmsg_last(self):
        suite.banner(self.test_findmsg_last) 
        a = self.a        
        
        _;      a.macro     (ldxy_imm, 'test.table')
        _;      a(lda_imm,  2)
        _;      a(jsr,      'FINDMSG')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.table')
        _;      a.data      ('000000', 0)
        _;      a.data      ('000000', 0)
        _;  a('answer')
        _;      a.data      ('123456', 0)
        
        self.run_test() 
        ptr = self.meta.lookup('answer')
        self.assertEquals(vm.lb(ptr), self.cpu.x) 
        self.assertEquals(vm.hb(ptr), self.cpu.y) 
        
    def test_bcd2chr_lo(self):
        suite.banner(self.test_bcd2chr_lo)
        a = self.a
        
        _;      a(lda_imm,  0x45) 
        _;      a(jsr,      'BCD2CHR_LO')
        
        self.run_test() 
        self.assertEquals(ord('5'), self.cpu.a) 
        
    def test_bcd2chr_hi(self):
        suite.banner(self.test_bcd2chr_hi)
        a = self.a
        
        _;      a(lda_imm,  0x45) 
        _;      a(jsr,      'BCD2CHR_HI')
        
        self.run_test() 
        self.assertEquals(ord('4'), self.cpu.a) 
        
        