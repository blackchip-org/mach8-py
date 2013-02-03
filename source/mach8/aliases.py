#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: aliases.py 144 2012-03-19 22:09:00Z mcgann $
#------------------------------------------------------------------------------
"""
System aliases. 
"""
from mach8 import memmap, vm 

#==============================================================================
# Bits
#==============================================================================

TERM_RX_READY = vm.BIT0 
"""
Bit to set in :data:`TERM_STATUS` when data from the terminal is ready to 
be read. 
"""

TERM_TX_READY = vm.BIT1
"""
Bit to set in :data:`TERM_STATUS` when data is ready to be sent to the 
terminal. 
"""

TERM_RX_REQUEST = vm.BIT2 
"""
Bit to set in :data:`TERM_STATUS` when key presses should be accepted as
input. 
"""

TERM_RX_COMPLETE = ~(TERM_RX_READY | TERM_RX_REQUEST)
"""
Value to AND after reading from the terminal is complete (clears 
:data:`TERM_RX_READY` and :data:`TERM_RX_REQUEST`
"""

#==============================================================================
# Pointers and offsets
#==============================================================================
FAC0 = memmap.FAC0_SIGN
"""
Starting location of floating point accumulator 0.
"""

FAC1 = memmap.FAC1_SIGN
"""
Starting location of floating point accumulator 1. 
"""

FAC_SIGN = 0
"""
Offset from the start of a FAC to the sign byte. 
"""

FAC_MANTISSA = 4
"""
Offset from the start of a FAC to the first mantissa byte (then working
downwards)
"""

FAC_EXPONENT = 5
"""
Offset from the start of a FAC to the exponent byte.
"""

SIGN_MANTISSA = 0xf0
"""
Bit mask for the mantissa sign value in :data:`FAC_SIGN`.
"""

SIGN_EXPONENT = 0x0f 
"""
Bit mask for the exponent sign value in :data:`FAC_SIGN`.
"""

DEMO_ENTRY = 0xf000 
"""
Entry point for the demonstration program. 
"""

#==============================================================================
# FPU operations
#==============================================================================
FPU_ADD = 1
"""
Addition FPU opcode.
"""

FPU_SUB = 2
"""
Subtraction FPU opcode. 
"""

FPU_MUL = 3
"""
Multiplication FPU opcode. 
"""

FPU_DIV = 4
"""
Division FPU opcode. 
"""

FPU_EQ  = 5
"""
Equality FPU opcode. 
"""

FPU_NE  = 6 
"""
Not equality FPU opcode. 
"""

FPU_GT  = 7 
"""
Greater than FPU opcode. 
"""

FPU_GE  = 8 
"""
Greater than or equals FPU opcode. 
"""

FPU_LT  = 9 
"""
Less than FPU opcode. 
"""

FPU_LE  = 10  
""" 
Less than or equals FPU opcode. 
"""

#==============================================================================
# Error codes
#==============================================================================
ERR_STRING_TOO_LONG = 1
"""
String input exceeded the length of a page. 
"""

ERR_FPU_UNKNOWN = 2 
"""
Unexpected FPU error as a result of an underlying exception.
"""

ERR_FPU_INVALID_COMMAND = 3
"""
Invalid FPU opcode. 
"""

ERR_FPU_DIVISION_BY_ZERO = 4
"""
Only Chuck Norris can divide by zero.
"""

ERR_PROGRAM_INCOMPLETE = 5
"""
YAP program invoked without ending with a ``DONE()`` command. 
"""

#==============================================================================
# Values 
#==============================================================================
FPU_OK = 1
"""
Result of FPU operation was successful.
"""

SIZEOF_FAC = 6
"""
Size, in bytes, of a floating point accumulator. 
"""

CHR_LINE_FEED   = 0x0a
"""
Line feed character
"""
