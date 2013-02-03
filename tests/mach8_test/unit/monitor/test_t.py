#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_t.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 
   
class TestR(console.TestHarness):

    def test_three_deep(self):
        suite.banner(self.test_three_deep)
        self.shell.config.err = True 
        self.run_test("""
a(jsr, 'test.one')
a(brk) 
a(nop)
a('test.one')
a(nop)
a(pha)
a(pha)
a(jsr, 'test.two')
a(pla)
a(pla)
a(rts) 
a('test.two')
a(nop)
a(jsr, 'test.three')
a(rts) 
a('test.three')
a(pha) 
a(nop)
a('break.here')
a(nop)
a(pla) 
a(rts) 
d('PROGRAM_START', 0x2011)
b('break.here')
r
t""")
        self.assertEquals('$2015  1 <current>', self.results[-6])
        self.assertEquals('$200f  0 jsr test.three', self.results[-5])
        self.assertEquals('$2008  2 jsr test.two', self.results[-4])
        self.assertEquals('$2000  0 jsr test.one', self.results[-3])

    def test_no_jsr(self):
        suite.banner(self.test_no_jsr) 
        self.run_test("""
a(lda_imm, 0x22)
a(brk)
r
t""")
        self.assertEquals('$2004  0 <current>', self.results[-3])

    def test_no_run(self):
        suite.banner(self.test_no_run) 
        self.run_test('t')
        self.assertEquals('mach8> t', self.results[-3])
        self.assertEquals('mach8>', self.results[-2])
