#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011-2012, Reprint what you like.
#
# $Id: pally.py 134 2012-01-28 03:04:07Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import * 

def assemble(a):
    _;  a('pally')
    _;      a.remark    ('Store "quit" command in R3 for later reference')
    _;      a.macro     (ldxy_imm,  'pally.quit_command') 
    _;      a.macro     (stxy_zp,   'R3')    
    
    _;      a.remark    ('Welcome banner')
    _;      a(jsr,      'PRIMM')
    _;      a.data      ('Palindrome checker\nType "quit" to exit\n', 0)
    
    _;  a('pally.loop')
    _;      a.remark    ('Print prompt')
    _;      a(jsr,      'PRIMM')
    _;      a.data      ('> ', 0) 
    
    _;      a.remark    ('Read in string to check')
    _;      a(jsr,      'LINEIN')
    
    _;      a.remark    ('Store linein location to R1 and compare to "quit"')
    _;      a.macro     (stxy_zp,   'R1') 
    _;      a(jsr,      'STRCMP')
    
    _;      a.remark    ('If true, done')
    _;      a(beq,      'pally.exit')

    _;      a(jsr,      'is_pally')
    _;      a(beq,      'pally.print_true')

    _;      a(jsr,      'PRIMM')
    _;      a.data      ('False\n', 0)
    _;      a(bra,      'pally.loop')
    
    _;  a('pally.print_true')
    _;      a(jsr,      'PRIMM')
    _;      a.data      ('True\n', 0) 
    _;      a(bra,      'pally.loop')
    
    _;  a('pally.exit')
    _;      a(rts) 
    
    _;  a('pally.quit_command')
    _;      a.data      ('quit', 0) 
    
    _;  a('is_pally')
    _;      a.remark    ('Save registers')
    _;      a(phx)
    _;      a(phy)

    _;      a.remark    ('Store string address in R1 for IZY addressing')
    _;      a.macro     (stxy_zp, 'R1') 
    _;      a(ldy_imm,  0)
    
    _;  a('is_pally.strcpy')
    _;      a.remark    ('Copy string to TEXT_WORK and get length')
    _;      a(lda_izy,  'R1')

    _;      a.remark    ('String terminator?')
    _;      a(beq,      'is_pally.compare')

    _;      a.remark    ('Do copy')
    _;      a(sta_aby,  'TEXT_WORK')
    _;      a(iny)
    _;      a(bra,      'is_pally.strcpy')
    
    _;  a('is_pally.compare')
    _;      a.remark     ('X = index forward, Y = index backward')
    _;      a.remark     ('Y is at terminator, go back one')
    _;      a(dey)
    _;      a(ldx_imm,  0) 
 
    _;  a('is_pally.compare_loop')
    _;      a(lda_abx,  'TEXT_WORK')
    _;      a(cmp_aby,  'TEXT_WORK')
    _;      a(bne,      'is_pally.false')
    _;      a(inx)
    _;      a(dey)

    _;      a.remark    ('Done if underflow on Y')
    _;      a(cpy_imm,  0xff)
    _;      a(beq,      'is_pally.true') 
    _;      a(bra,      'is_pally.compare_loop')
    
    _;  a('is_pally.false')
    _;      a(lda_imm,  1)
    _;      a.macro     (skip2) 
    
    _;  a('is_pally.true')
    _;      a(lda_imm,  0)
    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(plx)
    _;      a.remark    ('Set flags for return')
    _;      a(cmp_imm,  0) 
    _;      a(rts) 
    