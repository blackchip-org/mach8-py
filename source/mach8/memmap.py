#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: memmap.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Zero page
#------------------------------------------------------------------------------
ZP_ZERO = 0x00
"""
``$00``: Reserved
"""

R1 = 0x01
"""
``$01``: General register 1
"""

R2 = 0x02
"""
``$02``: General register 2
"""

R3 = 0x03
"""
``$03``: General register 3
"""

R4 = 0x04
"""
``$04``: General register 4
"""

R5 = 0x05
"""
``$05``: General register 5
"""

R6 = 0x06
"""
``$06``: General register 6
"""

KA = 0x0a
"""
``$0a``: Kernel register A
"""

KB = 0x0b
"""
``$0b``: Kernel register B
"""

KC = 0x0c
"""
``$0c``: Kernel register C
"""

KD = 0x0d
"""
``$0d``: Kernel register D
"""

KE = 0x0e
"""
``$0e``: Kernel register E
"""

KF = 0x0f
"""
``$0f``: Kernel register F
"""

FAC0_SIGN = 0x20
"""
``$20``: Floating point accumulator 0 signs. High nibble is mantissa sign, 
low nibble is exponent sign. $0 = positive, $F = negative. 
"""

FAC0_MANTISSA = 0x21
"""
``$21 - $24``: Floating point accumulator 0 mantissa, 4 bytes, BCD. 
"""

FAC0_EXPONENT = 0x25
"""
``$25``: Floating point accumulator 0 exponent, BCD. 
"""

FAC1_SIGN = 0x26
"""
``$26``: Floating point accumulator 1 signs. High nibble is mantissa sign, 
low nibble is exponent sign. $0 = positive, $F = negative. 
"""

FAC1_MANTISSA = 0x27
"""
``$27 - $2a``: Floating point accumulator 1 mantissa, 4 bytes, BCD.
"""

FAC1_EXPONENT = 0x2b
"""
``$2b``: Floating point accumulator 0 exponent, BCD.
"""

FAC_PTR = 0x2c
"""
``$2c``: Pointer to active floating point accumulator.
"""

FPU_COMMAND = 0x2d
"""
``$2d``: Command to send to the FPU.
"""

FPU_STATUS = 0x2e
"""
``$2e``: Status of last FPU operation.
"""

ERRNO = 0x2f
"""
``$2f``: Error number of last general operation. 
"""

TERM_STATUS = 0x30
"""
``$30``: Terminal status bits (TERM_TX_READY, TERM_RX_READY, TERM_RX_REQUEST) 
"""

TERM_INPUT = 0x31
"""
``$31``: Character received from terminal. 
"""

TERM_OUTPUT  = 0x32
"""
``$32``: Character to send to terminal. 
"""

TEXT_WORK_PTR = 0x33
"""
``$33 - $34``: Pointer used for the text work area. 
"""

HEAP_PTR = 0x35
"""
``$35 - $36``: Pointer to next free area in heap. 
"""

#------------------------------------------------------------------------------
# Scratch memory 
#------------------------------------------------------------------------------

STACK_PAGE = 0x100
"""
``$0100 - $01ff``: Processor stack
"""

TERM_INPUT_BUFFER = 0x200 
"""
``$0200 - $02ff``
"""

TEXT_WORK = 0x300
"""
``$0300 - $03ff``
"""

#------------------------------------------------------------------------------
# Code/Runtime space
#------------------------------------------------------------------------------
ROM_START = 0x0600
"""
``$0600``: ROM assembly starts here.  
"""

PROGRAM_START = 0x2000
"""
``$2000``: Space provided for general programs.
"""

HEAP = 0xfeff
"""
$FEFF: Heap starts here and grows downward.
"""
#------------------------------------------------------------------------------
# Vectors / Jumps
#------------------------------------------------------------------------------
ISTART = 0xff00
"""
``$ff00 - $ff02``: Indirect start jump. 
"""

YAP_EXIT_VECTOR = 0xff03
"""
``$ff03 - $ff04``
"""

YAP_ABORT_VECTOR = 0xff05
"""
``$ff05 - $ff06``
"""
 
NMI_VECTOR = 0xfffa
"""
``$fffa - $fffb``: Non-maskable interrupt vector
"""

RESET_VECTOR = 0xfffc
"""
``$fffc - $fffd``: CPU reset vector
"""

IRQ_VECTOR = 0xfffe
"""
``$fffe - $ffff``: Interrupt request vector
"""
