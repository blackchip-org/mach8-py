#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_stack.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution

class TestStack(execution.TestHarness):
    
    def test_pha(self):
        suite.banner(self.test_pha) 
        a = self.a 
        
        _;      a(lda_imm, 0x11) 
        _;      a(pha) 
        _;      a(lda_imm, 0x22) 
        _;      a(pha) 
        
        self.run_test() 
        self.assertEquals(0x22, self.mem[0x01fe])
        self.assertEquals(0x11, self.mem[0x01ff])
        
    def test_pla(self):
        suite.banner(self.test_pla) 
        a = self.a 
        
        _;      a(pha) 
        _;      a(pha) 
        _;      a(ldy_imm, 0x22) 
        _;      a(sty_abs, 0x1fe) 
        _;      a(ldy_imm, 0x11) 
        _;      a(sty_abs, 0x1ff) 
        _;      a(pla) 
        _;      a(pla) 
        
        self.run_test() 
        self.assertEquals(0x11, self.cpu.a) 
        
    def test_pla_zero(self):
        suite.banner(self.test_pla_zero)
        a = self.a

        _;      a(lda_imm,  0x00)
        _;      a(pha)
        _;      a(lda_imm,  0x22)
        _;      a(pla)
        
        self.run_test() 
        self.assertEquals(0, self.cpu.a)
        self.assertTrue(self.cpu.z and not self.cpu.n)
        
    def test_pla_negative(self):
        suite.banner(self.test_pla_negative) 
        a = self.a 

        _;      a(lda_imm,  0x81) 
        _;      a(pha) 
        _;      a(lda_imm,  0x00)
        _;      a(pla)
         
        self.run_test() 
        self.assertEquals(0x81, self.cpu.a)
        self.assertTrue(not self.cpu.z and self.cpu.n)

    def test_phx(self):
        suite.banner(self.test_phx) 
        a = self.a 
        
        _;      a(ldx_imm, 0x11) 
        _;      a(phx) 
        _;      a(ldx_imm, 0x22) 
        _;      a(phx) 
        
        self.run_test() 
        self.assertEquals(0x22, self.mem[0x01fe])
        self.assertEquals(0x11, self.mem[0x01ff])
        
    def test_plx(self):
        suite.banner(self.test_plx) 
        a = self.a 
        
        _;      a(phx) 
        _;      a(phx) 
        _;      a(lda_imm, 0x22) 
        _;      a(sta_abs, 0x1fe) 
        _;      a(lda_imm, 0x11) 
        _;      a(sta_abs, 0x1ff) 
        _;      a(plx) 
        _;      a(plx) 
        
        self.run_test() 
        self.assertEquals(0x11, self.cpu.x) 
        
    def test_plx_zero(self):
        suite.banner(self.test_plx_zero) 
        a = self.a

        _;      a(ldx_imm,  0x00)
        _;      a(phx)
        _;      a(ldx_imm,  0x22)
        _;      a(plx)
         
        self.run_test() 
        self.assertEquals(0, self.cpu.x)
        self.assertTrue(self.cpu.z and not self.cpu.n)

    def test_plx_negative(self):
        suite.banner(self.test_plx_negative) 
        a = self.a

        _;      a(ldx_imm,  0x81)
        _;      a(phx) 
        _;      a(ldx_imm,  0x00)
        _;      a(plx) 
        
        self.run_test() 
        self.assertEquals(0x81, self.cpu.x)
        self.assertTrue(not self.cpu.z and self.cpu.n)

    def test_phy(self):
        suite.banner(self.test_phy) 
        a = self.a 
        
        _;      a(ldy_imm, 0x11) 
        _;      a(phy) 
        _;      a(ldy_imm, 0x22) 
        _;      a(phy) 
        
        self.run_test() 
        self.assertEquals(0x22, self.mem[0x01fe])
        self.assertEquals(0x11, self.mem[0x01ff])
        
    def test_ply(self):
        suite.banner(self.test_ply) 
        a = self.a 
        
        _;      a(phy) 
        _;      a(phy) 
        _;      a(lda_imm, 0x22) 
        _;      a(sta_abs, 0x1fe) 
        _;      a(lda_imm, 0x11) 
        _;      a(sta_abs, 0x1ff) 
        _;      a(ply) 
        _;      a(ply) 
        
        self.run_test() 
        self.assertEquals(0x11, self.cpu.y) 
        
    def test_ply_zero(self):
        suite.banner(self.test_ply_zero) 
        a = self.a

        _;      a(ldy_imm,  0x00)
        _;      a(phy)
        _;      a(ldy_imm,  0x22)
        _;      a(ply) 
        
        self.run_test() 
        self.assertEquals(0, self.cpu.y)
        self.assertTrue(self.cpu.z and not self.cpu.n)

    def test_ply_negative(self):
        suite.banner(self.test_ply_negative) 
        a = self.a

        _;      a(ldy_imm,  0x81) 
        _;      a(phy) 
        _;      a(ldy_imm,  0x00)
        _;      a(ply)
        
        self.run_test() 
        self.assertEquals(0x81, self.cpu.y)
        self.assertTrue(not self.cpu.z and self.cpu.n)


    def test_php(self):
        suite.banner(self.test_php) 
        a = self.a
        self.cpu.sr = 0b11101011
        
        _;      a(php) 
        
        self.run_test() 
        self.assertEquals(0b11101011, self.mem[0x1ff])

    def test_plp(self):
        suite.banner(self.test_plp) 
        a = self.a 
        
        _;      a(lda_imm,  b8(0b11101011))
        _;      a(pha) 
        _;      a(cmp_imm,  1)
        _;      a(plp) 
        
        self.run_test() 
        # Include the break flag!
        self.assertEquals(0b11111011, self.cpu.sr) 
        
    def test_txs(self):
        suite.banner(self.test_txs) 
        a = self.a

        _;      a(lda_imm,  0x11) 
        _;      a(pha) 
        _;      a(lda_imm,  0x22) 
        _;      a(pha) 
        _;      a(ldx_imm,  0xfe) 
        _;      a(txs)
        _;      a(pla) 
        
        self.run_test()         
        self.assertEquals(0x11, self.cpu.a);
        
    def test_tsx(self):
        suite.banner(self.test_tsx) 
        a = self.a 
        
        _;      a(pha)
        _;      a(pha)
        _;      a(pha) 

        _;      a(tsx) 
        
        _;      a(plp)
        _;      a(plp) 
        _;      a(plp) 
        
        self.run_test() 
        self.assertEquals(0xfc, self.cpu.x)

    
