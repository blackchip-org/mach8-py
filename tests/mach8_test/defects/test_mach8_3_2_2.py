#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_mach8_3_2_2.py 148 2012-03-22 02:29:57Z mcgann $
#------------------------------------------------------------------------------
from mach8 import monitor
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestDefects_3_2_2(execution.TestHarness):
    
    def test_meta_cleared(self):
        """
        === Defect ===
        Incorrect disassembly display when assembling demo segment after 
        asm.fib was loaded. 
        
        === Steps to reproduce ===
        l('asm.fib')
        a.position = 0x2000 
        a(ldx_imm, 0x00) 
        a(ldy_imm, 0x30) 
        a(jsr, 'STROUT') 
        a(rts)
        d(0x2000, 0x2007) 

        === Incorrect output === 
        PROGRAM_START:
            $2000: a2 00     ldx #$00
            $2002: a0 30     ldy #fib.acc
            $2004: 20 15 07  jsr STROUT
            $2007: 60        rts
            
        === Correct output === 
            $2002: a0 30     ldy #$30
            
        === Reason ===
        Assembler does not set _new_position to True when PC advanced during
        a normal assembly operation. 
        """

        from asm import fib
        a = self.a
        fib.assemble(a) 
        
        a.position = 0x2000 
        a(ldx_imm, 0x00) 
        a(ldy_imm, 0x30) 
        a(jsr, 'STROUT') 
        a(rts)
        
        result = self.d.dump(0x2000, 0x2007)
        lines = result.splitlines()
        self.assertEquals('$2002: a0 30     ldy #$30', lines[2].lstrip())

    def test_clear_binary_flag_on_load(self):
        """
        === Defect ===
        Programs may raise an InvalidBCDNumberError trap after running 
        'asm.fib'
        
        === Steps to reproduce ===
        mach8> l('asm.fib')
        mach8> r
        mach8> l('asm.hello')
        mach8> r
        
        === Incorrect execution ===
        InvalidBCDNumberError trap raised. 
        
        === Correct execution ===
        Prints 'Hello world!'
        
        === Reason ===
        D flag needs to be cleared when loading a new program. Corrective
        action for now is to clear the flag at the end of asm.fib, but this
        needs to be fixed later. A bug in the test suite is preventing proper
        testing at the moment. 
        """
        suite.banner(self.test_clear_binary_flag_on_load) 
        
        sh = monitor.Shell(self.comp) 
        sh.l('asm.fib')
        sh.r()
        sh.l('asm.hello')
        sh.r()
        
    def test_d_flag_cleared_on_reset(self):
        """
        === Defect === 
        An InvalidBCDNumberError trap raised on reset if D flag is set. 
        
        === Steps to reproduce ===
        mach8> cpu.d = True
        mach8> z
        
        === Reason ===
        Flag must be cleared in the initialization routines. 
        """
        suite.banner(self.test_d_flag_cleared_on_reset)
        
        self.cpu.d = True
        self.run_test() 
        
        
                


