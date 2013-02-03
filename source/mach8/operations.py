#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: operations.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
"""
Most of the documentation in this module is provided by http://6502.org and 
reprinted here with permission. Written by John Pickens and Bruce Clark. 
Adaptations and portions modified where relevant.
"""

__all__ = ['ADC', 'AND', 'ASL', 'BCC', 'BCS', 'BEQ', 'BIT', 'BMI', 'BNE', 
           'BPL', 'BRA', 'BRK', 'BVC', 'BVS', 'CLC', 'CLI', 'CLV', 'CLD', 
           'CMP', 'CPX', 'CPY', 'DEC', 'DEX', 'DEY', 'EOR', 'INC', 'INX', 
           'INY', 'JMP', 'JSR', 'LDA', 'LDX', 'LDY', 'LSR', 'NOP', 'ORA', 
           'PHA', 'PHP', 'PHX', 'PHY', 'PLA', 'PLP', 'PLX', 'PLY', 'ROL', 
           'ROR', 'RTI', 'RTS', 'SBC', 'SEC', 'SED', 'SEI', 'STA', 'STX', 
           'STY', 'STZ', 'TAX', 'TAY', 'TSX', 'TXA', 'TXS', 'TYA']

ADC = 'adc'
"""
Add with carry. 

=============== =============== ======= 
Addressing Mode Syntax          Opcode 
=============== =============== =======
Immediate       ``ADC #$44``    ``$69``    
Zero Page       ``ADC $44``     ``$65``    
Zero Page,X     ``ADC $44,X``   ``$75``    
Absolute        ``ADC $4400``   ``$6D``    
Absolute,X      ``ADC $4400,X`` ``$7D``    
Absolute,Y      ``ADC $4400,Y`` ``$79``    
Indirect,X      ``ADC ($44,X)`` ``$61``    
Indirect,Y      ``ADC ($44),Y`` ``$71``    
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.v`, 
:attr:`~mach8.x6502.CPU.z`, :attr:`~mach8.x6502.CPU.c`

Results are dependent on the setting of the decimal flag. In
decimal mode, addition is carried out on the assumption that the
values involved are packed BCD (Binary Coded Decimal).

There is no way to add without carry. See the notes for the
:attr:`~mach8.x6502.CPU.c` flag. When starting addition, always clear the carry 
first with a :data:`CLC` instruction.
"""

AND = 'and'
"""
Bitwise *AND* with accumulator.

=============== =============== ======
Addressing Mode Syntax          Opcode
=============== =============== ======
Immediate       ``AND #$44``    ``$29``
Zero Page       ``AND $44``     ``$25``
Zero Page,X     ``AND $44,X``   ``$35``
Absolute        ``AND $4400``   ``$2D``
Absolute,X      ``AND $4400,X`` ``$3D``
Absolute,Y      ``AND $4400,Y`` ``$39``
Indirect,X      ``AND ($44,X)`` ``$21``
Indirect,Y      ``AND ($44),Y`` ``$31``
=============== =============== ======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`
"""

ASL = 'asl'
"""
Arithimetic shift left.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Accumulator     ``ASL A``       ``$0A``
Zero Page       ``ASL $44``     ``$06``
Zero Page,X     ``ASL $44,X``   ``$16``
Absolute        ``ASL $4400``   ``$0E``
Absolute,X      ``ASL $4400,X`` ``$1E``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z` 
:attr:`~mach8.x6502.CPU.c`

Shifts all bits left one position. 0 is shifted into bit 0 and the
original bit 7 is shifted into the carry.
"""

BCC = 'bcc'
"""
Branch on carry (:attr:`~mach8.x6502.CPU.c`) clear. Opcode ``$90``.
"""

BCS = 'bcs'
"""
Branch on carry (:attr:`~mach8.x6502.CPU.c`) set. Opcode ``$B0``.
"""

BEQ = 'beq'
"""
Branch on equals (:attr:`~mach8.x6502.CPU.z` set). Opcode ``$F0``.
"""

