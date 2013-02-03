#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: instructions.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
from mach8 import (addressing as am, operations as op, executors as exe, 
                   x6502) 

__all__ = [ 
    'adc_imm', 'adc_zp',  'adc_zpx', 'adc_abs', 'adc_abx', 'adc_aby', 
    'adc_izx', 'adc_izy',
    'and_imm', 'and_zp',  'and_zpx', 'and_abs', 'and_abx', 'and_aby', 
    'and_izx', 'and_izy',
    'asl_acc', 'asl_zp',  'asl_zpx', 'asl_abs', 'asl_abx', 
    'bit_zp',  'bit_zpx', 'bit_abs', 'bit_abx',
    'brk', 
    # Branches
    'bpl',     'bmi',     'bvc',     'bvs',     'bcc',     'bcs',     
    'bne',     'beq',     'bra',
    'cmp_imm', 'cmp_zp',  'cmp_zpx', 'cmp_abs', 'cmp_abx', 'cmp_aby', 
    'cmp_izx', 'cmp_izy', 
    'cpx_imm', 'cpx_zp',  'cpx_abs', 
    'cpy_imm', 'cpy_zp',  'cpy_abs', 
    'dec_zp',  'dec_zpx', 'dec_abs', 'dec_abx',
    'eor_imm', 'eor_zp',  'eor_zpx', 'eor_abs', 'eor_abx', 'eor_aby', 
    'eor_izx', 'eor_izy',
    # Flags
    'clc',     'sec',     'cli',     'sei',     'clv',     'cld',     'sed', 
    'inc_zp',  'inc_zpx', 'inc_abs', 'inc_abx',
    'nop', 
    'jmp_abs', 'jmp_ind',
    'jsr',
    'lda_imm', 'lda_zp',  'lda_zpx', 'lda_abs', 'lda_abx', 'lda_aby', 
    'lda_izx', 'lda_izy',
    'ldx_imm', 'ldx_zp',  'ldx_zpy', 'ldx_abs', 'ldx_aby', 
    'ldy_imm', 'ldy_zp',  'ldy_zpx', 'ldy_abs', 'ldy_abx', 
    'lsr_acc', 'lsr_zp',  'lsr_zpx', 'lsr_abs', 'lsr_abx',  
    'ora_imm', 'ora_zp',  'ora_zpx', 'ora_abs', 'ora_abx', 'ora_aby', 
    'ora_izx', 'ora_izy',
    # Register 
    'tax',     'txa',     'dex',     'inx',     'tay',     'tya',     
    'dey',     'iny', 
    'rol_acc', 'rol_zp',  'rol_zpx', 'rol_abs', 'rol_abx', 
    'ror_acc', 'ror_zp',  'ror_zpx', 'ror_abs', 'ror_abx', 
    'rts',
    'sbc_imm', 'sbc_zp',  'sbc_zpx', 'sbc_abs', 'sbc_abx', 'sbc_aby', 
    'sbc_izx', 'sbc_izy',
    'sta_zp',  'sta_zpx', 'sta_abs', 'sta_abx', 'sta_aby', 'sta_izx', 
    'sta_izy', 
    # Stack Instructions
    'txs',     'tsx',     'pha',     'pla',     'php',    'plp',
    'phx',     'phy',     'plx',     'ply', 
    'stx_zp',  'stx_zpy', 'stx_abs',
    'sty_zp',  'sty_zpx', 'sty_abs',  
    'stz_zp',  'stz_zpx', 'stz_abs', 'stz_abx',
]

adc_imm = x6502.Instruction(0x69, op.ADC, am.IMM, exe.add) 
adc_zp  = x6502.Instruction(0x65, op.ADC, am.ZP,  exe.add) 
adc_zpx = x6502.Instruction(0x75, op.ADC, am.ZPX, exe.add) 
adc_abs = x6502.Instruction(0x6d, op.ADC, am.ABS, exe.add) 
adc_abx = x6502.Instruction(0x7d, op.ADC, am.ABX, exe.add) 
adc_aby = x6502.Instruction(0x79, op.ADC, am.ABY, exe.add) 
adc_izx = x6502.Instruction(0x61, op.ADC, am.IZX, exe.add) 
adc_izy = x6502.Instruction(0x71, op.ADC, am.IZY, exe.add) 

