#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_conf.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestConf(console.TestHarness):
    
    def test_exe_true(self):
        suite.banner(self.test_exe_true) 
        self.run_test("""
a(nop)
a(brk)
conf.exe = True
conf.exe = True
r""")
        self.assertEquals('$2001: 00        brk', self.results[-6])
        
    def test_exe_false(self):
        suite.banner(self.test_exe_false) 
        self.run_test("""
a(nop)
a(brk)
conf.exe = True
conf.exe = False
conf.exe = False
r""")
        self.assertEquals('[break]', self.results[-5])
        
    