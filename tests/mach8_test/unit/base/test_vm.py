#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_vm.py 82 2011-11-16 02:08:42Z mcgann $
#------------------------------------------------------------------------------
from mach8 import vm
import unittest

class TestVM(unittest.TestCase):
    
    def test_bstr(self):
        self.assertEquals([ord('A'), ord('B')], vm.bstr('AB'))
                
    def test_lb(self):
        self.assertEquals(0x34, vm.lb(0x1234))

    def test_hb(self):
        self.assertEquals(0x12, vm.hb(0x1234))
        
    def test_hex8(self):
        self.assertEquals('$0a', vm.hex8(0x0a)) 

    def test_hex16(self):
        self.assertEquals('$0abc', vm.hex16(0x0abc)) 
                        
    def test_bin8(self):
        self.assertEquals('b10101010', vm.bin8(0xaa)) 
        
    def test_is8(self):
        self.assertTrue(vm.is8(0xff)) 
        
    def test_is8_false(self):
        self.assertFalse(vm.is8(0x100)) 
        
    def test_is8s_low(self):
        self.assertTrue(vm.is8s(-128)) 
        
    def test_is8s_high(self):
        self.assertTrue(vm.is8s(255))
        
    def test_is8s_too_low(self):
        self.assertFalse(vm.is8s(-129))
        
    def test_is8s_too_high(self):
        self.assertFalse(vm.is8s(256)) 

    def test_size8s_low(self):
        self.assertEquals(-128, vm.size8s(-128)) 
        
    def test_size8s_high(self):
        self.assertEquals(255, vm.size8s(255))
        
    def test_size8s_too_low(self):
        self.assertRaises(OverflowError, vm.size8s, -129)
        
    def test_size8s_too_high(self):
        self.assertRaises(OverflowError, vm.size8s, 256) 
                
    def test_is16(self):
        self.assertTrue(vm.is16(0xffff))
        
    def test_is16_false(self):
        self.assertFalse(vm.is16(0x10000)) 
        
    def test_mask8(self):
        self.assertEquals(0xff, vm.mask8(0xff)) 
        
    def test_mask8_mask(self):
        self.assertEquals(0xff, vm.mask8(0x12ff)) 
        
    def test_mask16(self):
        self.assertEquals(0xffff, vm.mask16(0xffff)) 
        
    def test_mask16_mask(self):
        self.assertEquals(0xffff, vm.mask16(0x1234ffff)) 
                        
    def test_size8(self):
        self.assertEquals(0xff, vm.size8(0xff)) 
        
    def test_size8_negative(self):
        self.assertEquals(vm.SBYTE_MIN, vm.size8(vm.SBYTE_MIN)) 
        
    def test_size8_overflow(self):
        self.assertRaises(OverflowError, vm.size8, 0x100) 
        
    def test_size8_negative_overflow(self):
        self.assertRaises(OverflowError, vm.size8, vm.SBYTE_MIN - 1) 
        
    def test_size16(self):
        self.assertEquals(0xffff, vm.size16(0xffff)) 
        
    def test_size16_negative(self):
        self.assertEquals(vm.SWORD_MIN, vm.size16(vm.SWORD_MIN)) 
        
    def test_size16_overflow(self):
        self.assertRaises(OverflowError, vm.size16, 0x10000) 
        
    def test_size16_negative_overflow(self):
        self.assertRaises(OverflowError, vm.size16, vm.SWORD_MIN - 1) 
                
    def test_word(self):
        self.assertEquals(0x1234, vm.word(0x34, 0x12))

    def test_word_invalid_low(self):
        self.assertRaises(OverflowError, vm.word, 0x345, 0x12)
            
    def test_word_invalid_high(self):
        self.assertRaises(OverflowError, vm.word, 0x34, 0x123)
        
    def test_to_words(self):
        self.assertEquals([0x1234, 0x5678], 
                          vm.to_words([0x34, 0x12, 0x78, 0x56]))
        
    def test_to_words_invalid_length(self):
        self.assertRaises(ValueError, vm.to_words, [0x12, 0x34, 0x56])
        
    def test_from_words(self):
        self.assertEquals([0x34, 0x12, 0x78, 0x56], 
                          vm.from_words([0x1234, 0x5678]))
        
    def test_twos_forward(self):
        self.assertEquals(0x02, vm.twos_forward(2)) 
    
    def test_twos_forward_negative(self):
        self.assertEquals(0xfe, vm.twos_forward(-2))
        
    def test_twos_forward_max_signed(self):
        self.assertEquals(0x7f, vm.twos_forward(127))
    
    def test_twos_forward_min_signed(self):
        self.assertEquals(0x80, vm.twos_forward(-128))
        
    def test_twos_forward_max_unsigned(self): 
        self.assertEquals(0xff, vm.twos_forward(255)) 
        
    def test_twos_forward_too_high(self):
        self.assertRaises(OverflowError, vm.twos_forward, 0x100) 
        
    def test_twos_forward_too_low(self):
        self.assertRaises(OverflowError, vm.twos_forward, -129) 
        
    def test_twos_inverse(self):
        self.assertEquals(2, vm.twos_inverse(0x02)) 
        
    def test_twos_inverse_negative(self):
        self.assertEquals(-1, vm.twos_inverse(0xff))
        
    def test_twos_inverse_min(self):
        self.assertEquals(-128, vm.twos_inverse(0x80))

    def test_twos_inverse_max(self):
        self.assertEquals(127,  vm.twos_inverse(0x7f))

    def test_twos_inverse_too_large(self):        
        self.assertRaises(OverflowError, vm.twos_inverse, 0x100)
        
    def test_bcd_forward(self):
        self.assertEquals(0x42, vm.bcd_forward(42))
        
    def test_bcd_inverse(self):
        self.assertEquals(42, vm.bcd_inverse(0x42))
        
    def test_bcd_invalid(self):
        self.assertRaises(TypeError, vm.bcd_forward(0x0a))
               
    def test_byte(self):
        self.assertEquals(0xab, vm.byte(0xb, 0xa)) 
    
    def test_py2fac(self):
        self.assertListEqual([0x00, 0x70, 0x56, 0x34, 0x12, 0x00], 
                             vm.py2fac(1.234567))
   
    def test_fac2py(self):
        bytes = [0x00, 0x70, 0x56, 0x34, 0x12, 0x00]
        self.assertEquals(1.234567, vm.fac2py(bytes))
        
    def test_py2fac_exponent6(self):
        self.assertListEqual([0x00, 0x70, 0x56, 0x34, 0x12, 0x06], 
                             vm.py2fac(1234567))
        
    def test_fac2py_exponent6(self):
        bytes = [0x00, 0x70, 0x56, 0x34, 0x12, 0x06]
        self.assertEquals(1234567, vm.fac2py(bytes))
        
    def test_py2fac_exponent2(self):
        self.assertListEqual([0x00, 0x00, 0x00, 0x30, 0x12, 0x02], 
                             vm.py2fac(123))

    def test_fac2py_exponent2(self):
        bytes = [0x00, 0x00, 0x00, 0x30, 0x12, 0x02]
        self.assertEquals(123, vm.fac2py(bytes))
        
    def test_py2fac_sign_mantissa(self):
        self.assertListEqual([0xf0, 0x70, 0x56, 0x34, 0x12, 0x06], 
                             vm.py2fac(-1234567))

    def test_fac2py_sign_mantissa(self):
        bytes = [0xf0, 0x70, 0x56, 0x34, 0x12, 0x06]
        self.assertEquals(-1234567, vm.fac2py(bytes))
        
    def test_py2fac_sign_mantissa_with_exponent(self):
        self.assertListEqual([0xf0, 0x70, 0x56, 0x34, 0x12, 0x42], 
                             vm.py2fac(-1.234567e42))

    def test_fac2py_sign_mantissa_with_exponent(self):
        bytes = [0xf0, 0x70, 0x56, 0x34, 0x12, 0x42]
        self.assertEquals(-1.234567e42, vm.fac2py(bytes))
        
    def test_py2fac_sign_both(self):
        self.assertListEqual([0xff, 0x70, 0x56, 0x34, 0x12, 0x42], 
                             vm.py2fac(-1.234567e-42))
       
    def test_fac2py_sign_both(self):
        bytes = [0xf0, 0x70, 0x56, 0x34, 0x12, 0x42]
        self.assertEquals(-1.234567e42, vm.fac2py(bytes)) 
        
    def test_ln(self):
        self.assertEquals(0xb, vm.ln(0xab)) 
        
    def test_hn(self):
        self.assertEquals(0xa, vm.hn(0xab)) 
        