and_imm = x6502.Instruction(0x29, op.AND, am.IMM, exe.bit_op) 
and_zp  = x6502.Instruction(0x25, op.AND, am.ZP,  exe.bit_op) 
and_zpx = x6502.Instruction(0x35, op.AND, am.ZPX, exe.bit_op) 
and_abs = x6502.Instruction(0x2d, op.AND, am.ABS, exe.bit_op) 
and_abx = x6502.Instruction(0x3d, op.AND, am.ABX, exe.bit_op) 
and_aby = x6502.Instruction(0x39, op.AND, am.ABY, exe.bit_op) 
and_izx = x6502.Instruction(0x21, op.AND, am.IZX, exe.bit_op) 
and_izy = x6502.Instruction(0x31, op.AND, am.IZY, exe.bit_op) 

asl_acc = x6502.Instruction(0x0a, op.ASL, am.ACC, exe.shift) 
asl_zp  = x6502.Instruction(0x06, op.ASL, am.ZP,  exe.shift) 
asl_zpx = x6502.Instruction(0x16, op.ASL, am.ZPX, exe.shift) 
asl_abs = x6502.Instruction(0x0e, op.ASL, am.ABS, exe.shift) 
asl_abx = x6502.Instruction(0x1e, op.ASL, am.ABX, exe.shift) 

bit_zp  = x6502.Instruction(0x24, op.BIT, am.ZP,  exe.bit) 
bit_zpx = x6502.Instruction(0x34, op.BIT, am.ZPX, exe.bit)
bit_abs = x6502.Instruction(0x2c, op.BIT, am.ABS, exe.bit)
bit_abx = x6502.Instruction(0x3c, op.BIT, am.ABX, exe.bit) 

# Branches 
bpl     = x6502.Instruction(0x10, op.BPL, am.REL, exe.branch) 
bmi     = x6502.Instruction(0x30, op.BMI, am.REL, exe.branch) 
bvc     = x6502.Instruction(0x50, op.BVC, am.REL, exe.branch)
bvs     = x6502.Instruction(0x70, op.BVS, am.REL, exe.branch) 
bcc     = x6502.Instruction(0x90, op.BCC, am.REL, exe.branch) 
bcs     = x6502.Instruction(0xb0, op.BCS, am.REL, exe.branch) 
bne     = x6502.Instruction(0xd0, op.BNE, am.REL, exe.branch) 
beq     = x6502.Instruction(0xf0, op.BEQ, am.REL, exe.branch) 
bra     = x6502.Instruction(0x80, op.BRA, am.REL, exe.branch) 

brk     = x6502.Instruction(0x00, op.BRK, am.IMP, exe.brk) 

cmp_imm = x6502.Instruction(0xc9, op.CMP, am.IMM, exe.compare) 
cmp_zp  = x6502.Instruction(0xc5, op.CMP, am.ZP,  exe.compare) 
cmp_zpx = x6502.Instruction(0xd5, op.CMP, am.ZPX, exe.compare)
cmp_abs = x6502.Instruction(0xcd, op.CMP, am.ABS, exe.compare) 
cmp_abx = x6502.Instruction(0xdd, op.CMP, am.ABX, exe.compare) 
cmp_aby = x6502.Instruction(0xd9, op.CMP, am.ABY, exe.compare) 
cmp_izx = x6502.Instruction(0xc1, op.CMP, am.IZX, exe.compare) 
cmp_izy = x6502.Instruction(0xd1, op.CMP, am.IZY, exe.compare) 

