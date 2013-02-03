#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_flags.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestFlags(execution.TestHarness):
    
    def test_sec(self):
        suite.banner(self.test_sec)   
        a = self.a  
        
        _;      a(clc)
        _;      a(sec)
        
        self.run_test()
        self.assertTrue(self.cpu.c)

    def test_clc(self):
        suite.banner(self.test_clc) 
        a = self.a 

        _;      a(sec)
        _;      a(clc)

        self.run_test()
        self.assertFalse(self.cpu.c)

    def test_sei(self):
        suite.banner(self.test_sei)    
        a = self.a
        
        _;      a(cli)
        _;      a(sei)
        
        self.run_test()
        self.assertTrue(self.cpu.i)

    def test_cli(self):
        suite.banner(self.test_cli) 
        a = self.a

        _;      a(sei)
        _;      a(cli)

        self.run_test()
        self.assertFalse(self.cpu.c)

    def test_sed(self):
        suite.banner(self.test_sed)  
        a = self.a
        
        _;      a(cld)
        _;      a(sed)
        
        self.run_test()
        self.assertTrue(self.cpu.d)

    def test_cld(self):
        suite.banner(self.test_cld) 
        a = self.a

        _;      a(sed)
        _;      a(cld)

        self.run_test()
        self.assertFalse(self.cpu.d)

    def test_clv(self):
        suite.banner(self.test_cld) 
        a = self.a
        
        # No SEV command, hand jam
        self.cpu.v = True 
        
        _;      a(clv)

        self.run_test()
        self.assertFalse(self.cpu.v)

