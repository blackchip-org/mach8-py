#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_disassembled.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8 import memmap, memory, tools
from mach8.assembly import * 
import unittest
from mach8_test import suite

class TestDisassembled(unittest.TestCase):
    
    def setUp(self):
        self.d = tools.Disassembled()
        self.d.address = 0xa1b2
        
    def test_no_arg(self):
        suite.banner(self.test_no_arg)
        self.d.instruction = nop 
        self.d.bytes = [nop.opcode]
        suite.log.info(str(self.d))
        self.assertEquals("    $a1b2: ea        nop", str(self.d)) 
        
    def test_byte_arg(self):
        suite.banner(self.test_byte_arg)
        self.d.instruction = lda_imm
        self.d.bytes = [lda_imm.opcode, 0x42]
        suite.log.info(str(self.d)) 
        self.assertEquals("    $a1b2: a9 42     lda #$42", str(self.d)) 
        
    def test_word_arg(self):
        suite.banner(self.test_word_arg)
        self.d.instruction = jmp_abs
        self.d.bytes = [jmp_abs.opcode, 0x34, 0x12]
        suite.log.info(str(self.d)) 
        self.assertEquals("    $a1b2: 4c 34 12  jmp $1234", str(self.d)) 
        
    def test_text_arg(self):
        suite.banner(self.test_text_arg)
        self.d.instruction = jmp_abs
        self.d.bytes = [jmp_abs.opcode, 0x34, 0x12]
        self.d.argument = 'argument'
        suite.log.info(str(self.d)) 
        self.assertEquals("    $a1b2: 4c 34 12  jmp argument", str(self.d)) 
        
    def test_labels(self):
        suite.banner(self.test_labels) 
        self.d.instruction = nop 
        self.d.bytes = [nop.opcode]
        self.d.labels = ['foo', 'bar']
        suite.log.info(str(self.d)) 
        self.assertEquals("""\
foo:
bar:
    $a1b2: ea        nop\
""", str(self.d))
        
    def test_remarks(self):
        suite.banner(self.test_remarks) 
        self.d.instruction = nop 
        self.d.bytes = [nop.opcode]
        self.d.remarks = ['Remark 1', 'Remark 2'] 
        suite.log.info(str(self.d)) 
        self.assertEquals("""\
    ; Remark 1
    ; Remark 2
    $a1b2: ea        nop\
""", str(self.d))
        
    def test_order(self):
        suite.banner(self.test_order) 
        self.d.instruction = nop 
        self.d.bytes = [nop.opcode]
        self.d.remarks = ['Remark']
        self.d.labels = ['Label']
        suite.log.info(str(self.d)) 
        self.assertEquals("""\
Label:
    ; Remark
    $a1b2: ea        nop\
""", str(self.d))
        
    def test_data(self):
        suite.banner(self.test_data) 
        self.d.instruction = nop
        self.d.bytes = [nop.opcode] 
        self.d.data = tools.Data(0xa1b0, 5, repr('Hello'))
        suite.log.info(str(self.d)) 
        self.assertEquals("    $a1b0: data      'Hello'", str(self.d))
        
    def test_data_invalid(self):
        suite.banner(self.test_data_invalid) 
        self.d.instruction = nop
        self.d.bytes = [nop.opcode] 
        self.d.data = tools.Data(0xa1b0, 5, repr('Hello'))
        self.d.data.valid = False 
        suite.log.info(str(self.d)) 
        self.assertEquals("    $a1b2: ea        nop", str(self.d))
        
    def test_empty(self):
        suite.banner(self.test_empty)
        suite.log.info(str(self.d))  
        self.assertEquals('$a1b2: ff        ?XX', str(self.d).strip()) 
        
        
    