BIT = 'bit'
"""
Test bits.

================== =============== =======
Addressing Mode    Syntax          Opcode
================== =============== =======
Zero Page          ``BIT $44``     ``$24``
Zero Page,X [#f1]_ ``BIT $44,X``   ``$34``
Absolute           ``BIT $4400``   ``$2C``
Absolute,X  [#f1]_ ``BIT $4400,X`` ``$3C``
================== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.v`, 
:attr:`~mach8.x6502.CPU.z`

Sets the Z flag as though the value in the address tested were
*and*\-ed with the accumulator. The N and V flags are set to match bits 7
and 6 respectively in the value stored at the tested address.

This instruction can also be useful for skipping over bytes. See
the :func:`skip2` macro for more information.
"""

BMI = 'bmi'
"""
Branch on minus (:attr:`~mach8.x6502.CPU.n` set). Opcode ``$30``.
"""

BNE = 'bne'
"""
Branch on not equals (:attr:`~mach8.x6502.CPU.z` clear). Opcode ``$D0``.
"""

BPL = 'bpl'
"""
Branch on plus (:attr:`~mach8.x6502.CPU.n` clear). Opcode ``$10``.
"""

BRA = 'bra'
"""
Branch always [#f1]_. If the target is within the range of a branch,
saves one byte over using a :data:`jmp` instruction. Opcode
``$80``.
"""

BRK = 'brk'
"""
In the Mach-8, this sets the :data:`B` flag, increments the program
counter by one, and causes the CPU to stop. If execution should be
resumed after the break instruction (during debugging), add a
:data:`nop` after the break. Opcode ``$00``.
"""

BVC = 'bvc'
"""
Branch on overflow (:attr:`~mach8.x6502.CPU.v`) clear. Opcode ``$50``.
"""

BVS = 'bvs'
"""
Branch on overflow (:attr:`~mach8.x6502.CPU.v`) set. Opcode ``$70``.
"""

CLC = 'clc'
"""
Clear carry (:attr:`~mach8.x6502.CPU.c`) flag. Opcode ``$18``.
"""

CLI = 'cli'
"""
Clear interrupt disable (:attr:`~mach8.x6502.CPU.i`) flag. Opcode ``$58``.
"""

CLV = 'clv'
"""
Clear overflow (:attr:`~mach8.x6502.CPU.v`) flag. There is no instruction to 
set the overflow but a :data:`bit` test on an :data:`RTS` instruction will
do the trick. Opcode ``$B8``.
"""

CLD = 'cld'
"""
Clear decimal (:attr:`~mach8.x6502.CPU.d`) flag. Opcode ``$D8``.
"""

CMP = 'cmp'
"""
Compare :attr:`~mach8.x6502.CPU.a` register.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``CMP #$44``    ``$C9``
Zero Page       ``CMP $44``     ``$C5``
Zero Page,X     ``CMP $44,X``   ``$D5``
Absolute        ``CMP $4400``   ``$CD``
Absolute,X      ``CMP $4400,X`` ``$DD``
Absolute,Y      ``CMP $4400,Y`` ``$D9``
Indirect,X      ``CMP ($44,X)`` ``$C1``
Indirect,Y      ``CMP ($44),Y`` ``$D1``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`, 
:attr:`~mach8.x6502.CPU.c`

Compare sets flags as if a subtraction had been carried out. If the
value in the accumulator is equal or greater than the compared
value, the carry will be set. The equal (:attr:`~mach8.x6502.CPU.z`) and sign
(:attr:`~mach8.x6502.CPU.n`) flags will be set based on equality or lack thereof and
the sign (i.e. :attr:`~mach8.x6502.CPU.a` >= ``$80``) of the accumulator.
"""

CPX = 'cpx'
"""
Compare :attr:`~mach8.x6502.CPU.x` register.

=============== ============= =======
Addressing Mode Syntax        Opcode
=============== ============= =======
Immediate       ``CPX #$44``  ``$E0``
Zero Page       ``CPX $44``   ``$E4``
Absolute        ``CPX $4400`` ``$EC``
=============== ============= =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`, 
:attr:`~mach8.x6502.CPU.c`

Operation and flag results are identical to :data:`CMP`.
"""

CPY = 'cpy' 
"""
Compare :attr:`~mach8.x6502.CPU.y` register.

=============== ============= =======
Addressing Mode Syntax        Opcode
=============== ============= =======
Immediate       ``CPY #$44``  ``$C0``
Zero Page       ``CPY $44``   ``$C4``
Absolute        ``CPY $4400`` ``$CC``
=============== ============= =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`, :attr:`~mach8.x6502.CPU.c`

Operation and flag results are identical to :data:`CMP`.
"""

