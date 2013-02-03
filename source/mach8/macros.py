#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: macros.py 79 2011-11-07 12:48:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.instructions import *
from mach8.expressions import * 
from mach8 import vm 

__all__ = ['fac0', 'fac1', 'fac', 'inc_zp_word', 'inxy', 'ldxy_abs', 
           'ldxy_imm', 'ldxy_zp', 'lsr_nibble', 'macro', 'primm', 'skip2', 
           'stxy_zp', 'stxy_abs', 'zfac0', 'zfac1']

_ = object() 

def macro(func):
    """
    Decorator for macro functions.
    """
    def wrapper(a, *args):
        name = func.func_name
        a.remark('     macro     {}({})'
                 .format(name, ', '.join(map(repr, args))))
        func(a, *args)
        a.remark('     end       {}'.format(name)) 
    return wrapper 

def _fac(a, number, label, stz, sta):
    bytes = vm.py2fac(number) 
    for i, byte in enumerate(bytes): 
        if byte == 0: 
            a(stz,     add(label, i)) 
        else: 
            a(lda_imm, x8(byte))
            a(sta,     add(label, i)) 

@macro 
def fac0(a, number):
    """
    Store a floating point number to FAC0. 
    """
    _fac(a, number, 'FAC0', stz_zp, sta_zp)

@macro
def fac1(a, number):
    """
    Store a floating point number to FAC1.
    """
    _fac(a, number, 'FAC1', stz_zp, sta_zp)
    
@macro 
def fac(a, number, address):
    """
    Store a floating point number to memory.
    """
    _fac(a, number, address, stz_abs, sta_abs) 
    
@macro
def inc_zp_word(a, address):
    """
    Increments a word at a zero page location.
    """
    no_carry = a.auto_label() 
    
    _;      a(inc_zp,   address) 
    _;      a(bne,      no_carry)
    _;      a(inc_zp,   add(address, 1)) 
    _;      a.label(no_carry)
    
@macro 
def inxy(a):
    """
    Increments a word stored in the X (lo) and Y (hi) registers. 
    """
    no_carry = a.auto_label() 
    
    _;      a(inx)
    _;      a(bne,      no_carry)
    _;      a(iny)
    _;  a(no_carry) 
    
@macro
def ldxy_abs(a, address):
    """
    Load a word from address to the X (lo) and Y (hi) registers. 
    """
    _;      a(ldx_abs,  address) 
    _;      a(ldy_abs,  add(address, 1)) 
    
@macro
def ldxy_imm(a, address):
    """
    Load a word into the X (lo) and Y (hi) registers. 
    """
    _;      a(ldx_imm,  lb(address))
    _;      a(ldy_imm,  hb(address)) 
    
@macro
def ldxy_zp(a, address):
    """
    Load a word from a zero page address to the X (lo) and Y (hi) registers. 
    """
    _;      a(ldx_zp,   address) 
    _;      a(ldy_zp,   add(address, 1))  
    
@macro
def lsr_nibble(a):
    """
    Left shift nibble. 
    """
    _;      a(lsr_acc)
    _;      a(lsr_acc)
    _;      a(lsr_acc)
    _;      a(lsr_acc)
    
@macro
def primm(a, text):
    """
    Call :data:`PRIMM`, splitting up *text* into separate calls if too large. 
    """
    while len(text) >= 254: 
        head = text[:254]
        tail = text[254:]
        _;      a(jsr,  'PRIMM')
        _;      a.data  (head, 0) 
        text = tail 
    _;  a(jsr,  'PRIMM')
    _;  a.data  (text, 0) 
    
@macro
def skip2(a):
    """
    Emits the byte $2c. This is used to 'skip' over the next two bytes 
    since a harmless bit operation will be performed. Example:

    a('use.one')
        a(ldx_imm,  1)
        a.macro     (skip2)
    a('use.two')
        a(ldx_imm,  2)
        a(jsr,      'something.that.uses.x')

    Entering in at label 'use.one' will load the X register with 1, and then 
    'skip' the next load by performing a bit operation on the address $02a2 
    ($a2 is the opcode for ldx_imm and $02 is the argument). 
    """
    _;      a.data      (x8(0x2c)) 
    
@macro
def stxy_zp(a, address):
    """
    Store a word to a zero page address which is loaded into the X (lo) 
    and Y (hi) registers.
    """
    _;      a(stx_zp,   address)
    _;      a(sty_zp,   add(address, 1))
    
@macro
def stxy_abs(a, address):
    """
    Store a word to an address which is loaded into the X (lo) and Y (hi) 
    registers.
    """
    _;      a(stx_abs,   address)
    _;      a(sty_abs,   add(address, 1))
    

def _zfac(a, fac):
    loop = a.auto_label() 
    _;      a(phx) 
    _;      a(ldx_imm,  'SIZEOF_FAC')
    _;  a(loop)
    _;      a(stz_zpx,  sub(fac, 1)) 
    _;      a(dex)
    _;      a(bne,      loop)
    _;      a(plx) 
    
@macro
def zfac0(a):
    """
    Zero out FAC0.
    """
    _zfac(a, 'FAC0')
    
@macro
def zfac1(a):
    """
    Zero out FAC1.
    """
    _zfac(a, 'FAC1')
    