cpx_imm = x6502.Instruction(0xe0, op.CPX, am.IMM, exe.compare) 
cpx_zp  = x6502.Instruction(0xe4, op.CPX, am.ZP,  exe.compare) 
cpx_abs = x6502.Instruction(0xec, op.CPX, am.ABS, exe.compare)

cpy_imm = x6502.Instruction(0xc0, op.CPY, am.IMM, exe.compare) 
cpy_zp  = x6502.Instruction(0xc4, op.CPY, am.ZP,  exe.compare) 
cpy_abs = x6502.Instruction(0xcc, op.CPY, am.ABS, exe.compare)

dec_zp  = x6502.Instruction(0xc6, op.DEC, am.ZP,  exe.one_memory) 
dec_zpx = x6502.Instruction(0xd6, op.DEC, am.ZPX, exe.one_memory) 
dec_abs = x6502.Instruction(0xce, op.DEC, am.ABS, exe.one_memory) 
dec_abx = x6502.Instruction(0xde, op.DEC, am.ABX, exe.one_memory) 

eor_imm = x6502.Instruction(0x49, op.EOR, am.IMM, exe.bit_op) 
eor_zp  = x6502.Instruction(0x45, op.EOR, am.ZP,  exe.bit_op) 
eor_zpx = x6502.Instruction(0x55, op.EOR, am.ZPX, exe.bit_op) 
eor_abs = x6502.Instruction(0x4d, op.EOR, am.ABS, exe.bit_op) 
eor_abx = x6502.Instruction(0x5d, op.EOR, am.ABX, exe.bit_op) 
eor_aby = x6502.Instruction(0x59, op.EOR, am.ABY, exe.bit_op) 
eor_izx = x6502.Instruction(0x41, op.EOR, am.IZX, exe.bit_op) 
eor_izy = x6502.Instruction(0x51, op.EOR, am.IZY, exe.bit_op) 

# Flags
clc     = x6502.Instruction(0x18, op.CLC, am.IMP, exe.flags) 
sec     = x6502.Instruction(0x38, op.SEC, am.IMP, exe.flags) 
cli     = x6502.Instruction(0x58, op.CLI, am.IMP, exe.flags) 
sei     = x6502.Instruction(0x78, op.SEI, am.IMP, exe.flags) 
clv     = x6502.Instruction(0xb8, op.CLV, am.IMP, exe.flags) 
cld     = x6502.Instruction(0xd8, op.CLD, am.IMP, exe.flags) 
sed     = x6502.Instruction(0xf8, op.SED, am.IMP, exe.flags) 

inc_zp  = x6502.Instruction(0xe6, op.INC, am.ZP,  exe.one_memory) 
inc_zpx = x6502.Instruction(0xf6, op.INC, am.ZPX, exe.one_memory) 
inc_abs = x6502.Instruction(0xee, op.INC, am.ABS, exe.one_memory) 
inc_abx = x6502.Instruction(0xfe, op.INC, am.ABX, exe.one_memory) 

jmp_abs = x6502.Instruction(0x4c, op.JMP, am.ABS, exe.jump) 
jmp_ind = x6502.Instruction(0x6c, op.JMP, am.IND, exe.jump) 

jsr     = x6502.Instruction(0x20, op.JSR, am.ABS, exe.jump_subroutine)

lda_imm = x6502.Instruction(0xa9, op.LDA, am.IMM, exe.load)
lda_zp  = x6502.Instruction(0xa5, op.LDA, am.ZP,  exe.load) 
lda_zpx = x6502.Instruction(0xb5, op.LDA, am.ZPX, exe.load) 
lda_abs = x6502.Instruction(0xad, op.LDA, am.ABS, exe.load) 
lda_abx = x6502.Instruction(0xbd, op.LDA, am.ABX, exe.load) 
lda_aby = x6502.Instruction(0xb9, op.LDA, am.ABY, exe.load) 
lda_izx = x6502.Instruction(0xa1, op.LDA, am.IZX, exe.load) 
lda_izy = x6502.Instruction(0xb1, op.LDA, am.IZY, exe.load) 