DEC = 'dec' 
"""
Decrement memory.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Zero Page       ``DEC $44``     ``$C6``
Zero Page,X     ``DEC $44,X``   ``$D6``
Absolute        ``DEC $4400``   ``$CE``
Absolute,X      ``DEC $4400,X`` ``$DE``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`
"""

DEX = 'dex'
"""
Decrement :attr:`~mach8.x6502.CPU.x` register. Affects flags: 
:attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. Opcode ``$CA``.
"""

DEY = 'dey'
"""
Decrement :attr:`~mach8.x6502.CPU.y` register. Affects flags: 
:attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. Opcode ``$88``.
"""

EOR = 'eor'
"""
Bitwise exclusive *OR*.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``EOR #$44``    ``$49``
Zero Page       ``EOR $44``     ``$45``
Zero Page,X     ``EOR $44,X``   ``$55``
Absolute        ``EOR $4400``   ``$4D``
Absolute,X      ``EOR $4400,X`` ``$5D``
Absolute,Y      ``EOR $4400,Y`` ``$59``
Indirect,X      ``EOR ($44,X)`` ``$41``
Indirect,Y      ``EOR ($44),Y`` ``$51``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`
"""

INC = 'inc'
"""
Increment memory.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Zero Page       ``INC $44``     ``$E6``
Zero Page,X     ``INC $44,X``   ``$F6``
Absolute        ``INC $4400``   ``$EE``
Absolute,X      ``INC $4400,X`` ``$FE``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`
"""

INX = 'inx'
"""
Increment :attr:`~mach8.x6502.CPU.x` register. Affects flags: 
:attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. Opcode ``$E8``.
"""

INY = 'iny'
"""
Increment :attr:`~mach8.x6502.CPU.y` register. Affects flags: 
:attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. Opcode ``$C8``.
"""

JMP = 'jmp'
"""
Jump.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Absolute        ``JMP $5597``   ``$4C``
Indirect        ``JMP ($5597)`` ``$6C``
=============== =============== =======

Transfers program execution to the following address (absolute) or
to the location contained in the following address (indirect).
"""
 
JSR = 'jsr'
"""
Jump to subroutine.

Pushes the ``address - 1`` of the next operation on to the stack
before transferring program control to the following
address. Subroutines are normally terminated by a RTS
opcode. Opcode ``$20``.
"""

LDA = 'lda'
"""
Load :attr:`~mach8.x6502.CPU.a` register.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``LDA #$44``    ``$A9``
Zero Page       ``LDA $44``     ``$A5``
Zero Page,X     ``LDA $44,X``   ``$B5``
Absolute        ``LDA $4400``   ``$AD``
Absolute,X      ``LDA $4400,X`` ``$BD``
Absolute,Y      ``LDA $4400,Y`` ``$B9``
Indirect,X      ``LDA ($44,X)`` ``$A1``
Indirect,Y      ``LDA ($44),Y`` ``$B1``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`.
"""

LDX = 'ldx'
"""
Load :attr:`~mach8.x6502.CPU.x` register.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``LDX #$44``    ``$A2``
Zero Page       ``LDX $44``     ``$A6``
Zero Page,Y     ``LDX $44,Y``   ``$B6``
Absolute        ``LDX $4400``   ``$AE``
Absolute,Y      ``LDX $4400,Y`` ``$BE``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`.
"""

LDY = 'ldy'
"""
Load :attr:`~mach8.x6502.CPU.y` register.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``LDY #$44``    ``$A0``
Zero Page       ``LDY $44``     ``$A4``
Zero Page,X     ``LDY $44,X``   ``$B4``
Absolute        ``LDY $4400``   ``$AC``
Absolute,X      ``LDY $4400,X`` ``$BC``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`.
"""

LSR = 'lsr'
"""
Logical shift left.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Accumulator     ``LSR A``       ``$4A``
Zero Page       ``LSR $44``     ``$46``
Zero Page,X     ``LSR $44,X``   ``$56``
Absolute        ``LSR $4400``   ``$4E``
Absolute,X      ``LSR $4400,X`` ``$5E``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`, 
:attr:`~mach8.x6502.CPU.c`

Shifts all bits right one position. 0 is shifted into bit 7 and the
original bit 0 is shifted into the carry.
"""

