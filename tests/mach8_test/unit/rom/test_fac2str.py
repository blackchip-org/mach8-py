#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_fac2str.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import *
from mach8_test import suite
from mach8_test.harness import execution
from mach8 import aliases, memmap, memory

m0_end = memmap.FAC0_MANTISSA + 4

class TestFAC2STR(execution.TestHarness):
    
    def setUp(self):
        execution.TestHarness.setUp(self)
        a = self.a
                
        _;      a(jsr,      'FAC2STR0')
        _;      a(jsr,      'TXTOUT')
        
    def tearDown(self):        
        suite.log.debug('\n')
        fac = memory.dump(self.mem, aliases.FAC0, aliases.FAC0 + 12)
        suite.log.debug(fac) 
        text = memory.dump(self.mem, memmap.TEXT_WORK, memmap.TEXT_WORK + 0x0f)
        suite.log.debug(text) 
        
    def test_fac2str_00(self):
        suite.banner(self.test_fac2str_00)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 6
        self.run_test() 
        self.assertEquals('1234567', self.output.getvalue()) 
        
    def test_fac2str_01(self):
        suite.banner(self.test_fac2str_01)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 5
        self.run_test() 
        self.assertEquals('123456.7', self.output.getvalue()) 
     
    def test_fac2str_02(self):
        suite.banner(self.test_fac2str_02)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 0
        self.run_test() 
        self.assertEquals('1.234567', self.output.getvalue()) 

    def test_fac2str_03(self):
        suite.banner(self.test_fac2str_03)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 8
        self.run_test() 
        self.assertEquals('1.234567E+08', self.output.getvalue()) 
                   
    def test_fac2str_04(self):
        suite.banner(self.test_fac2str_04)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 6
        self.mem[memmap.FAC0_SIGN] = aliases.SIGN_MANTISSA
        self.run_test() 
        self.assertEquals('-1234567', self.output.getvalue()) 
        
    def test_fac2str_05(self):
        suite.banner(self.test_fac2str_05) 
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x00, 0x40]
        self.run_test() 
        self.assertEquals('4', self.output.getvalue()) 

    def test_fac2str_06(self):
        suite.banner(self.test_fac2str_06)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x00, 0x40]
        self.mem[memmap.FAC0_SIGN] = aliases.SIGN_MANTISSA
        self.run_test() 
        self.assertEquals('-4', self.output.getvalue()) 
        
    def test_fac2str_07(self):
        suite.banner(self.test_fac2str_07)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x10, 0x42]
        self.mem[memmap.FAC0_EXPONENT] = 2
        self.run_test() 
        self.assertEquals('421', self.output.getvalue())         

    def test_fac2str_08(self):
        suite.banner(self.test_fac2str_08) 
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 1
        self.mem[memmap.FAC0_SIGN] = aliases.SIGN_EXPONENT
        self.run_test() 
        self.assertEquals('0.1234567', self.output.getvalue())   
        
    def test_fac2str_09(self):
        suite.banner(self.test_fac2str_09)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x10, 0x42]
        self.mem[memmap.FAC0_EXPONENT] = 2
        self.mem[memmap.FAC0_SIGN] = aliases.SIGN_EXPONENT
        self.run_test() 
        self.assertEquals('0.0421', self.output.getvalue())  

    def test_fac2str_10(self):
        suite.banner(self.test_fac2str_10)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x00, 0x40]
        self.mem[memmap.FAC0_EXPONENT] = 6
        self.mem[memmap.FAC0_SIGN] = aliases.SIGN_EXPONENT
        self.run_test() 
        self.assertEquals('0.000004', self.output.getvalue())          

    def test_fac2str_11(self):
        suite.banner(self.test_fac2str_11) 
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x00, 0x40]
        self.mem[memmap.FAC0_EXPONENT] = 8
        self.mem[memmap.FAC0_SIGN] = aliases.SIGN_EXPONENT
        self.run_test() 
        self.assertEquals('4.000000E-08', self.output.getvalue())   

    def test_fac2str_12(self):
        suite.banner(self.test_fac2str_12)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x70, 0x56, 0x34, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 2
        self.mem[memmap.FAC0_SIGN] = (aliases.SIGN_EXPONENT | 
                                      aliases.SIGN_MANTISSA)
        self.run_test() 
        self.assertEquals('-1.234567E-02', self.output.getvalue())  

    def test_fac2str_13(self):
        suite.banner(self.test_fac2str_13)
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x00, 0x12]
        self.mem[memmap.FAC0_EXPONENT] = 2
        self.run_test() 
        self.assertEquals('120', self.output.getvalue())          

    def test_fac2str_14(self):
        suite.banner(self.test_fac2str_14) 
        self.mem[memmap.FAC0_MANTISSA:m0_end] = [0x00, 0x00, 0x00, 0x10]
        self.mem[memmap.FAC0_EXPONENT] = 1
        self.run_test() 
        self.assertEquals('10', self.output.getvalue()) 
        