ldx_imm = x6502.Instruction(0xa2, op.LDX, am.IMM, exe.load)
ldx_zp  = x6502.Instruction(0xa6, op.LDX, am.ZP,  exe.load) 
ldx_zpy = x6502.Instruction(0xb6, op.LDX, am.ZPY, exe.load) 
ldx_abs = x6502.Instruction(0xae, op.LDX, am.ABS, exe.load) 
ldx_aby = x6502.Instruction(0xbe, op.LDX, am.ABY, exe.load) 

ldy_imm = x6502.Instruction(0xa0, op.LDY, am.IMM, exe.load)
ldy_zp  = x6502.Instruction(0xa4, op.LDY, am.ZP,  exe.load) 
ldy_zpx = x6502.Instruction(0xb4, op.LDY, am.ZPX, exe.load) 
ldy_abs = x6502.Instruction(0xac, op.LDY, am.ABS, exe.load) 
ldy_abx = x6502.Instruction(0xbc, op.LDY, am.ABX, exe.load) 

lsr_acc = x6502.Instruction(0x4a, op.LSR, am.ACC, exe.shift) 
lsr_zp  = x6502.Instruction(0x46, op.LSR, am.ZP,  exe.shift) 
lsr_zpx = x6502.Instruction(0x56, op.LSR, am.ZPX, exe.shift)
lsr_abs = x6502.Instruction(0x4e, op.LSR, am.ABS, exe.shift) 
lsr_abx = x6502.Instruction(0x5e, op.LSR, am.ABX, exe.shift) 

nop     = x6502.Instruction(0xea, op.NOP, am.IMP, exe.nop)

ora_imm = x6502.Instruction(0x09, op.ORA, am.IMM, exe.bit_op) 
ora_zp  = x6502.Instruction(0x05, op.ORA, am.ZP,  exe.bit_op) 
ora_zpx = x6502.Instruction(0x15, op.ORA, am.ZPX, exe.bit_op) 
ora_abs = x6502.Instruction(0x0d, op.ORA, am.ABS, exe.bit_op) 
ora_abx = x6502.Instruction(0x1d, op.ORA, am.ABX, exe.bit_op) 
ora_aby = x6502.Instruction(0x19, op.ORA, am.ABY, exe.bit_op) 
ora_izx = x6502.Instruction(0x01, op.ORA, am.IZX, exe.bit_op) 
ora_izy = x6502.Instruction(0x11, op.ORA, am.IZY, exe.bit_op)

# Register Instructions
tax     = x6502.Instruction(0xaa, op.TAX, am.IMP, exe.transfer) 
txa     = x6502.Instruction(0x8a, op.TXA, am.IMP, exe.transfer) 
dex     = x6502.Instruction(0xca, op.DEX, am.IMP, exe.one_register) 
inx     = x6502.Instruction(0xe8, op.INX, am.IMP, exe.one_register) 
tay     = x6502.Instruction(0xa8, op.TAY, am.IMP, exe.transfer) 
tya     = x6502.Instruction(0x98, op.TYA, am.IMP, exe.transfer)
dey     = x6502.Instruction(0x88, op.DEY, am.IMP, exe.one_register) 
iny     = x6502.Instruction(0xc8, op.INY, am.IMP, exe.one_register) 

rol_acc = x6502.Instruction(0x2a, op.ROL, am.ACC, exe.shift) 
rol_zp  = x6502.Instruction(0x26, op.ROL, am.ZP,  exe.shift) 
rol_zpx = x6502.Instruction(0x36, op.ROL, am.ZPX, exe.shift)
rol_abs = x6502.Instruction(0x2e, op.ROL, am.ABS, exe.shift) 
rol_abx = x6502.Instruction(0x3e, op.ROL, am.ABX, exe.shift) 

