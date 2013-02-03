#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_one_register.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestOneRegister(execution.TestHarness):
            
    def test_inx(self):   
        suite.banner(self.test_inx)       
        a = self.a

        _;      a(ldx_imm,  0xfe)
        _;      a(inx)
        
        self.run_test()
        self.assertEquals(0xff, self.cpu.x)
        self.assertTrue(self.cpu.n and not self.cpu.z)

    def test_inx_wrap(self):
        suite.banner(self.test_inx_wrap) 
        a = self.a 
        
        _;      a(ldx_imm,  0xff) 
        _;      a(inx)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.x) 
        self.assertTrue(not self.cpu.n and self.cpu.z)
   
    def test_inx_dex(self):
        suite.banner(self.test_inx_dex) 
        a = self.a 
        
        _;      a(ldx_imm,  0x00)
        _;      a(inx)
        _;      a(dex)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.x) 
        self.assertTrue(not self.cpu.n and self.cpu.z)
         
    def test_dex_wrap(self):
        suite.banner(self.test_dex_wrap) 
        a = self.a 
        
        _;      a(ldx_imm,  0x00)
        _;      a(dex)
        
        self.run_test()
        self.assertEquals(0xff, self.cpu.x)
        self.assertTrue(self.cpu.n and not self.cpu.z)  
        
    def test_iny(self):
        suite.banner(self.test_iny) 
        a = self.a 
        
        _;      a(ldy_imm,  0xfe)
        _;      a(iny)
        
        self.run_test()
        self.assertEquals(0xff, self.cpu.y)
        self.assertTrue(self.cpu.n and not self.cpu.z)

    def test_iny_wrap(self):
        suite.banner(self.test_iny_wrap) 
        a = self.a 
        
        _;      a(ldy_imm,  0xff) 
        _;      a(iny)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.y) 
        self.assertTrue(not self.cpu.n and self.cpu.z)

    def test_iny_dey(self):
        suite.banner(self.test_iny_dey) 
        a = self.a 
        
        _;      a(ldy_imm,  0x00)
        _;      a(iny)
        _;      a(dey)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.y) 
        self.assertTrue(not self.cpu.n and self.cpu.z)
         
    def test_dey_wrap(self):
        suite.banner(self.test_dey_wrap) 
        a = self.a 
        
        _;      a(ldy_imm,  0x00) 
        _;      a(dey)
        
        self.run_test()
        self.assertEquals(0xff, self.cpu.y)
        self.assertTrue(self.cpu.n and not self.cpu.z)  

