#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_b.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestB(console.TestHarness):
    
    def test_add_breakpoint(self):
        suite.banner(self.test_add_breakpoint)
        self.run_test("""\
a(lda_imm, 0x11)
a(lda_imm, 0x22)
a(lda_imm, 0x33)
a(lda_imm, 0x44)
a(brk)
a(nop)
b(0x2004)
r""")
        self.assertEquals('[breakpoint]', self.results[-5])
        self.assertEquals('2003 20 22 00 00 fd  . . * . . . . .', 
                          self.results[-3])

    def test_add_breakpoint_label(self):
        suite.banner(self.test_add_breakpoint_label)
        self.run_test("""\
a(lda_imm, 0x11)
a(lda_imm, 0x22)
a('break_here')
a(lda_imm, 0x33)
a(lda_imm, 0x44)
a(brk)
a(nop)
b('break_here')
r""")
        self.assertEquals('[breakpoint]', self.results[-5])
        self.assertEquals('2003 20 22 00 00 fd  . . * . . . . .', 
                          self.results[-3])
        
    def test_remove_breakpoint(self):
        suite.banner(self.test_remove_breakpoint)
        self.run_test("""\
a(lda_imm, 0x11)
a(lda_imm, 0x22)
a('break_here')
a(lda_imm, 0x33)
a(lda_imm, 0x44)
a(brk)
a(nop)
b('break_here')
b('break_here')
r""")
        self.assertEquals('[break]', self.results[-5])
        
        
    def test_list_breakpoints(self):
        suite.banner(self.test_list_breakpoints)
        self.run_test("""\
b(0x4000)
b(0x3000)
b(0x5000)
a.label('foo', 0x3000)
a.label('bar', 0x3000) 
a.label('baz', 0x4000) 
b""")
        self.assertEquals('$3000: bar, foo', self.results[-5])
        self.assertEquals('$4000: baz', self.results[-4])
        self.assertEquals('$5000', self.results[-3])
        
    def test_clear_breakpoints(self):
        suite.banner(self.test_clear_breakpoints)
        self.run_test("""\
b(0x4000)
b(0x3000)
b(0x5000)
b(0)
b""")
        self.assertEquals('mach8>', self.results[-2])

