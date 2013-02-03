#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_block.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
import unittest
from mach8 import memory, vm 

class TestMemoryBlock(unittest.TestCase):

    def setUp(self):
        self.block = memory.Block(pages=2) 
        
    def test_block_new_zero(self):
        self.assertEquals(0x00, self.block[0xa])
        
    def test_block_store_invalid_value(self):
        self.assertRaises(OverflowError, self.block.__setitem__, 0x0a, 0x1234)
        
    def test_block_invalid_index(self):
        self.assertRaises(IndexError, self.block.__setitem__, 0x200, 0x00) 

    def test_block_load_store(self):
        self.block[0x0a] = 0x42
        self.assertEquals(0x42, self.block[0x0a])
    
    def test_block_load_bytes(self):
        self.block[0x0a] = 0x12
        self.block[0x0b] = 0x34
        self.block[0x0c] = 0x56
        self.assertEquals([0x12, 0x34, 0x56], self.block[0x0a:0x0d])
        
    def test_block_load_word(self):
        self.block[0x0a] = 0x34
        self.block[0x0b] = 0x12
        self.assertEquals(0x1234, self.block[0x0a::2])
        
    def test_block_load_word_list(self):
        self.block[0x0a] = 0x34
        self.block[0x0b] = 0x12
        self.assertEquals([0x1234], self.block[0x0a:0x0c:2])

    def test_block_load_word_list2(self):
        self.block[0x0a] = 0x34
        self.block[0x0b] = 0x12
        self.block[0x0c] = 0x78
        self.block[0x0d] = 0x56
        self.assertEquals([0x1234, 0x5678], self.block[0x0a:0x0e:2])
        
    def test_block_load_invalid_step(self):
        self.assertRaises(ValueError, self.block.__getitem__, 
                          slice(0x0a, 0x0e, 3))
        
    def test_block_load_no_start(self):
        self.assertRaises(ValueError, self.block.__getitem__, slice(None, 0x0a))
        
    def test_block_store_bytes(self):
        self.block[0x0a:0x0d] = [0x12, 0x34, 0x56]
        self.assertEquals(0x12, self.block[0x0a])
        self.assertEquals(0x34, self.block[0x0b])
        self.assertEquals(0x56, self.block[0x0c])

    def test_block_store_bytes_mismatch(self):
        self.assertRaises(ValueError, self.block.__setitem__, 
                          slice(0x0a, 0x0c), [0x12, 0x34, 0x56])
        
    def test_block_store_word(self):
        self.block[0x0a::2] = 0x1234
        self.assertEquals(0x1234, vm.word(self.block[0xa], self.block[0xb]))
    
    def test_block_store_word_list(self):
        self.block[0x0a:0x0c:2] = [0x1234]
        self.assertEquals(0x1234, vm.word(self.block[0x0a], self.block[0x0b]))

    def test_block_store_words_mismatch(self):
        self.assertRaises(ValueError, self.block.__setitem__, 
                          slice(0x0a, 0x0c, 2), [0x1234, 0x5678])
        
    def test_block_store_word_list2(self):
        self.block[0x0a:0x0e:2] = [0x1234, 0x5678]
        self.assertEquals(0x1234, vm.word(self.block[0x0a], self.block[0x0b]))
        self.assertEquals(0x5678, vm.word(self.block[0x0c], self.block[0x0d]))
        
    def test_block_store_invalid_step(self):
        self.assertRaises(ValueError, self.block.__setitem__, 
                          slice(0x0a, 0x0e, 3), 0x1234)
        
    def test_block_store_no_start(self):
        self.assertRaises(ValueError, self.block.__setitem__, 
                          slice(None, 0x0a), 0xff)
        
    def test_block_store_read_only(self):
        self.block.read_only = True
        self.assertRaises(memory.ReadOnlyError, 
                          self.block.__setitem__, 0x0a, 0x0a)

    def test_block_load_listener(self):
        self.block[0x0a] = 0xff
        def listener(a, v):
            listener.address = a
            listener.value = v
        self.block.load_listeners += [listener]
        self.block[0x0a]
        self.assertEquals(0x0a, listener.address) 
        self.assertEquals(0xff, listener.value) 
        
    def test_block_store_listener(self):
        def listener(a, v):
            listener.address = a
            listener.value = v
        self.block.store_listeners += [listener]
        self.block[0x0a] = 0xff
        self.assertEquals(0x0a, listener.address) 
        self.assertEquals(0xff, listener.value) 
                
    def test_block_clear(self):
        self.block[0x0a] = 0xff
        self.block.clear() 
        self.assertEquals(0, self.block[0x0a])
        
    def test_block_clear_read_only(self):
        self.block[0x0a] = 0xff
        self.block.read_only = True
        self.block.clear() 
        self.assertEquals(0xff, self.block[0x0a])        
        
    def test_page_boundary(self):
        self.block[0xff] = 0x12
        self.block[0x100] = 0x34
        self.assertEquals(0x12, self.block[0xff])
        self.assertEquals(0x34, self.block[0x100])
        
    def test_set_bits(self):
        self.block[0x10] = 0b11001100
        self.block.set_bits(0x10, 0b01110000)
        self.assertEquals(0b11111100, self.block[0x10])
        
    def test_clear_bits(self):
        self.block[0x10] = 0b11001100
        self.block.clear_bits(0x10, 0b11110000)
        self.assertEquals(0b00001100, self.block[0x10])
