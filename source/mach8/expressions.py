#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: expressions.py 82 2011-11-16 02:08:42Z mcgann $
#------------------------------------------------------------------------------
"""
These functions are used when assembling programs to aid in symbol
lookup and disassembly. For example, the following is valid:

>>> a(lda_imm, 'MY_VALUE') 

because a lookup in the symbol table is automatically performed on
string arguments. The following is invalid:

>>> a(lda_imm, 'MY_VALUE' + 4) 

The :data:`add` expression can be used instead:

>>> a(lda_imm, add('MY_VALUE', 4)) 

These functions are also useful to preserve the intent of literals. The
following assembly shows the following when disassembling:

>>> a(lda_imm, ord('A')) 
$2000: A9 41     LDA #$41

Instead, use the following expression:

>>> a(lda_imm, asc('A'))
$2000: A9 41     LDA #'A'

The disassembler always prints arguments out in hexadecimal, but
arguments within expressions print out in decimal. Use the ``x``
functions to format in hex. Examples:

>>> a(lda_imm, add(10 + 1))
$2000: A9 0B     LDA #[10 + 1]
>>> a(lda_imm, add(x8(10), x8(1)))
$2000: A9 0B     LDA #[$0A + $01]

Square brackets ``[]`` are used for grouping instead of ``()`` to
avoid confusion with the syntax for indirect addressing. This is the
same syntax used in the Ophis assembler.

Instead of importing this module, import the :mod:`mach8.assembly` module which 
includes this module. 

Function Reference
------------------
"""
from mach8 import expression as expr, vm
import operator

__all__ = ['add', 'and_', 'asc', 'b8', 'byte0', 'byte1', 'byte2', 'byte3', 
           'eor', 'hb', 'lb', 'or_', 'sub', 'x8', 'x16', 'x32']
    
add = lambda *args: expr.BinaryExpression(operator.add, ' + ', *args)
"""
Addition. 

>>> a(lda_imm, add(12, 34, 56))
$2000: A9 66     LDA #[12 + 34 + 56]
"""

and_ = lambda *args: expr.BinaryExpression(operator.and_, ' & ', *args) 
"""
Bitwise and.

>>> a(lda_imm, and(x8(0xff), x8(0xf0)))
$2000: A9 F0     LDA #[$FF ^ $F0]
"""

asc = lambda arg: expr.LiteralExpression(ord, expr.format_asc, arg) 
"""
Formats argument as an ASCII character.

>>> a(lda_imm, asc('A'))
$2000: A9 41     LDA #'A'
"""

b8 = lambda arg: expr.LiteralExpression(expr.do_null, vm.bin8, arg) 
"""
Formats argument as an 8-bit binary number. 

>>> a(lda_imm, b8(0xff))
$2000: A9 41     LDA #b11111111
"""

byte0 = lambda arg: expr.UnaryExpression(vm.lb, '{}<0>', arg) 
"""
Byte 0, the lowest byte, of a 32-byte integer. For 16-byte values, use 
:data:`lb` instead. 

>>> a(lda_imm, byte0(x32(0x12345678)))
$2000: A9 78     LDA #$12345678<0>
"""

byte1 = lambda arg: expr.UnaryExpression(vm.hb, '{}<1>', arg)
"""
Byte 1 of a 32-byte integer. For 16-byte values, use :data:`hb` instead. 

>>> a(lda_imm, byte1(x32(0x12345678)))
$2000: A9 56     LDA #$12345678<1>
"""

byte2 = lambda arg: expr.UnaryExpression(expr.do_byte2, '{}<2>', arg)
"""
Byte 2 of a 32-byte integer.

>>> a(lda_imm, byte2(x32(0x12345678)))
$2000: A9 34     LDA #$12345678<2> 
"""

byte3 = lambda arg: expr.UnaryExpression(expr.do_byte3, '{}<3>', arg) 
"""
Byte 3, the highest byte, of a 32-byte integer. 

>>> a(lda_imm, byte3(x32(0x12345678)))
$2000: A9 12     LDA #$12345678<3>
"""

eor = lambda *args: expr.BinaryExpression(operator.xor, ' ^ ', *args) 
"""
Bitwise exclusive or. 

>>> a(lda_imm, eor(x8(0xff), x8(0xf0)))
$2000: A9 0F     LDA #[$FF ^ $F0]
"""

hb = lambda arg: expr.UnaryExpression(vm.hb, '>{}', arg) 
"""
High byte of a 16-byte value.

>>> a(lda_imm, hb(x8(0xfa12)))
$2000: A9 FA     LDA #>$FA12 
"""

lb = lambda arg: expr.UnaryExpression(vm.lb, '<{}', arg) 
"""
Low byte of a 16-bit word.

>>> a(lda_imm, lb(x16(0xfa12))
$2000: A9 12     LDA #<$FA12
"""

or_ = lambda *args: expr.BinaryExpression(operator.or_, ' | ', *args) 
"""
Bitwise or.

>>> a(lda_imm, or_(x8(0x0f), x8(0xf0)))
$2000: A9 FF     LDA #[$0F | $F0]
"""

sub = lambda *args: expr.BinaryExpression(operator.sub, ' - ', *args) 
"""
Subtraction.

>>> a(lda_imm, sub(7, 3))
$2000: A9 04     LDA #[7 - 3]
"""

x8 = lambda arg: expr.LiteralExpression(expr.do_null, vm.hex8, arg) 
"""
Formats argument as a hexadecimal 8-bit value.

>>> a(lda_imm, x8(0x42))
$2000: A9 42     LDA #$42
"""

x16 = lambda arg: expr.LiteralExpression(expr.do_null, vm.hex16, arg) 
"""
Formats argument as a hexadecimal 16-bit value.

>>> a(lda_abs, x16(0x1234) 
$2000: AD 34 12  LDA $1234
"""

x32 = lambda arg: expr.LiteralExpression(expr.do_null, expr.format_x32, arg)
"""
Formats argument as a hexadecimal 32-bit value.

>>> a(lda_imm, byte0(x32(0x12345678)))
$2000: A9 78     LDA #$12345678<0> 
"""


    


        
    