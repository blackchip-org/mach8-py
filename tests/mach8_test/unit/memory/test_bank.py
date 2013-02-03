#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_bank.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
import unittest
from mach8 import memory, vm 
import warnings 

class TestMemoryBank(unittest.TestCase):
    
    def setUp(self):
        self.bank = memory.Bank()
        self.block0 = memory.Block(pages=1) 
        self.block1 = memory.Block(pages=1) 
        
        self.bank.map(self.block0, 0x0000, 'block0')
        self.bank.map(self.block1, 0x0100, 'block1') 
        
    def test_store_block0(self):
        self.bank[0xff] = 0xaa
        self.assertEquals(0xaa, self.block0[0xff])

    def test_store_block1(self):
        self.bank[0x100] = 0xbb
        self.assertEquals(0xbb, self.block1[0x00])  

    def test_load_block0(self):
        self.block0[0xff] = 0xaa
        self.assertEquals(0xaa, self.bank[0xff])
        
    def test_load_block1(self):
        self.block1[0x00] = 0xbb
        self.assertEquals(0xbb, self.bank[0x100])
        
    def test_invalid_address(self):
        self.assertRaises(memory.AddressBusError, self.bank.__getitem__, 0x200)
            
    def test_duplicate_block(self):
        self.assertRaises(ValueError, self.bank.map, self.block0, 0x00, 
                          'block0')
        
    def test_clear_all(self):
        self.bank[0xff::2] = 0x1234
        self.bank.clear()
        self.assertEquals(0x00, self.bank[0xff])
        self.assertEquals(0x00, self.bank[0x100])
                
    def test_find_by_address_0(self):
        self.assertEquals(self.block0, self.bank.find(0x00)) 
        
    def test_find_by_address_1(self):
        self.assertEquals(self.block1, self.bank.find(0x1ff))
        
    def test_find_by_address_invalid(self):
        self.assertRaises(memory.AddressBusError, self.bank.find, 0xffff) 
        
    def test_find_by_name(self):
        self.assertEquals(self.block1, self.bank.find('block1')) 
        
    def test_find_by_name_invalid(self):
        self.assertRaises(KeyError, self.bank.find, 'block2')
        