ror_acc = x6502.Instruction(0x6a, op.ROR, am.ACC, exe.shift) 
ror_zp  = x6502.Instruction(0x66, op.ROR, am.ZP,  exe.shift) 
ror_zpx = x6502.Instruction(0x76, op.ROR, am.ZPX, exe.shift) 
ror_abs = x6502.Instruction(0x6e, op.ROR, am.ABS, exe.shift) 
ror_abx = x6502.Instruction(0x7e, op.ROR, am.ABX, exe.shift) 

rts     = x6502.Instruction(0x60, op.RTS, am.IMP, exe.return_subroutine) 

sbc_imm = x6502.Instruction(0xe9, op.SBC, am.IMM, exe.sub) 
sbc_zp  = x6502.Instruction(0xe5, op.SBC, am.ZP,  exe.sub)
sbc_zpx = x6502.Instruction(0xf5, op.SBC, am.ZPX, exe.sub) 
sbc_abs = x6502.Instruction(0xed, op.SBC, am.ABS, exe.sub) 
sbc_abx = x6502.Instruction(0xfd, op.SBC, am.ABX, exe.sub) 
sbc_aby = x6502.Instruction(0xf9, op.SBC, am.ABY, exe.sub) 
sbc_izx = x6502.Instruction(0xe1, op.SBC, am.IZX, exe.sub) 
sbc_izy = x6502.Instruction(0xf1, op.SBC, am.IZY, exe.sub)

sta_zp  = x6502.Instruction(0x85, op.STA, am.ZP,  exe.store) 
sta_zpx = x6502.Instruction(0x95, op.STA, am.ZPX, exe.store) 
sta_abs = x6502.Instruction(0x8d, op.STA, am.ABS, exe.store) 
sta_abx = x6502.Instruction(0x9d, op.STA, am.ABX, exe.store) 
sta_aby = x6502.Instruction(0x99, op.STA, am.ABY, exe.store) 
sta_izx = x6502.Instruction(0x81, op.STA, am.IZX, exe.store) 
sta_izy = x6502.Instruction(0x91, op.STA, am.IZY, exe.store) 

# Stack Instructions
txs     = x6502.Instruction(0x9a, op.TXS, am.IMP, exe.stack)
tsx     = x6502.Instruction(0xba, op.TSX, am.IMP, exe.stack) 
pha     = x6502.Instruction(0x48, op.PHA, am.IMP, exe.stack)
pla     = x6502.Instruction(0x68, op.PLA, am.IMP, exe.stack)
php     = x6502.Instruction(0x08, op.PHP, am.IMP, exe.stack) 
plp     = x6502.Instruction(0x28, op.PLP, am.IMP, exe.stack) 
phx     = x6502.Instruction(0xda, op.PHX, am.IMP, exe.stack)
phy     = x6502.Instruction(0x5a, op.PHY, am.IMP, exe.stack) 
plx     = x6502.Instruction(0xfa, op.PLX, am.IMP, exe.stack) 
ply     = x6502.Instruction(0x7a, op.PLY, am.IMP, exe.stack) 

stx_zp  = x6502.Instruction(0x86, op.STX, am.ZP,  exe.store) 
stx_zpy = x6502.Instruction(0x96, op.STX, am.ZPY, exe.store) 
stx_abs = x6502.Instruction(0x8e, op.STX, am.ABS, exe.store) 

sty_zp  = x6502.Instruction(0x84, op.STY, am.ZP,  exe.store) 
sty_zpx = x6502.Instruction(0x94, op.STY, am.ZPX, exe.store) 
sty_abs = x6502.Instruction(0x8c, op.STY, am.ABS, exe.store) 

stz_zp  = x6502.Instruction(0x64, op.STZ, am.ZP,  exe.store) 
stz_zpx = x6502.Instruction(0x74, op.STZ, am.ZPX, exe.store) 
stz_abs = x6502.Instruction(0x9c, op.STZ, am.ABS, exe.store) 
stz_abx = x6502.Instruction(0x93, op.STZ, am.ABX, exe.store) 




