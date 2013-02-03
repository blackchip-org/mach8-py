#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_inspector.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
import unittest
from mach8 import memory, vm 
from mach8_test import suite 

class TestMemoryInspector(unittest.TestCase):
    
    def setUp(self):
        self.mem = memory.Block(pages=256) 
        self.mem[0x00:0x10] = vm.bstr('ABCDEFGHIJKLMNOP')    
        self.mem[0x10:0x20] = vm.bstr('abcdefghijklmnop')
        
    def test_line0(self):
        suite.banner(self.test_line0)
        result = memory.dump(self.mem, 0x00, 0x0f) 
        suite.log.info(result) 
        self.assertEquals("""
$0000: 41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP
""".strip(), result)
        
    def test_line1(self):
        suite.banner(self.test_line1) 
        result = memory.dump(self.mem, 0x10, 0x1f) 
        suite.log.info(result) 
        self.assertEquals("""
$0010: 61 62 63 64 65 66 67 68  69 6a 6b 6c 6d 6e 6f 70  abcdefghijklmnop
""".strip(), result) 
        
    def test_lines(self):
        suite.banner(self.test_lines) 
        result = memory.dump(self.mem, 0x00, 0x1f) 
        suite.log.info(result) 
        self.assertEquals("""
$0000: 41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP
$0010: 61 62 63 64 65 66 67 68  69 6a 6b 6c 6d 6e 6f 70  abcdefghijklmnop
""".strip(), result)
        
    def test_partial_line(self):
        suite.banner(self.test_partial_line) 
        result = memory.dump(self.mem, 0x07, 0x0d)
        suite.log.info(result) 
        self.assertEquals("""
$0000:                      48  49 4a 4b 4c 4d 4e               HIJKLMN  
""".strip(), result)
        
    def test_partial_overlap(self):
        suite.banner(self.test_partial_overlap) 
        result = memory.dump(self.mem, 0x07, 0x13)
        suite.log.info(result) 
        self.assertEquals("""
$0000:                      48  49 4a 4b 4c 4d 4e 4f 50         HIJKLMNOP
$0010: 61 62 63 64                                       abcd
""".strip(), result) 
        
    def test_one(self):
        suite.banner(self.test_one) 
        result = memory.dump(self.mem, 0, 0) 
        suite.log.info(result) 
        self.assertEquals("""
$0000: 41                                                A""".strip(), result) 
        
    def test_none(self):
        suite.banner(self.test_none) 
        result = memory.dump(self.mem, 10, 0) 
        suite.log.info(result) 
        self.assertEquals('', result) 
        
    def test_end_of_memory(self):
        suite.banner(self.test_end_of_memory)
        result = memory.dump(self.mem, 0xfff0, 0x1000f) 
        suite.log.info(result) 
        self.assertEquals("""
$fff0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
$0000: 41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP
""".strip(), result) 
        
        