NOP = 'nop'
"""
No operation. Opcode ``$EA``.
"""

ORA = 'ora' 
"""
Bitwise *OR* with register :attr:`~mach8.x6502.CPU.a`.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``ORA #$44``    ``$09``
Zero Page       ``ORA $44``     ``$05``
Zero Page,X     ``ORA $44,X``   ``$15``
Absolute        ``ORA $4400``   ``$0D``
Absolute,X      ``ORA $4400,X`` ``$1D``
Absolute,Y      ``ORA $4400,Y`` ``$19``
Indirect,X      ``ORA ($44,X)`` ``$01``
Indirect,Y      ``ORA ($44),Y`` ``$11``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`
"""

PHA = 'pha'
"""
Push register :attr:`~mach8.x6502.CPU.a` to the stack. Opcode ``$48``.
"""

PHP = 'php'
"""
Push status register (:attr:`~mach8.x6502.CPU.sr`) to the stack. Opcode ``$08``.
"""

PHX = 'phx'
"""
Pull top of the stack into register :attr:`~mach8.x6502.CPU.x`. [#f1]_ 
Opcode ``$FA``.
"""

PHY = 'phy'
"""
Pull top of the stack into register :attr:`~mach8.x6502.CPU.y`. [#f1]_ 
Opcode ``$7A``.
"""
  
PLA = 'pla'
"""
Pull top of the stack into register :attr:`~mach8.x6502.CPU.a`. [#f1]_ 
Opcode ``$68``.
"""

PLP = 'plp'
"""
Pull top of the stack into the status register (:attr:`~mach8.x6502.CPU.sr`). 
Opcode ``$28``.
"""

PLX = 'plx'
"""
Pull top of the stack into register :attr:`~mach8.x6502.CPU.x`. [#f1]_ 
Opcode ``$FA``.
"""

PLY = 'ply' 
"""
Pull top of the stack into register :attr:`~mach8.x6502.CPU.y`. [#f1]_ 
Opcode ``$7A``.
"""

ROL = 'rol'
"""
Rotate left.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Accumulator     ``ROL A``       ``$2A``
Zero Page       ``ROL $44``     ``$26``
Zero Page,X     ``ROL $44,X``   ``$36``
Absolute        ``ROL $4400``   ``$2E``
Absolute,X      ``ROL $4400,X`` ``$3E``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`, 
:attr:`~mach8.x6502.CPU.c`

Shifts all bits left one position. The carry is shifted into bit 0
and the original bit 7 is shifted into the carry.
"""

ROR = 'ror' 
"""
Rotate right.

============== =============== =======
Addresing Mode Syntax          Opcode
============== =============== =======
Accumulator    ``ROR A``       ``$6A``
Zero Page      ``ROR $44``     ``$66``
Zero Page,X    ``ROR $44,X``   ``$76``
Absolute       ``ROR $4400``   ``$6E``
Absolute,X     ``ROR $4400,X`` ``$7E``
============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`, 
:attr:`~mach8.x6502.CPU.c`

Shifts all bits right one position. The carry is shifted into bit 7
and the original bit 0 is shifted into the carry.
"""

RTI = 'rti' 
"""
Return from interrupt.

In the Mach-8, this instruction is treated as an illegal operation. 
Opcode ``$40``.
"""

RTS = 'rts'
"""
Return from subroutine.

Pulls the top two bytes off the stack (low byte first) and transfers program 
control to that ``address + 1``. It is used, as expected, to exit a subroutine 
invoked via JSR which pushed the ``address - 1``. Opcode ``$60``.
"""

