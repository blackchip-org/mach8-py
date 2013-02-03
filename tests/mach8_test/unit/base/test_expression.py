#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_expression.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
from mach8.expressions import * 
from mach8 import tools
import unittest

class TestExpression(unittest.TestCase):

    def setUp(self):
        self.meta = tools.MetaSource() 
        
    def test_add(self):
        e = add(2, 4) 
        self.assertEquals(6, e.eval()) 
        self.assertEquals('[2 + 4]', str(e)) 
        
    def test_and(self):
        e = and_(x8(0xff), x8(0x0f))
        self.assertEquals(0x0f, e.eval()) 
        self.assertEquals('[$ff & $0f]', str(e)) 
        
    def test_asc(self):
        e = asc('A') 
        self.assertEquals(ord('A'), e.eval()) 
        self.assertEquals("'A'", str(e)) 
        
    def test_b8(self):
        e = b8(0xaa)
        self.assertEquals(0xaa, e.eval()) 
        self.assertEquals('b10101010', str(e)) 
        
    def test_byte0(self):
        e = byte0(x32(0x12345678)) 
        self.assertEquals(0x78, e.eval()) 
        self.assertEquals('$12345678<0>', str(e))

    def test_byte1(self):
        e = byte1(x32(0x12345678)) 
        self.assertEquals(0x56, e.eval()) 
        self.assertEquals('$12345678<1>', str(e))
        
    def test_byte2(self):
        e = byte2(x32(0x12345678)) 
        self.assertEquals(0x34, e.eval()) 
        self.assertEquals('$12345678<2>', str(e))
        
    def test_byte3(self):
        e = byte3(x32(0x12345678)) 
        self.assertEquals(0x12, e.eval()) 
        self.assertEquals('$12345678<3>', str(e))
                
    def test_eor(self):
        e = eor(x8(0xf0), x8(0xff)) 
        self.assertEquals(0x0f, e.eval()) 
        self.assertEquals('[$f0 ^ $ff]', str(e)) 
        
    def test_hb(self):
        e = hb(x16(0x1234)) 
        self.assertEquals(0x12, e.eval()) 
        self.assertEquals('>$1234', str(e)) 
        
    def test_lb(self):
        e = lb(x16(0x1234))
        self.assertEquals(0x34, e.eval()) 
        self.assertEquals('<$1234', str(e)) 

    def test_or(self):
        e = or_(x8(0xf0), x8(0x0f)) 
        self.assertEquals(0xff, e.eval()) 
        self.assertEquals('[$f0 | $0f]', str(e)) 
        
    def test_sub(self):
        e = sub(6, 4) 
        self.assertEquals(2, e.eval()) 
        self.assertEquals('[6 - 4]', str(e)) 
        
    def test_x8(self):
        e = x8(0x7f)
        self.assertEquals(0x7f, e.eval()) 
        self.assertEquals('$7f', str(e)) 
          
    def test_x16(self):
        e = x16(0x0a7f)
        self.assertEquals(0xa7f, e.eval()) 
        self.assertEquals('$0a7f', str(e)) 

    def test_x32(self):
        e = x32(0x0a7f1234)
        self.assertEquals(0x0a7f1234, e.eval()) 
        self.assertEquals('$0a7f1234', str(e)) 
                
    def test_add_symbol(self):
        self.meta.define_alias('two', 2) 
        self.meta.define_alias('four', 4) 
        e = add('two', 'four') 
        self.assertEquals(6, e.eval(self.meta)) 
        self.assertEquals('[two + four]', str(e)) 
        
    def test_add_sub_complex(self):
        self.meta.define_alias('eight', 8)
        self.meta.define_alias('one', 1) 
        e = add(6, 4, sub('eight', 2), add('one', sub(5, 2)))
        self.assertEquals(20, e.eval(self.meta)) 
        self.assertEquals('[6 + 4 + [eight - 2] + [one + [5 - 2]]]', str(e)) 
        
        
        