#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_c.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestC(console.TestHarness):
    
    def test(self):
        suite.banner(self.test)
        self.run_test("""\
cpu.pc = 0x1234
cpu.a  = 0x56
cpu.x  = 0x78
cpu.y  = 0x9a
cpu.sr = 0xff
cpu.sp = 0xff
c""")
        self.assertEquals('1234 ff 56 78 9a ff  * * * * * * * *', 
                          self.results[-3])