SBC = 'sbc'
"""
Subtract with carry.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Immediate       ``SBC #$44``    ``$E9``
Zero Page       ``SBC $44``     ``$E5``
Zero Page,X     ``SBC $44,X``   ``$F5``
Absolute        ``SBC $4400``   ``$ED``
Absolute,X      ``SBC $4400,X`` ``$FD``
Absolute,Y      ``SBC $4400,Y`` ``$F9``
Indirect,X      ``SBC ($44,X)`` ``$E1``
Indirect,Y      ``SBC ($44),Y`` ``$F1``
=============== =============== =======

Affects Flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.v`, 
:attr:`~mach8.x6502.CPU.z`, :attr:`~mach8.x6502.CPU.c`

SBC results are dependent on the setting of the decimal flag. In
decimal mode, subtraction is carried out on the assumption that the
values involved are packed BCD (Binary Coded Decimal).

There is no way to subtract without the carry which works as an
inverse borrow. See the notes for the :attr:`~mach8.x6502.CPU.c` flag. When 
starting subtraction, set the carry first with a :data:`SEC` instruction.
"""

SEC = 'sec'
"""
Set carry (:attr:`~mach8.x6502.CPU.c` flag). Opcode ``$38``.
"""

SED = 'sed'
"""
Set decimal (:attr:`~mach8.x6502.CPU.d` flag). Opcode ``$F8``.
"""

SEI = 'sei'
"""
Set interrupt disable (:attr:`~mach8.x6502.CPU.i` flag). Opcode ``$78``.
"""

STA = 'sta'
"""
Store register :attr:`~mach8.x6502.CPU.a` to memory.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Zero Page       ``STA $44``     ``$85``
Zero Page,X     ``STA $44,X``   ``$95``
Absolute        ``STA $4400``   ``$8D``
Absolute,X      ``STA $4400,X`` ``$9D``
Absolute,Y      ``STA $4400,Y`` ``$99``
Indirect,X      ``STA ($44,X)`` ``$81``
Indirect,Y      ``STA ($44),Y`` ``$91``
=============== =============== =======
"""

STX = 'stx'
"""
Store register :attr:`~mach8.x6502.CPU.x` to memory.

=============== ============= =======
Addressing Mode Syntax        Opcode
=============== ============= =======
Zero Page       ``STX $44``   ``$86``
Zero Page,Y     ``STX $44,Y`` ``$96``
Absolute        ``STX $4400`` ``$8E``
=============== ============= =======
"""

STY = 'sty'
"""
Store register :attr:`~mach8.x6502.CPU.y` to memory.

=============== ============= =======
Addressing Mode Syntax        Opcode
=============== ============= =======
Zero Page       ``STY $44``   ``$84``
Zero Page,X     ``STY $44,X`` ``$94``
Absolute        ``STY $4400`` ``$8C``
=============== ============= =======
"""

STZ = 'stz'
"""
Store zero to memory.

=============== =============== =======
Addressing Mode Syntax          Opcode
=============== =============== =======
Zero Page       ``STZ $44``     ``$64``
Zero Page,X     ``STZ $44,X``   ``$74``
Absolute        ``STZ $4400``   ``$9C``
Absolute,X      ``STZ $4400,X`` ``$9E``
=============== =============== =======
"""

TAX = 'tax'
"""
Transfer :attr:`~mach8.x6502.CPU.a` register to :attr:`~mach8.x6502.CPU.x`. 
Affects flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. 
Opcode ``$AA``.
"""

TAY = 'tay'
"""
Transfer :attr:`~mach8.x6502.CPU.a` register to :attr:`~mach8.x6502.CPU.y`. 
Affects flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. 
Opcode ``$A8``.
"""

TSX = 'tsx'
"""
Transfer the stack pointer (:data:`SP`) to register :attr:`~mach8.x6502.CPU.x`. 
Affects flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. 
Opcode ``$BA``.
"""

TXA = 'txa'
"""
Transfer :attr:`~mach8.x6502.CPU.x` register to :attr:`~mach8.x6502.CPU.a`. 
Affects flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. 
Opcode ``$8A``.
"""

TXS = 'txs'
"""
Transfer :attr:`~mach8.x6502.CPU.x` register to the stack pointer (:data:`SP`). 
Affects flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. 
Opcode ``$9A``.
"""

TYA = 'tya'
"""
Transfer :attr:`~mach8.x6502.CPU.y` register to :attr:`~mach8.x6502.CPU.a`. 
Affects flags: :attr:`~mach8.x6502.CPU.n`, :attr:`~mach8.x6502.CPU.z`. 
Opcode ``$98``.
"""

