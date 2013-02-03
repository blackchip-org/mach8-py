#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: addressing.py 144 2012-03-19 22:09:00Z mcgann $
#------------------------------------------------------------------------------
"""
Addressing mode constants. 
"""

__all__ = ['ABS', 'ABX', 'ABY', 'ACC', 'IMP', 'IMM', 'IND', 'IZX', 'IZY', 
           'REL', 'ZP', 'ZPX', 'ZPY']

ABS = 'abs'
"""
Absolute addressing with a 16-byte address. 

The following example loads the value of ``0x42`` into the accumulator:
   >>> mem[0x2000] = 0x42
   >>> a(lda_abs, 0x2000)
"""

ABX = 'abx'
""" 
Absolute addressing with a 16-byte address, plus the value of the 
:attr:`X <mach8.x6502.CPU.x>` register.

The following example loads the value of ``0x42`` into the accumulator:
   >>> mem[0x20ab] = 0x42
   >>> cpu.x = 0xab
   >>> a(lda_abx, 0x2000)
"""

ABY = 'aby'
"""
Absolute addressing with a 16-byte address plus, the value of the 
:attr:`Y <mach8.x6502.CPU.y>` register. 

The following example loads the value of ``0x42`` into the accumulator:
   >>> mem[0x20ab] = 0x42
   >>> cpu.y = 0xab
   >>> a(lda_aby, 0x2000)
"""

ACC = 'acc'
"""
Operand is the value in the :attr:`accumulator <mach8.x6502.CPU.a>`

The following example loads the value of 128 into the accumulator:
   >>> cpu.a = 64
   >>> a(asl_acc)
"""

IMP = 'imp'
"""
Implied --- operation takes no arguments. 

Example:
   >>> a(tax) 
"""

IMM = 'imm'
"""
Immediate --- operand is a literal value. 

The following example loads the value of ``0x42`` into the accumulator:
   >>> a(lda_imm, 0x42) 
"""

IND = 'ind'
"""
Indirect addressing. 

The following example jumps to ``0x8000``: 
   >>> mem[0xaaaa] = 0x8000
   >>> a(jmp_ind, 0xaaaa)
"""

IZX = 'izx'
"""
Indexed indirect on a 8-byte zero page address. 

The following example loads '0x42' into the accumulator:
   >>> mem[0x88dd] = 0x42
   >>> mem[0xab::2] = 0x88dd
   >>> cpu.x = 0x0b 
   >>> a(lda_izx, 0xa0) 
"""

IZY = 'izy'
"""
Indirect indexed on a 8-byte zero page address. 

The following example loads '0x42' into the accumulator:
   >>> mem[0x88dd] = 0x42
   >>> mem[0xab::2] = 0x8800
   >>> cpu.y = 0xdd
   >>> a(lda_izy, 0xab)
"""

REL = 'rel'
"""
Relative addressing with an 8-byte displacement. Used in branch instructions.
"""

ZP  = 'zp'
"""
Absolute addressing with a 8-byte zero page address. 

The following example loads the value of ``0x42`` into the accumulator:
   >>> mem[0x20] = 0x42
   >>> a(lda_abs, 0x20)
"""

ZPX = 'zpx'
"""
Absolute addressing with a 8-byte zero page address, plus the value of the 
:attr:`X <mach8.x6502.CPU.x>` register.

The following example loads the value of ``0x42`` into the accumulator:
   >>> mem[0x2b] = 0x42
   >>> cpu.x = 0xb
   >>> a(lda_abx, 0x20)
"""

ZPY = 'zpy'
"""
Absolute addressing with a 8-byte zero page address, plus the value of the 
:attr:`Y <mach8.x6502.CPU.y>` register.

The following example loads the value of ``0x42`` into the accumulator:
   >>> mem[0x2b] = 0x42
   >>> cpu.y = 0xb
   >>> a(lda_abx, 0x20)
"""