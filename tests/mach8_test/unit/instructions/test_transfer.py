#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_transfer.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestTransfer(execution.TestHarness):
    
    def test_tax(self):  
        suite.banner(self.test_tax)       
        a = self.a
           
        _;      a(lda_imm,  0x44)
        _;      a(tax)
        
        self.run_test()
        self.assertEquals(0x44, self.cpu.x) 
        self.assertTrue(not self.cpu.n and not self.cpu.z)
        
    def test_tax_zero(self):
        suite.banner(self.test_tax_zero) 
        a = self.a

        _;      a(lda_imm,  0x00)
        _;      a(tax)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.x) 
        self.assertTrue(not self.cpu.n and self.cpu.z)
        
    def test_tax_signed(self):
        suite.banner(self.test_tax_signed) 
        a = self.a
         
        _;      a(lda_imm,  0xaa)
        _;      a(tax)
        
        self.run_test()
        self.assertEquals(0xaa, self.cpu.x) 
        self.assertTrue(self.cpu.n and not self.cpu.z)
        
    def test_txa(self):
        suite.banner(self.test_txa)
        a = self.a
        
        _;      a(ldx_imm,  0x44)
        _;      a(txa)
        
        self.run_test()
        self.assertEquals(0x44, self.cpu.a) 
        self.assertTrue(not self.cpu.n and not self.cpu.z)
        
    def test_txa_zero(self):
        suite.banner(self.test_txa_zero)
        a = self.a 
        
        _;      a(ldx_imm,  0x00)
        _;      a(txa)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.a) 
        self.assertTrue(not self.cpu.n and self.cpu.z)

    def test_txa_signed(self):
        suite.banner(self.test_txa_signed) 
        a = self.a

        _;      a(ldx_imm,  0xaa)
        _;      a(txa)
        
        self.run_test()
        self.assertEquals(0xaa, self.cpu.a) 
        self.assertTrue(self.cpu.n and not self.cpu.z)

    def test_tay(self):
        suite.banner(self.test_tay)          
        a = self.a
        
        _;      a(lda_imm,  0x44)
        _;      a(tay)
        
        self.run_test()
        self.assertEquals(0x44, self.cpu.y) 
        self.assertTrue(not self.cpu.n and not self.cpu.z)
        
    def test_tay_zero(self):
        suite.banner(self.test_tay_zero) 
        a = self.a
        
        _;      a(lda_imm,  0x00)
        _;      a(tay)

        self.run_test()
        self.assertEquals(0x00, self.cpu.y) 
        self.assertTrue(not self.cpu.n and self.cpu.z)
        
    def test_tay_signed(self):
        suite.banner(self.test_tay_signed) 
        a = self.a
        
        _;      a(lda_imm,  0xaa)
        _;      a(tay)
        
        self.run_test()
        self.assertEquals(0xaa, self.cpu.y) 
        self.assertTrue(self.cpu.n and not self.cpu.z)
        
    def test_tya(self):
        suite.banner(self.test_tya) 
        a = self.a 
        
        _;      a(ldy_imm,  0x44)
        _;      a(tya)
        
        self.run_test()
        self.assertEquals(0x44, self.cpu.a) 
        self.assertTrue(not self.cpu.n and not self.cpu.z)

    def test_tya_zero(self):
        suite.banner(self.test_tya_zero) 
        a = self.a
        
        _;      a(ldy_imm,  0x00)
        _;      a(tya)
        
        self.run_test()
        self.assertEquals(0x00, self.cpu.a) 
        self.assertTrue(not self.cpu.n and self.cpu.z)
        
    def test_tya_signed(self):
        suite.banner(self.test_tya_signed) 
        a = self.a 

        _;      a(ldy_imm,  0xaa)
        _;      a(tya)
        
        self.run_test()
        self.assertEquals(0xaa, self.cpu.a) 
        self.assertTrue(self.cpu.n and not self.cpu.z)

    