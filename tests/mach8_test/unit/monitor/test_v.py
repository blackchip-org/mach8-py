#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_v.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 
   
class TestR(console.TestHarness):
    
    def test_v(self):
        suite.banner(self.test_v) 
        self.run_test("""
a(lda_imm, 'foo') 
a(jmp_abs, 'bar')
a(bra,     'baz') 
a(sta_zp,  'fuz')
a(lda_imm, add(1, 'foo'))
v""")
        self.assertEquals('$2001 val foo', self.results[-7])
        self.assertEquals('$2003 abs bar', self.results[-6])
        self.assertEquals('$2006 rel baz', self.results[-5])
        self.assertEquals('$2008 zp  fuz', self.results[-4])
        self.assertEquals('$200a val foo: [1 + foo]', self.results[-3])

    def test_v_empty(self):
        suite.banner(self.test_v_empty) 
        self.run_test('v')
        self.assertEquals('mach8>', self.results[-2])
