#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: yap.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
import unittest
from mach8_test import suite
from mach8 import tools, mach, memmap, vm
from mach8.assembly import * 
import StringIO 

class TestHarness(unittest.TestCase):
    
    def __init__(self, a):
        unittest.TestCase.__init__(self, a)
        
    def setUp(self):
        self.comp = mach.Computer() 
        self.output = StringIO.StringIO() 
        self.comp.terminal_output.destination = self.output
        self.d = tools.Disassembler(self.comp.mem, origin=memmap.PROGRAM_START, 
                                    meta=self.comp.meta) 
        # Simulate jsr
        self.comp.cpu.push2(self.comp.meta['MONITOR'] - 1)
        self.comp.mem[memmap.YAP_EXIT_VECTOR::2] = self.comp.meta['YAP_EXIT']
        
        self.logging_run = False 
        self.comp.limit = 0x8ff
        
    def _find_program_end(self):
        ptr = memmap.PROGRAM_START 
        marker_count = 0
        
        while True: 
            if self.comp.mem[ptr] == 0: 
                marker_count += 1
                if marker_count == 3: 
                    break 
            else: 
                marker_count = 0
            ptr += 1
        return ptr - 3
    
    def run_test(self, log=False):
        if log: 
            self.comp.cpu.run_listeners += [self.run_listener]
        self.comp.cpu.pc = memmap.PROGRAM_START - 1
        end=self._find_program_end()
        suite.log.info(self.d.dump(end=end))
        if log: 
            suite.log.info('\n***** START')
        self.comp.run() 
        if log: 
            suite.log.info('***** END')
        suite.log.info(self.output.getvalue()) 
        
    def run_listener(self, address, instr):
        self.logging_run = True 
        result = self.d.dump(address)
        suite.log.info(str(result))
        self.logging_run = False  

        
        