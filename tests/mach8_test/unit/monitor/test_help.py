#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_help.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestHelp(console.TestHarness):
    """
    These tests only check to make sure the help commands run successfully, 
    and that the default help is not executed.  
    """
    
    def test_help(self):
        suite.banner(self.test_help)
        self.run_test('help')
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_a(self):
        suite.banner(self.test_help_a) 
        self.run_test('help(a)')
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_b(self):
        suite.banner(self.test_help_b) 
        self.run_test('help(b)')
        self.assertFalse(self.results[10].startswith('Help on'))
                        
    def test_help_c(self):
        suite.banner(self.test_help_c) 
        self.run_test('help(c)')
        self.assertFalse(self.results[10].startswith('Help on'))
        
    def test_help_d(self):
        suite.banner(self.test_help_d) 
        self.run_test('help(d)')
        self.assertFalse(self.results[10].startswith('Help on'))
    
    def test_help_f(self):
        suite.banner(self.test_help_f) 
        self.run_test('help(f)')
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_g(self):
        suite.banner(self.test_help_g) 
        self.run_test('help(g)')
        self.assertFalse(self.results[10].startswith('Help on'))
                
    def test_help_k(self):
        suite.banner(self.test_help_k) 
        self.run_test('help(k)')
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_l(self):
        suite.banner(self.test_help_k) 
        self.run_test('help(l)')
        self.assertFalse(self.results[10].startswith('Help on'))
                
    def test_help_m(self):
        suite.banner(self.test_help_m) 
        self.run_test('help(m)')    
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_n(self):
        suite.banner(self.test_help_n) 
        self.run_test('help(n)')    
        self.assertFalse(self.results[10].startswith('Help on'))
        
    def test_help_r(self):
        suite.banner(self.test_help_m) 
        self.run_test('help(r)')    
        self.assertFalse(self.results[10].startswith('Help on'))
            
    def test_help_s(self):
        suite.banner(self.test_help_s) 
        self.run_test('help(s)')
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_t(self):
        suite.banner(self.test_help_t) 
        self.run_test('help(t)')
        self.assertFalse(self.results[10].startswith('Help on'))
        
    def test_help_q(self):
        suite.banner(self.test_help_q) 
        self.run_test('help(q)')
        self.assertFalse(self.results[10].startswith('Help on'))

    def test_help_v(self):
        suite.banner(self.test_help_v) 
        self.run_test('help(v)')
        self.assertFalse(self.results[10].startswith('Help on'))
        
    def test_help_w(self):
        suite.banner(self.test_help_w) 
        self.run_test('help(w)')
        self.assertFalse(self.results[10].startswith('Help on'))
        
    def test_help_x(self):
        suite.banner(self.test_help_x) 
        self.run_test('help(x)')
        self.assertFalse(self.results[10].startswith('Help on'))
    
    def test_help_y(self):
        suite.banner(self.test_help_y) 
        self.run_test('help(y)')
        self.assertFalse(self.results[10].startswith('Help on'))
                
    def test_help_z(self):
        suite.banner(self.test_help_z) 
        self.run_test('help(z)')
        self.assertFalse(self.results[10].startswith('Help on'))

        