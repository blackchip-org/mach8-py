#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: execution.py 146 2012-03-22 02:12:42Z mcgann $
#------------------------------------------------------------------------------
import unittest
from mach8_test import suite
from mach8 import tools, mach, memmap, vm
from mach8.assembly import * 
import StringIO 
from mach8_test import noseutil

class TestHarness(unittest.TestCase):
        
    def __init__(self, a):
        unittest.TestCase.__init__(self, a) 
        
    def setUp(self):            
        self.comp = mach.Computer()
        self.cpu = self.comp.cpu 
        self.mem = self.comp.mem
        self.meta = self.comp.meta 
        
        self.a = tools.Assembler(self.mem, memmap.PROGRAM_START, self.meta)
        self.d = tools.Disassembler(self.mem, self.a.position, self.meta) 
    
        self.logging_run = False 
        self.comp.limit = 0xffff
        self.cpu.pc = memmap.PROGRAM_START - 1
        self.output = StringIO.StringIO() 
        self.comp.terminal_output.destination = self.output

    @noseutil.nottest
    def run_test(self, log=False): 
        self.a(brk)
        self.a(nop)  
        self.a.verify()
        
        results = self.d.disassemble(end=self.a.position - 1)
        map(suite.log.info, map(str, results))
                
        if log: 
            self.mem.load_listeners = [self.memory_load_listener]
            self.mem.store_listeners = [self.memory_store_listener]
            self.cpu.run_listeners = [self.run_listener] 
            suite.log.info('\nrun')
        try:
            self.comp.run()
        finally:
            if log: 
                suite.log.info('end')
            suite.log.debug('')
            if len(self.output.getvalue()) > 0: 
                suite.log.debug(self.output.getvalue()) 
                suite.log.debug('')
            suite.log.debug(str(self.cpu)) 
        
    def memory_load_listener(self, address, value):
        if not self.logging_run: 
            suite.log.info('mem {} =-> {}'.format(vm.hex16(address), 
                                                  vm.hex8(value)))
    
    def memory_store_listener(self, address, value):
        if not self.logging_run:
            suite.log.info('mem {} <-= {}'.format(vm.hex16(address), 
                                                  vm.hex8(value)))
    
    def run_listener(self, address, instr):
        print 'BOO'
        self.logging_run = True 
        result = self.d.dump(address)
        suite.log.info(str(result))
        self.logging_run = False  
        
    
