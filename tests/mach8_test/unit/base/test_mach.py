#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_mach.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8 import mach, x6502
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestMach(execution.TestHarness):
    
    def test_jiffy_timer(self):
        import itertools 
        
        counter1 = itertools.count(0).next
        counter2 = itertools.count(10).next
        
        timer = mach.JiffyTimer(interval=5, actions=[counter1, counter2])
        i = 0
        while i < 12: 
            timer.cycle() 
            i += 1
        self.assertEquals(2, counter1())
        self.assertEquals(12, counter2())
        
    def test_step(self):
        suite.banner(self.test_step) 
        a = self.a 
        
        _;      a(lda_imm, 0x11) 
        _;      a(lda_imm, 0x22) 
        _;      a(lda_imm, 0x33) 
        _;      a(lda_imm, 0x44) 
        
        self.comp.step = True 
        self.run_test() 
        self.assertEquals(0x11, self.cpu.a) 
        self.comp.step = True 
        self.comp.run() 
        suite.log.info('\n' + str(self.cpu)) 
        self.assertEquals(0x22, self.cpu.a) 
        self.comp.run() 
        suite.log.info('\n' + str(self.cpu)) 
        self.assertEquals(0x44, self.cpu.a) 
        
    def test_trap(self):
        suite.banner(self.test_trap) 
        a = self.a 
        
        _;      a.data  (x8(0x02)) 
        
        self.assertRaises(x6502.IllegalInstructionError, self.run_test)
        
    def test_breakpoints(self):
        suite.banner(self.test_breakpoints) 
        a = self.a 
        
        _;      a(lda_imm, 0x11) 
        _;  a('one')
        _;      a(lda_imm, 0x22) 
        _;      a(lda_imm, 0x33) 
        _;  a('two')
        _;      a(lda_imm, 0x44) 
        
        self.comp.breakpoints.add(self.meta['one'])
        self.comp.breakpoints.add(self.meta['two'])

        self.run_test() 
        self.assertEquals(0x11, self.cpu.a) 
        self.comp.run() 
        suite.log.info('\n' + str(self.cpu)) 
        self.assertEquals(0x33, self.cpu.a) 
        self.comp.run() 
        suite.log.info('\n' + str(self.cpu)) 
        self.assertEquals(0x44, self.cpu.a) 

    def test_idle(self):
        suite.banner(self.test_idle) 
        a = self.a 
        
        def action():
            action.count += 1
        action.count = 0        
        self.comp.timer.actions += [action]
        
        _;      a(jsr,      'IDLE')

        self.run_test()         
        # Actions always serviced on exit, so count is 2. 
        self.assertEquals(2, action.count) 
        
    def test_limit(self):
        suite.banner(self.test_limit) 
        a = self.a 
        
        _;      a(ldx_imm,  0) 
        _;  a('loop')
        _;      a(inx) 
        _;      a(bne,      'loop')
        
        self.comp.limit = 10 
        self.assertRaises(mach.LimitExceededError, self.run_test)
        self.assertEquals(10, self.comp.cycles)  

    def test_no_pull(self):
        suite.banner(self.test_no_pull) 
        a = self.a 
        
        _;      a(jsr,      'test.1')
        _;      a(brk)
        _;      a(nop)
        _;  a('test.1')
        _;      a(pha) 
        _;      a(jsr,      'test.2')
        _;      a(rts) 
        _;  a('test.2')
        _;      a(pha) 
        _;      a(pla)
        _;      a(rts) 
        
        self.assertRaises(x6502.StackError, self.run_test)
        
    def test_no_push(self):
        suite.banner(self.test_no_push) 
        a = self.a 
        
        _;      a(jsr,      'test.1')
        _;      a(brk)
        _;      a(nop)
        _;  a('test.1') 
        _;      a(jsr,      'test.2')
        _;      a(pla) 
        _;      a(rts) 
        _;  a('test.2')
        _;      a(pha) 
        _;      a(pla)
        _;      a(rts) 
        
        self.assertRaises(x6502.StackError, self.run_test)
        
    def test_pull_many(self):
        suite.banner(self.test_pull_many) 
        a = self.a 
        
        _;      a(jsr,      'test.1')
        _;      a(brk)
        _;      a(nop)
        _;  a('test.1') 
        _;      a(pha) 
        _;      a(jsr,      'test.2')
        _;      a(pla) 
        _;      a(rts) 
        _;  a('test.2')
        _;      a(pha) 
        _;      a(pla)
        _;      a(pla) 
        _;      a(rts) 
        
        self.assertRaises(x6502.StackError, self.run_test)
        
    def test_stack_overflow(self):
        suite.banner(self.test_stack_overflow) 
        a = self.a 
    
        _;      a(ldx_imm,  0)    
        _;  a('test.loop')
        _;      a(phx) 
        _;      a(inx) 
        _;      a(bne,      'test.loop')
        
        self.assertRaises(x6502.StackError, self.run_test) 
