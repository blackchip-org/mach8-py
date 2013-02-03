#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_io.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite, mock
from mach8_test.harness import execution
from mach8 import aliases, memmap, vm 

class TestIO(execution.TestHarness):

    def test_chrout(self):
        suite.banner(self.test_chrout) 
        a = self.a 
        
        _;      a(lda_imm, asc('0'))
        _;      a(jsr,     'CHROUT') 
        
        self.run_test() 
        self.assertEquals('0', self.output.getvalue()) 
        
    def test_chrin(self):
        suite.banner(self.test_chrin) 
        a = self.a
        
        termin = mock.TerminalInput('123456\x00')
        self.comp.terminal_input.source = termin
        
        _;      a(ldx_imm,  0) 
        _;  a('test.loop')
        _;      a(jsr,      'CHRIN')
        _;      a(cmp_imm,  0x00)
        _;      a(beq,      'test.done')
        _;      a(sta_abx,  0x5000) 
        _;      a(inx)
        _;      a(bra,      'test.loop')
        _;  a('test.done')
        
        self.run_test()
        chars = [chr(self.mem[0x5000 + i]) for i in xrange(6)]
        self.assertEquals('123456', ''.join(chars)) 
        
    def test_strout(self):
        suite.banner(self.test_strout) 
        a = self.a        

        _;      a.macro     (ldxy_imm, 'test.str')
        _;      a(jsr,      'STROUT')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.str') 
        _;      a.data      ('123456', 0)
        
        self.run_test() 
        self.assertEquals('123456', self.output.getvalue()) 
        
    def test_strout_zero(self):
        suite.banner(self.test_strout_zero) 
        a = self.a        

        _;      a.macro     (ldxy_imm, 'test.str')
        _;      a(jsr,      'STROUT')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.str') 
        _;      a.data      (0)
        
        self.run_test() 
        self.assertEquals('', self.output.getvalue())
        
    def test_linein(self):
        suite.banner(self.test_linein)
        a = self.a                 
        termin = mock.TerminalInput('12345\n')
        self.comp.terminal_input.source = termin
        buf = memmap.TERM_INPUT_BUFFER
        
        self.mem[buf:buf+8:2] = (0xdead, 0xbeef, 0xdead, 0xbeef)
                
        _;      a(jsr,      'LINEIN')

        self.run_test() 
        value = ''.join(map(chr, self.mem[buf:buf+6]))
        self.assertEquals('12345\x00', value)  
        self.assertEquals(buf, vm.word(self.cpu.x, self.cpu.y))

    def test_linein_empty(self):
        suite.banner(self.test_linein_empty)        
        a = self.a
        termin = mock.TerminalInput('\n')
        self.comp.terminal_input.source = termin
        buf = memmap.TERM_INPUT_BUFFER

        self.mem[buf:buf+8:2] = (0xdead, 0xbeef, 0xdead, 0xbeef)
                
        _;      a(jsr,      'LINEIN')

        self.run_test() 
        self.assertEquals(0, self.mem[memmap.TERM_INPUT_BUFFER])
        self.assertEquals(buf, vm.word(self.cpu.x, self.cpu.y))
                        
    def test_linein_long(self):
        suite.banner(self.test_linein_long) 
        a = self.a
        
        termin = mock.TerminalInput('*' * 256) 
        self.comp.terminal_input.source = termin
        self.cpu.cycle_limit = 10000
        
        _;      a.macro     (ldxy_imm, 'test.abort')
        _;      a.macro     (stxy_abs, 'YAP_ABORT_VECTOR')
        _;      a(jsr,      'LINEIN')
        _;      a(lda_zp,   'ERRNO')
        _;      a(brk)
        _;      a(nop)
        
        _;  a('test.abort')
        _;      a(rts) 
        
        self.run_test()
        self.assertEquals(aliases.ERR_STRING_TOO_LONG, self.cpu.a) 
        
    def test_primm(self):
        suite.banner(self.test_primm) 
        a = self.a
        
        _;      a(jsr,      'PRIMM')
        _;      a.data      ('123456', 0) 
        _;      a(lda_imm,  0xff)
         
        self.run_test() 
        self.assertEquals('123456', self.output.getvalue()) 
        self.assertEquals(0xff, self.cpu.a) 
            
    def test_primm_zero(self):
        suite.banner(self.test_primm_zero) 
        a = self.a
        
        _;      a(jsr,      'PRIMM')
        _;      a.data      (0) 
        _;      a(lda_imm,  0xff)
         
        self.run_test() 
        self.assertEquals('', self.output.getvalue()) 
        self.assertEquals(0xff, self.cpu.a) 
         
    
        
        
