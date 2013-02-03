#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011-2012, Reprint what you like.
#
# $Id: test_fib.py 147 2012-03-22 02:13:46Z mcgann $
#------------------------------------------------------------------------------
from asm import fib
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestPally(execution.TestHarness):
            
    def test_output(self):
        suite.banner(self.test_output)
        a = self.a
        
        _;      a(jsr,      'fib')
        _;      a(brk)
        _;      a(nop)
        
        fib.assemble(self.a) 
        self.run_test() 
        
        self.assertEquals("""\
1
1
2
3
5
8
13
21
34
55
89
""".strip(), self.output.getvalue().strip()) 