#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_disassembler.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8 import memmap, memory, tools
from mach8.assembly import * 
import unittest
from mach8_test import suite

ORIGIN = memmap.PROGRAM_START 

class TestDisassembler(unittest.TestCase):
    
    def setUp(self):
        self.mem = memory.Block(pages=256)
        self.meta = tools.MetaSource()
        self.a = tools.Assembler(self.mem, origin=ORIGIN, meta=self.meta) 
        self.d = tools.Disassembler(self.mem, origin=ORIGIN, meta=self.meta)
        
    def test_abs(self):        
        suite.banner(self.test_abs)
        self.a(lda_abs, 0x1234)  
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: ad 34 12  lda $1234', str(result).strip()) 
        
    def test_abs_label(self):    
        suite.banner(self.test_abs_label)    
        self.a.label('foo', 0x1234)
        self.a(lda_abs, 'foo') 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: ad 34 12  lda foo', str(result).strip()) 
        
    def test_abs_expression(self):
        suite.banner(self.test_abs_expression) 
        self.a.label('foo', 0x1000)
        self.a(lda_abs, add('foo', x16(0x234)))
        result = self.d.next() 
        suite.log.info(str(result))  
        self.assertEquals('$2000: ad 34 12  lda [foo + $0234]', 
                          str(result).strip())
        
    def test_abx(self):
        suite.banner(self.test_abx)
        self.a(lda_abx, 0x2345) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: bd 45 23  lda $2345,x', str(result).strip()) 
                
    def test_aby(self):
        suite.banner(self.test_aby) 
        self.a(lda_aby, 0x3456)
        result = self.d.next() 
        suite.log.info(str(result))  
        self.assertEquals('$2000: b9 56 34  lda $3456,y', str(result).strip()) 
                
    def test_acc(self):
        suite.banner(self.test_acc)
        self.a(asl_acc) 
        result = self.d.next()
        suite.log.info(str(result))  
        self.assertEquals('$2000: 0a        asl a', str(result).strip()) 

    def test_imp(self):
        suite.banner(self.test_imp) 
        self.a(brk)
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: 00        brk', str(result).strip())
        
    def test_imm(self):
        suite.banner(self.test_imm) 
        self.a(lda_imm, 0x42) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: a9 42     lda #$42', str(result).strip()) 
        
    def test_imm_alias(self):
        suite.banner(self.test_imm_alias)
        self.a.alias('baz', 0x42)
        self.a(lda_imm, 'baz')
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: a9 42     lda #baz', str(result).strip()) 
         
    def test_ind(self):
        suite.banner(self.test_ind) 
        self.a(jmp_ind, 0x4567) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: 6c 67 45  jmp ($4567)', str(result).strip())
                
    def test_izx(self):
        suite.banner(self.test_izx) 
        self.a(lda_izx, 0x42)
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: a1 42     lda ($42,x)', str(result).strip())
        
    def test_izy(self):
        suite.banner(self.test_izy) 
        self.a(lda_izy, 0x42) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: b1 42     lda ($42),y', str(result).strip()) 

    def test_rel(self):
        suite.banner(self.test_rel)
        self.a(bra, 0x2000) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: 80 fe     bra $2000', str(result).strip()) 
        
    def test_rel_label(self):
        suite.banner(self.test_rel_label) 
        a = self.a 
        
        _;  a('branch.back')
        _;      a(nop)
        _;      a(bra,      'branch.back')
        _;      a(bra,      'branch.forward')
        _;      a(nop)
        _;  a('branch.forward')
        
        self.d.next() 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2001: 80 fd     bra branch.back', 
                          str(result).strip())
        result = self.d.next() 
        suite.log.info(str(result))  
        self.assertEquals('$2003: 80 01     bra branch.forward', 
                          str(result).strip()) 
        
    def test_zp(self):
        suite.banner(self.test_zp) 
        self.a(lda_zp, 0x12)
        result = self.d.next()
        suite.log.info(str(result))  
        self.assertEquals('$2000: a5 12     lda $12', str(result).strip()) 
        
    def test_zpx(self):
        suite.banner(self.test_zpx) 
        self.a(lda_zpx, 0x23) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: b5 23     lda $23,x', str(result).strip()) 
                
    def test_zpy(self):
        suite.banner(self.test_zpy) 
        self.a(ldx_zpy, 0x34) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: b6 34     ldx $34,y', str(result).strip()) 
        
    def test_illegal(self):
        suite.banner(self.test_illegal) 
        self.mem[0x2000] = 0x02
        result = self.d.next()
        suite.log.info(str(result)) 
        self.assertEquals('$2000: 02        ?02', str(result).strip()) 
        
    def test_data_branch(self):
        suite.banner(self.test_data_branch)
        self.mem[0x2000] = 0x80
        self.mem[0x2001] = 0xfe 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: 80 fe     bra $2000', str(result).strip())
        
    def test_data(self):
        suite.banner(self.test_data)
        self.a.data('Hello', 42, x8(0x42)) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals("$2000: data      'Hello', 42, $42", 
                          str(result).strip()) 
        
    def test_peek(self):
        suite.banner(self.test_peek) 
        self.a(lda_abs, 0x1234)
        result = self.d.peek() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: ad 34 12  lda $1234', 
                          str(result).strip()) 
        result = self.d.peek() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: ad 34 12  lda $1234', 
                          str(result).strip()) 

    def test_next(self):
        suite.banner(self.test_next) 
        self.a(lda_abs, 0x1234)
        self.a(lda_abs, 0x5678)
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2000: ad 34 12  lda $1234', str(result).strip()) 
        result = self.d.next() 
        suite.log.info(str(result)) 
        self.assertEquals('$2003: ad 78 56  lda $5678', str(result).strip())
        
    def test_disassemble_range(self):
        result = self.d(0x2000, 0x200f)
        result_list = [x for x in result] 
        self.assertEquals(16, len(result_list)) 
        self.assertEquals(0x200f, result_list[-1].address)

    def test_disassemble_one(self):
        result = self.d(0x2000)
        result_list = [x for x in result] 
        self.assertEquals(1, len(result_list)) 
        self.assertEquals(0x2000, result_list[-1].address)
                
    def test_end_range(self):
        self.d.position = 0x2000
        result = self.d.disassemble(end=0x200f)
        result_list = [x for x in result]
        self.assertEquals(16, len(result_list)) 
        self.assertEquals(0x200f, result_list[-1].address)
        
    def test_memory_top(self):
        self.d.position = 0xfff0
        result = self.d.disassemble(end=0xffff)
        result_list = [x for x in result]
        self.assertEquals(0xffff, result_list[-1].address) 
        
    def test_invalid_position(self):
        self.d.position = 0x10000
        self.assertRaises(OverflowError, self.d.next) 

        
