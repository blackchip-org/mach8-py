#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_program_counter.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
import unittest
from mach8 import memory

class TestProgramCounter(unittest.TestCase):
    
    def setUp(self):
        mem_lo = memory.Block(0x10) 
        mem_hi = memory.Block(0x10) 
        self.mem = memory.Bank()
        self.mem.map(mem_lo, 0x0, 'mem_lo')
        self.mem.map(mem_hi, 0xfff0, 'mem_hi')
        self.pc = memory.ProgramCounter(self.mem)
        
    def test_load(self):
        self.mem[0x00] = 0x34
        self.assertEquals(0x34, self.pc.load()) 
        self.mem[0x01] = 0x12
        self.assertEquals(0x12, self.pc.load()) 
        
    def test_load2(self):
        self.mem[0x00] = 0x34
        self.mem[0x01] = 0x12
        self.assertEquals(0x1234, self.pc.load2()) 
        self.mem[0x02] = 0x78
        self.mem[0x03] = 0x56
        self.assertEquals(0x5678, self.pc.load2()) 
        
    def test_store(self):
        self.pc.store(0x34) 
        self.assertEquals(0x34, self.mem[0x00])
        self.pc.store(0x12)
        self.assertEquals(0x12, self.mem[0x01]) 
        
    def test_store2(self):
        self.pc.store2(0x1234) 
        self.assertEquals(0x34, self.mem[0x00])
        self.assertEquals(0x12, self.mem[0x01])
        self.pc.store2(0x5678) 
        self.assertEquals(0x78, self.mem[0x02])
        self.assertEquals(0x56, self.mem[0x03])
        
    def test_position(self):
        self.pc.position = 0x08
        self.assertEquals(0x08, self.pc.position)
        self.pc.store(0x42) 
        self.assertEquals(0x42, self.mem[0x08])
        
    def test_end_load(self):
        self.mem[0xffff] = 0x12
        self.pc.position = 0xffff
        self.assertEquals(0x12, self.pc.load()) 
        self.assertRaises(OverflowError, self.pc.load) 
        
    def test_increment_first(self):
        self.pc.increment_first = True
        self.mem[0x01] = 0x42
        self.assertEquals(0x42, self.pc.load()) 
        

    
        
    
        