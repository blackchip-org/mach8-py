#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: matrix.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import * 

def assemble(a):
    _;  a.alias('char.start', 0x21) 
    _;  a.alias('char.stop',  0x7f) 
    
    _;  a('matrix.begin')
    _;      a.remark    ('Welcome to the Matrix!')
    _;      a(ldx_imm,  'char.start')
    
    _;  a('matrix.next_char')
    _;      a(txa) 
    _;      a(jsr,      'CHROUT')
    _;      a(inx) 
    _;      a(cpx_imm,  'char.stop') 
    _;      a(bne,      'matrix.next_char')
    _;      a(bra,      'matrix.begin')