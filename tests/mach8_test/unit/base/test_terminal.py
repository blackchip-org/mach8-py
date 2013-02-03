#------------------------------------------------------------------------------
# Vintage Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_terminal.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8 import io, aliases, memory, memmap
import StringIO
import unittest
from mach8_test import mock

class TestTerminal(unittest.TestCase):
        
    def setUp(self):
        self.mem = memory.Block(pages=1)
        
    def test_output(self):
        output = StringIO.StringIO()
        service = io.TerminalOutput(self.mem, destination=output)       
        value = 'Hello'
        for char in value:
            self.mem[memmap.TERM_OUTPUT] = ord(char)
            self.mem.set_bits(memmap.TERM_STATUS, aliases.TERM_TX_READY)
            service()
            service() # Check for nothing when TX not ready
        self.assertEquals(value, output.getvalue())
        
    def test_input(self):
        input = mock.TerminalInputSlow('Baz')
        service = io.TerminalInput(self.mem, source=input) 
        service() # Check for nothing when RX request not set
        characters = []
        for i in xrange(6): 
            self.mem.set_bits(memmap.TERM_STATUS, aliases.TERM_RX_REQUEST)
            service() 
            if self.mem.is_set(memmap.TERM_STATUS, aliases.TERM_RX_READY):
                characters += [chr(self.mem[memmap.TERM_INPUT])]
                self.mem.clear_bits(memmap.TERM_STATUS, aliases.TERM_RX_READY)
            i # Remove warning
        answer = ''.join(characters) 
        
        self.assertEquals('Baz', answer)
