#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_assembler.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
from mach8 import memmap, memory, tools, vm
from mach8.assembly import * 
import unittest

ORIGIN = memmap.PROGRAM_START

class TestAssembler(unittest.TestCase):
    
    def setUp(self):
        self.mem = memory.Block(pages=256)
        self.meta = tools.MetaSource()
        self.a = tools.Assembler(self.mem, origin=ORIGIN, meta=self.meta) 
        
    def test_no_arg(self):
        a = self.a
        
        _;      a(nop) 
        _;      a.data(0xff) 
        
        self.assertEquals(nop.opcode, self.mem[ORIGIN])
        self.assertEquals(0xff, self.mem[ORIGIN + 1])
        
    def test_no_arg_with_arg(self):
        self.assertRaises(TypeError, self.a.assemble, nop, 0x12) 
        
    def test_byte_arg(self):
        a = self.a 
        
        _;      a(lda_imm,  0x12)
        _;      a.data      (0xff)
        
        self.assertEquals(lda_imm.opcode, self.mem[ORIGIN])
        self.assertEquals(0x12, self.mem[ORIGIN + 1])
        
    def test_byte_arg_invalid(self):
        self.assertRaises(OverflowError, self.a.assemble, lda_imm, 0x1234)
        
    def test_byte_arg_no_arg(self):
        self.assertRaises(TypeError, self.a.assemble, lda_imm) 
        
    def test_word_arg(self):
        a = self.a 
                
        _;      a(lda_abs,  0x1234)
        _;      a.data      (0xff)
         
        self.assertEquals(lda_abs.opcode, self.mem[ORIGIN])
        self.assertEquals(0x34, self.mem[ORIGIN + 1])
        self.assertEquals(0x12, self.mem[ORIGIN + 2])
        self.assertEquals(0xff, self.mem[ORIGIN + 3])
        
    def test_word_arg_no_arg(self):
        self.assertRaises(TypeError, self.a.assemble, lda_abs) 
        
    def test_word_arg_invalid_address(self):
        self.assertRaises(OverflowError, self.a.assemble, lda_abs, 0x10000)

    def test_word_arg_negative_address(self):
        self.assertRaises(OverflowError, self.a.assemble, lda_abs, -1) 
    
    def test_too_many_arg(self):
        self.assertRaises(TypeError, self.a.assemble, lda_abs, 1, 2)   
    
    def test_word_arg_label(self):   
        a = self.a    
        a.label('foo', 0x1234)
        
        _;      a(lda_abs,  'foo')
        _;      a.data      (0xff)
         
        self.assertEquals(lda_abs.opcode, self.mem[ORIGIN])
        self.assertEquals(0x34, self.mem[ORIGIN + 1])
        self.assertEquals(0x12, self.mem[ORIGIN + 2])
        self.assertEquals(0xff, self.mem[ORIGIN + 3])
        
    def test_word_arg_function(self):    
        a = self.a     
        a.label('foo', 0x1000)
        
        _;      a(lda_abs,  add('foo', 0x234))
        _;      a.data      (0xff)
         
        self.assertEquals(lda_abs.opcode, self.mem[ORIGIN])
        self.assertEquals(0x34, self.mem[ORIGIN + 1])
        self.assertEquals(0x12, self.mem[ORIGIN + 2])
        self.assertEquals(0xff, self.mem[ORIGIN + 3]) 
        
    def test_label_redefine(self):
        a = self.a
        a.label('test.foo', 0x1234)
        self.assertRaises(tools.SymbolConflictError, a.label, 'test.foo', 
                          0x9999)
        
    def test_label_invalid(self):
        a = self.a 
        self.assertRaises(OverflowError, a.label, 'test.xxx', 0x12345)
        
    def test_label_negative(self):
        a = self.a 
        self.assertRaises(OverflowError, a.label, 'test.yyy', -1)
        
    def test_alias(self):
        a = self.a 
        a.alias('data.jonx', 0x42)
        
        _;      a(lda_imm,  'data.jonx')
        
        self.assertEquals(0x42, self.mem[ORIGIN + 1])

    def test_alias_negative(self):
        a = self.a 
        a.alias('data.neg', -2) 
        
        _;      a(lda_imm,  'data.neg')
        
        self.assertEquals(0xfe, self.mem[ORIGIN + 1])
        
    def test_alias_redefine(self):
        a = self.a 
        a.alias('data.jonx', 0x44)
        self.assertRaises(tools.SymbolConflictError, a.alias, 'data.jonx', 0x99)
        
    def test_alias_invalid(self):
        a = self.a 
        a.alias('data.xxx', 0x100)
        self.assertRaises(OverflowError, a.assemble, lda_imm, 'data.xxx')
        
    def test_alias_invalid_negative(self):
        a = self.a 
        a.alias('data.yyy', -129)
        self.assertRaises(OverflowError, a.assemble, lda_imm, 'data.yyy') 
        
    def test_alias_unresolved(self):
        a = self.a
        
        _;      a(lda_imm,  'illegal')
        
        self.assertRaises(OverflowError, a.alias, 'illegal', 0x12345)
        
    def test_alias_with_alias(self):
        a = self.a 
        a.alias('foo', 0x42) 
        a.alias('bar', 'foo')
        
        _;      a(lda_imm,  'bar')
        
        self.assertEquals(0x42, self.mem[ORIGIN + 1])
        
    def test_data(self):
        a = self.a 
        
        _;      a.data      ('H!', x8(0x12), -1, x16(0x1234))
        
        self.assertEquals(ord('H'), self.mem[ORIGIN])
        self.assertEquals(ord('!'), self.mem[ORIGIN + 1])
        self.assertEquals(0x12,     self.mem[ORIGIN + 2])
        self.assertEquals(0xff,     self.mem[ORIGIN + 3])
        self.assertEquals(0x34,     self.mem[ORIGIN + 4])
        self.assertEquals(0x12,     self.mem[ORIGIN + 5])
        
        self.assertEquals("'H!', $12, -1, $1234", 
                          self.meta.get_data(ORIGIN).text)
        
    def test_data_invalid(self):
        a = self.a 
        self.assertRaises(OverflowError, a.data, 0x10000)

    def test_data_invalid_negative(self):
        a = self.a 
        self.assertRaises(OverflowError, a.data, -129)
        
    def test_verify_unresolved(self):     
        a = self.a 
           
        _;      a(lda_imm, lb('foo')) 
        
        self.assertRaises(tools.SymbolUnresolvedError, a.verify) 
        
    def test_verify_resolved(self):
        a = self.a 
        
        _;      a(lda_imm, lb('foo'))
        _;  a('foo')

        a.verify() 

    def test_resolve_abs(self):
        a = self.a 
        
        _;      a(jmp_abs,  'foo')
        _;      a.data      (0xff) 
        
        a.label('foo', 0x1234) 
        
        self.assertEquals(0x34, self.mem[ORIGIN + 1])
        self.assertEquals(0x12, self.mem[ORIGIN + 2])
        self.assertEquals(0xff, self.mem[ORIGIN + 3])
        
    def test_resolve_rel(self):
        a = self.a 
        
        _;      a(bra,      'foo')
        _;      a.data      (0xff) 
        
        a.label('foo', ORIGIN) 
        
        self.assertEquals(0xfe, self.mem[ORIGIN + 1])
        self.assertEquals(0xff, self.mem[ORIGIN + 2])
        
    def test_resolve_rel_invalid_high(self):
        a = self.a 
        
        _;      a(bra,      'foo')
        
        # Branch to self is -2, so add 3
        self.assertRaises(tools.BranchRangeError, a.label, 'foo', 
                          ORIGIN + vm.SBYTE_MAX + 3) 
        
    def test_resolve_rel_invalid_low(self):
        a = self.a 
        
        _;      a(bra,      'foo')
        
        # Branch to self is -2, so add 1
        self.assertRaises(tools.BranchRangeError, a.label, 'foo', 
                          ORIGIN + vm.SBYTE_MIN + 1)
        
    def test_resolve_zp(self):
        a = self.a 
        
        _;      a(lda_zp,   'foo')
        _;      a.data      (0xff) 
        
        a.label('foo', 0x42) 
        
        self.assertEquals(0x42, self.mem[ORIGIN + 1])
        self.assertEquals(0xff, self.mem[ORIGIN + 2])
        
    def test_resolve_zp_invalid(self):
        a = self.a 
        
        _;      a(lda_zp,   'foo')
        
        self.assertRaises(OverflowError, a.label, 'foo', 0x1234) 
        
    def test_resolve_expr(self):
        a = self.a 
        
        _;      a(lda_zp,   add(1, 'foo'))
        _;      a.data      (0xff) 
        
        a.alias('foo', 0x2) 
        
        self.assertEquals(0x03, self.mem[ORIGIN + 1])
        self.assertEquals(0xff, self.mem[ORIGIN + 2])
        
    def test_resolve_expr_invalid(self):
        a = self.a 
        
        _;      a(lda_zp,   add(1, 'foo'))
        
        self.assertRaises(OverflowError, a.alias, 'foo', 0xff) 
        
    def test_position(self):    
        a = self.a    
        a.position = 0x7777 
        
        _;      a(lda_imm,  0xaa)
        
        self.assertEquals(0xaa, self.mem[0x7778])
        self.assertEquals(0x7779, a.position)
        
    def test_position_label(self):
        a = self.a 
        a.label('test.8888', 0x8888)
        a.position = 'test.8888'
        
        _;      a(lda_imm,  0xbb)
        
        self.assertEquals(0xbb, self.mem[0x8889])
        
    def test_position_invalid(self):
        a = self.a 
        a.position = 0x10000
        self.assertRaises(OverflowError, a.assemble, nop) 
        
    def test_position_invalid_label(self):
        a = self.a 
        self.assertRaises(tools.SymbolUndefinedError, setattr, a,  
                          'position', 'test.9999')
        
    def test_resolved(self):        
        a = self.a
        mem = self.mem
        a.position = 0x4567
        
        _;  a('test.backward')
        _;      a(jmp_abs, 'test.forward')
        
        self.assertEquals(jmp_abs.opcode, mem[0x4567])
        self.assertEquals(0,              mem[0x4568])
        self.assertEquals(0,              mem[0x4569])
        
        a.position = 0x5678
 
        _;  a('test.forward')
        _;      a(jmp_abs, 'test.backward')
        
        a.verify() 
        self.assertEquals(0x78,           mem[0x4568])
        self.assertEquals(0x56,           mem[0x4569])
        
    def test_unresolved(self):        
        a = self.a
        
        _;      a(jmp_abs, 'test.zzyy')
        _;      a(jmp_abs, 'test.aabb')
        
        self.assertRaises(tools.SymbolUnresolvedError, a.verify)
        self.assertEquals(2, len(a.meta.unresolved))
        a.label('test.zzyy', 0x1000)
        self.assertEquals(1, len(a.meta.unresolved))
        a.label('test.aabb', 0x2000)
        self.assertEquals(0, len(a.meta.unresolved)) 
        a.verify()
        
    def test_overwrite(self):
        a = self.a 
        
        _; a('foo')
        _;      a.remark    ('Remark 1')
        _;      a(jmp_abs,  'bar') 
        _; a('bar')
        
        a.position = ORIGIN
        
        _; a('baz')
        _;      a.remark    ('Remark 2')
        _;      a(jmp_abs,  0x1234)
        
        self.assertSetEqual(set(['baz']), self.meta.get_labels(ORIGIN))
        self.assertListEqual(['Remark 2'], self.meta.get_remarks(ORIGIN)) 
        self.assertEquals(0, len(self.meta.get_references(ORIGIN))) 
        self.assertSetEqual(set(['bar']), self.meta.get_labels(ORIGIN + 3))
        
    def test_data_overwrite(self):
        a = self.a 
        
        _;      a.data('Foobar')
        
        self.assertTrue(self.meta.get_data(ORIGIN).valid) 
        a.position = ORIGIN
        
        _;      a(nop) 
        
        self.assertIsNone(self.meta.get_data(ORIGIN)) 
        self.assertFalse(self.meta.get_data(ORIGIN + 1).valid) 

    def test_overwrite_overlap1(self):
        a = self.a 
        
        _;      a(nop) 
        _;  a('foo')
        _;      a(nop) 
        _;  a('bar')
        
        a.position = ORIGIN
        
        _;      a(lda_imm, 0x42)
        
        self.assertEquals(0, len(self.meta.get_labels(ORIGIN + 1))) 
        self.assertSetEqual(set(['bar']), self.meta.get_labels(ORIGIN + 2))
        
    def test_overwrite_overlap2(self):
        a = self.a 
        
        _;      a(nop)
        _;      a(nop)
        _;  a('foo')
        _;      a(nop)
        _;  a('bar')
        
        a.position = ORIGIN
        
        _;      a(jmp_abs,  0x1234)

        self.assertEquals(0, len(self.meta.get_labels(ORIGIN + 2))) 
        self.assertSetEqual(set(['bar']), self.meta.get_labels(ORIGIN + 3))
        
        