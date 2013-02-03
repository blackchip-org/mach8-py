#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011-2012, Reprint what you like.
#
# $Id: fib.py 148 2012-03-22 02:29:57Z mcgann $
#------------------------------------------------------------------------------
from mach8.assembly import * 

def assemble(a):
    _;  a('fib')
    _;      a.remark    ('Initialize the first two values to one')    
    _;      a(lda_imm, 1) 
    _;      a(sta_abs, 'fib.acc')
    _;      a(sta_abs, 'fib.prev')
    _;      a.remark    ('Print out the first two values (just do acc twice)')
    _;      a(jsr,      'fib.print_acc')
    _;      a(jsr,      'fib.print_acc')
    
    _;      a.remark    ('Use BCD for all math')
    _;      a(sed) 
    _;      a.remark    ('Prepare for addition')
    _;      a(clc)
    
    _;  a('fib.loop')
    _;      a.remark    ('Add previous to current')
    _;      a(lda_abs,  'fib.prev')
    _;      a(adc_abs,  'fib.acc')
    _;      a.remark    ('Only print up to 99 -- done once exceeded')
    _;      a(bcs,      'fib.done')
    
    _;      a.remark    ('Answer in A, move acc to previous')
    _;      a(ldx_abs,  'fib.acc')
    _;      a(stx_abs,  'fib.prev')
    _;      a.remark    ('Store answer to acc')
    _;      a(sta_abs,  'fib.acc')
    _;      a(jsr,      'fib.print_acc')
    _;      a(bra,      'fib.loop')
      
    _;  a('fib.print_acc')
    _;      a.remark    ('Prints the BCD value in the accumulator')
    _;      a(lda_abs,  'fib.acc')
    _;      a.remark    ('A gets clobbered, save for later')
    _;      a(pha)
    _;      a(jsr,      'BCD2CHR_HI')
    _;      a.remark    ('Do not print leading zero')
    _;      a(cmp_imm,  asc('0'))
    _;      a(beq,      'fib.print_lo_byte')
    _;      a(jsr,      'CHROUT')
    
    _;  a('fib.print_lo_byte')
    _;      a.remark    ('Restore saved answer for lo byte')
    _;      a(pla) 
    _;      a(jsr,      'BCD2CHR_LO')
    _;      a(jsr,      'CHROUT')
    _;      a(lda_imm,  'CHR_LINE_FEED')
    _;      a(jsr,      'CHROUT')
    _;      a(rts)
    
    _;  a('fib.done')
    _;      a.remark    ('Clean up')
    _;      a(cld)
    _;      a(rts) 
    
    _;  a('fib.acc')
    _;      a.data(0)
    _;  a('fib.prev')
    _;      a.data(0)
    