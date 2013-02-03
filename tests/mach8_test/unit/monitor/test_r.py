#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_r.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 
   
class TestR(console.TestHarness):

    def test_run_label(self):
        suite.banner(self.test_run_label)
        self.run_test("r('WELCOME')")
        self.assertEquals('Welcome to the Mach-8!', self.results[-4])
        
    def test_run_address(self):
        suite.banner(self.test_run_address) 
        self.run_test("""\
a.position = 0x5000
a(jsr, 'WELCOME')
a(rts) 
r(0x5000)""")
        self.assertEquals('Welcome to the Mach-8!', self.results[-4])
        
    def test_run(self):
        suite.banner(self.test_run) 
        self.run_test("""\
a(jsr, 'WELCOME')
a(rts) 
r""")
        self.assertEquals('Welcome to the Mach-8!', self.results[-4])

    def test_break(self):
        suite.banner(self.test_break) 
        self.run_test('r')
        self.assertEquals('[break]', self.results[-5])

        
        
