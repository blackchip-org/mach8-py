#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: rom.py 146 2012-03-22 02:12:42Z mcgann $
#------------------------------------------------------------------------------
"""
Kernal and YAP runtime routines. 
"""
from mach8.assembly import * 

__all__ = ['mach8_start', 'welcome', 'cold_start', 'warm_start', 'idle', 
           'monitor', 'yap_exit', 'yap_error', 'strerr_table', 'yap_incomplete', 
           'chrout', 'chrin', 'strout', 'linein', 'primm', 'malloc', 
           'bzero', 'memcpy', 'txtrst', 'chrput', 'txtout', 'strlen', 
           'strcpy', 'strcmp', 'strcat', 'findmsg', 'bcd2chr', 
           'zfac0_', 'zfac1_', 'mem2fac', 'fac2mem', 'facop', 'fac2str']

#------------------------------------------------------------------------------
# Administrative routines
#------------------------------------------------------------------------------
def mach8_start(a):
    """
    Entry point on CPU reset.
    """
    _;  a('MACH8_START')
    _;      a(jsr,      'COLD_START')
    _;      a(jsr,      'WARM_START')
    _;      a(jsr,      'WELCOME') 
    _;      a(jmp_abs,  'MONITOR')
    
def welcome(a):
    """
    Prints 'Welcome to the Mach-8' to the terminal. 
    """
    _;  a('WELCOME')
    _;      a(jsr,      'PRIMM')
    _;      a.data      ('\nWelcome to the Mach-8!\n\n', 0)
    _;      a(rts) 

def cold_start(a):
    """
    Setup yap vectors. 
    """
    _;  a('COLD_START')
    _;      a.macro     (ldxy_imm, 'YAP_EXIT')
    _;      a.macro     (stxy_abs, 'YAP_EXIT_VECTOR')
    _;      a.macro     (ldxy_imm, 'YAP_ERROR')
    _;      a.macro     (stxy_abs, 'YAP_ABORT_VECTOR')
    
def warm_start(a):
    """
    Initializes variables and vectors. 
    """
    _;  a('WARM_START')
#    _;      a.remark    ('Always start with binary math')
#    _;      a(cld)
    
    _;      a.macro     (ldxy_imm, 'HEAP')
    _;      a.macro     (stxy_zp,  'HEAP_PTR')
    _;      a(jsr,      'TXTRST')
    _;
    _;      a.remark    ('Clean up registers')
    _;      a(lda_imm,  0)
    _;      a(ldx_imm,  0)
    _;      a(ldy_imm,  0)
    
    _;      a(rts) 
    
def idle(a):
    """
    No operation --- When the PC is equal to this routine, immediately service 
    actions registered with the :class:`JiffyTimer`. 
    """
    _;  a('IDLE')
    _;      a(rts) 
    
def monitor(a):
    """
    No operation -- When the PC is equal to this routine, stop the CPU and 
    start the monitor.
    """
    _;  a('MONITOR')
    _;      a.remark    ('In case the CPU is restarted at this point,') 
    _;      a.remark    ('run the monitor again.')
    _;      a(bra,      'MONITOR')

def yap_exit(a):
    """
    Default YAP exit handler. Assumes that jsr was used to start program and
    is the first item on the stack. Move stack pointer so that this is the
    only remaining item and then return to that address.
    """
    _;  a('YAP_EXIT')
    _;      a.remark    ('Clean up stack, leave last return address')
    _;      a(ldx_imm,  0xfd)
    _;      a(txs)
    _;      a(rts)  

def yap_error(a):
    """
    Default YAP error handler. Lookup message in STRERR_TABLE and write 
    to console. 
    """
    _;  a('YAP_ERROR')
    _;      a.remark    ('Print leading "? "')
    _;      a(lda_imm,  asc('?'))
    _;      a(jsr,      'CHROUT')
    _;      a(lda_imm,  asc(' '))
    _;      a(jsr,      'CHROUT')
    
    _;      a.remark    ('Print error message')
    _;      a(lda_zp,   'ERRNO')
    _;      a.macro     (ldxy_imm, 'STRERR_TABLE')
    _;      a(jsr,      'FINDMSG')
    _;      a(jsr,      'STROUT')
    
    _;      a.remark    ('Print "error"')
    _;      a(jsr,      'PRIMM')
    _;      a.data      (' error\n', 0)
     
    _;      a(jmp_ind,  'YAP_EXIT_VECTOR')
    
def strerr_table(a):
    _;  a('STRERR_TABLE')
    _;      a.data      ('No', 0)
    _;      a.data      ('String too long', 0)
    _;      a.data      ('General FPU', 0)
    _;      a.data      ('Invalid FPU operation', 0)
    _;      a.data      ('Division by zero', 0)
    _;      a.data      ('Program incomplete', 0)
    
def yap_incomplete(a):
    """
    Make sure ``DONE()`` is called by starting each program with a jump to this
    routine. When ``DONE()`` is called, clear out the jump with NOPs. 
    """
    _;  a('YAP_INCOMPLETE')
    _;      a(lda_imm,  'ERR_PROGRAM_INCOMPLETE')
    _;      a(sta_zp,   'ERRNO')
    _;      a(jmp_abs,  'YAP_ERROR')
    
#------------------------------------------------------------------------------
# Terminal I/O routines
#------------------------------------------------------------------------------

def chrout(a):
    """
    Prints a character to the terminal.
    
    * Parameter: A = Character to print 
    """
    _;  a('CHROUT')
    _;      a.remark    ('Prints a character to the terminal')
    _;      a.remark    ('A = char to print') 
    
    _;      a(pha)
    
    _;  a('chrout.wait')
    _;      a.remark    ('If TX ready is still set, that means the last')
    _;      a.remark    ('character has not yet been emitted. Wait until clear')
    _;      a(lda_imm,  'TERM_TX_READY')
    _;      a(bit_zp,   'TERM_STATUS') 
    _;      a(beq,      'chrout.ready')
    _;      a(jsr,      'IDLE')
    _;      a(bra,      'chrout.wait')
    
    _;  a('chrout.ready')
    _;      a.remark    ('Restore argument')
    _;      a(pla)
    _;      a.remark    ('Store character in the output register')
    _;      a(sta_zp,   'TERM_OUTPUT')
    _;
    _;      a.remark    ('Notify terminal output is ready')
    _;      a(sei)
    _;      a(lda_imm,  'TERM_TX_READY') 
    _;      a(ora_zp,   'TERM_STATUS') 
    _;      a(sta_zp,   'TERM_STATUS')
    _;      a(cli) 
    
    _;      a(rts) 
    
def chrin(a):
    """
    Read a character from the terminal.
    
    * Returns: A = character read. 
    """
    _;  a('CHRIN')
    _;      a.remark    ('Read a character from the terminal.')
    _;      a.remark    ('A = character read.')
    
    _;      a(phy)
    
    _;      a.remark    ('Ready to receive -- notify terminal')
    _;      a(sei)
    _;      a(lda_imm,  'TERM_RX_REQUEST')
    _;      a(ora_zp,   'TERM_STATUS')
    _;      a(sta_zp,   'TERM_STATUS')
    _;      a(cli)
    
    _;  a('chrin.wait')
    _;      a.remark    ('Busy wait until the terminal sends notification') 
    _;      a.remark    ('that data is ready')
    _;      a(lda_imm,  'TERM_RX_READY')
    _;      a(bit_zp,   'TERM_STATUS')
    _;      a(bne,      'chrin.ready')
    
    _;      a(jsr,      'IDLE')
    _;      a(bra,      'chrin.wait')
    
    _;  a('chrin.ready')
    _;      a.remark    ('Grab character input')
    _;      a(ldy_zp,   'TERM_INPUT')
    _;      a.remark    ('Clear both the TERM_RX_REQUEST and')
    _;      a.remark    ('TERM_RX_READY flags')
    _;      a(sei)
    _;      a(lda_imm,  'TERM_RX_COMPLETE')
    _;      a(and_zp,   'TERM_STATUS')
    _;      a(sta_zp,   'TERM_STATUS')
    _;      a(cli)
    
    _;      a.remark    ('Clean up')
    _;      a(tya)
    _;      a(ply)
    _;      a(rts) 
    
def strout(a):
    """
    Prints a zero-terminated string to the terminal (up to 254 bytes).  
    
    * Parameter: X/Y = string address (lo/hi) 
    * Uses: KA
    """
    _;  a('STROUT')
    _;      a.remark    ('Prints a zero-terminated string to the terminal.')
    _;      a.remark    ('Param: X,Y: low/high bytes of string address')
    
    _;      a(phy)      
    _;      a.remark    ('Store pointer in KA for IZY addressing')
    _;      a.macro     (stxy_zp, 'KA')
    _;      a(ldy_imm,  0)
    
    _;  a('strout.loop')
    _;      a.remark    ('Character loop')
    _;      a(lda_izy,  'KA')
    _;      a.remark    ('Terminator loaded?')
    _;      a(beq,      'strout.exit')
    
    _;      a(jsr,     'CHROUT') 
    _;      a.remark    ('Next character')
    _;      a(iny) 
    _;      a(bra,     'strout.loop')

    _;  a('strout.exit')
    _;      a(ply) 
    _;      a(rts) 
    
def linein(a):
    """
    Read a line from the terminal. Error if line > 254 bytes.
    
    * Returns: X,Y = Pointer to string read (lo/hi). 
    """ 
    _;  a('LINEIN')
    _;      a.remark    ('Read a line from the terminal.') 
    _;      a.remark    ('Returns: X,Y: Pointer to string read (lo/hi)')
    _;      a.remark    ('Error if line > 254 bytes')
    
    _;      a(pha)
    _;      a.remark    ('Y = buffer index')
    _;      a(ldy_imm,  0)

    _;  a('linein.loop')
    _;      a.remark    ('Character loop')    
    _;      a(jsr,      'CHRIN')
    _;      a.remark    ('Only deal with eoln on real systems')
    _;      a(cmp_imm,  'CHR_LINE_FEED')
    _;      a(beq,      'linein.done')
    
    _;      a.remark    ('Store character read')
    _;      a(sta_aby,  'TERM_INPUT_BUFFER')
    _;      a(iny)
    _;      a.remark    ('See if index wrapped around')
    _;      a(beq,      'linein.error')
    _;      a(bne,      'linein.loop')
    
    _;  a('linein.done')
    _;      a.remark    ('Write out terminator (Y advanced for LF)')
    _;      a(lda_imm,  0)
    _;      a(sta_aby,  'TERM_INPUT_BUFFER')
    
    _;      a.remark    ('Clean up')
    _;      a.macro     (ldxy_imm, 'TERM_INPUT_BUFFER')
    _;      a(pla) 
    _;      a(rts) 
        
    _;  a('linein.error')
    _;      a.remark    ('Avoid corrupt stack exception')
    _;      a(pla)
    _;      a(lda_imm, 'ERR_STRING_TOO_LONG')
    _;      a(sta_zp,  'ERRNO')
    _;      a(jmp_ind, 'YAP_ABORT_VECTOR')
    
def primm(a):
    """
    Print immediate -- print the zero-terminated string found after the jsr 
    instruction and resume execution with the instruction following the string. 
    """
    _;  a('PRIMM')
    _;      a.remark    ('Print immediate -- print the zero-terminated') 
    _;      a.remark    ('string found after the jsr to this routine.')

    _;      a(pha)
    _;      a(phx)
    _;      a(phy) 

    _;      a.remark    ('Get return address from stack.')
    _;      a(tsx) 
    _;      a.remark    ('Add 4 since 3 items were pushed')
    _;      a(lda_abx,  add('STACK_PAGE', 4)) 
    _;      a(ldy_abx,  add('STACK_PAGE', 5))    
    _;      a(tax)
    _;      a.remark    ('pc points to address - 1 of actual return. Add one.')
    _;      a.macro     (inxy)
    _;      a(jsr,      'STROUT')
    
    _;      a.remark    ('Increase return address by len + terminator')
    _;      a(jsr,      'STRLEN')
    _;      a(clc)
    _;      a(adc_imm,  1)
    
    _;      a.remark    ('Modify return address')
    _;      a(tsx)
    _;      a(adc_abx,  add('STACK_PAGE', 4))
    _;      a(sta_abx,  add('STACK_PAGE', 4))
    _;      a(lda_imm,  0)
    _;      a(adc_abx,  add('STACK_PAGE', 5))       
    _;      a(sta_abx,  add('STACK_PAGE', 5)) 
    
    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(plx)
    _;      a(pla)
    _;      a(rts) 
    
#------------------------------------------------------------------------------
# Memory routines
#------------------------------------------------------------------------------

def malloc(a):
    """
    Decrement HEAP_PTR by given amount.
    
    * Parameter: A = size of memory to allocate.
    * Returns: A = size allocated,
    * Returns: X/Y = value of HEAP_PTR (hi/lo)
    * Uses: KA 
    """
    _;  a('MALLOC')
    _;      a.remark    ('Decrement HEAP_PTR by given amount.')
    _;      a.remark    ('A = size of memory to allocate')
    _;      a.remark    ('Uses KA')
    
    _;      a.remark    ('Store to do subtraction')
    _;      a(sta_zp,  'KA')
    _;      a.remark    ('Preserve for return')
    _;      a(pha) 
    
    _;      a.remark    ('Subtract 16-bit')
    _;      a(sec) 
    _;      a(lda_zp,   'HEAP_PTR')
    _;      a(sbc_zp,   'KA')
    _;      a(sta_zp,   'HEAP_PTR')
    _;      a.remark    ('Save for return')
    _;      a(tax) 
    
    _;      a(lda_zp,   add('HEAP_PTR', 1)) 
    _;      a(sbc_imm,  0)   
    _;      a(sta_zp,   add('HEAP_PTR', 1))
    _;      a.remark    ('Save for return') 
    _;      a(tay)
    
    _;      a.remark    ('Clean up')
    _;      a(pla) 
    _;      a(rts) 
    
def bzero(a):
    """
    Zero out memory. 
    
    * Parameters: X/Y = Starting address (lo/hi) 
    * Parameter: A = length 
    * Uses: KA - KB
    """
    _;  a('BZERO')
    _;      a.remark    ('Zero out memory')
    _;      a.remark    ('X/Y = Starting address (lo/hi), A = length')
    
    _;      a(pha)
    _;      a(phx)
    _;      a(phy) 
    _;      a.remark    ('Store address in KA for IZY addressing')
    _;      a.macro     (stxy_zp, 'KA')
    _;      a.remark    ('Move length to IZY index')
    _;      a(tay) 
    _;      a.remark    ('Zero to store')
    _;      a(lda_imm,  0)
    
    _;  a('bzero.loop')
    _;      a.remark    ('Byte loop')
    _;      a(dey)
    _;      a.remark    ('Done on wrap around')
    _;      a(cpy_imm,  0xff)
    _;      a(beq,      'bzero.exit')
    _;      a(sta_izy,  'KA')
    _;      a(bra,      'bzero.loop')
    
    _;  a('bzero.exit')
    _;      a(ply)
    _;      a(plx)
    _;      a(pla) 
    _;      a(rts)
    
def memcpy(a):
    """
    Copy memory, 255 byte maximum.
     
    * Parameter: R1 = source address
    * Parameter: R3 = destination address
    * Parameter: A = length
    """
    _;  a('MEMCPY')
    _;      a.remark    ('Copy memory, 255 bytes max')
    _;      a.remark    ('R1 = src address, R3 = dest address, A = length')

    _;      a(pha)
    _;      a(phy)
    _;      a.remark    ('Use Y for IZY indexing') 
    _;      a(tay)
    
    _;  a('memcpy.loop')
    _;      a.remark    ('Byte loop')
    _;      a(dey)
    _;      a.remark    ('Done on wrap around')
    _;      a(cpy_imm,  0xff)
    _;      a(beq,     'memcpy.exit')
    
    _;      a.remark    ('Copy byte')
    _;      a(lda_izy, 'R1') 
    _;      a(sta_izy, 'R3') 
    _;      a(bra,     'memcpy.loop')
    
    _;  a('memcpy.exit')
    _;      a(ply)
    _;      a(pla) 
    _;      a(rts) 
    
#------------------------------------------------------------------------------
# Text work routines
#------------------------------------------------------------------------------

def txtrst(a):
    """
    Reset the text work pointer to the start of the work area. 
    """
    _;  a('TXTRST')
    _;      a.remark    ('Reset the text work pointer the the start of the')
    _;      a.remark    ('work area.')
    
    _;      a(phx) 
    _;      a(phy) 
    
    _;      a.macro     (ldxy_imm, 'TEXT_WORK')
    _;      a.macro     (stxy_zp,  'TEXT_WORK_PTR')

    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(plx) 
    _;      a(rts) 
    
def chrput(a):
    """
    Put a character in the text work area and advance the work area pointer. 
    
    * Parameter: A = Character to put
    """
    _;  a('CHRPUT')
    _;      a.remark   ('Put a character in the text work area and advance')
    _;      a.remark   ('the work area pointer. A = char to put')
    
    _;      a(pha)
    _;      a(phy)
    _;      a.remark    ('IZY dummy index') 
    _;      a(ldy_imm,  0) 
    
    _;      a(sta_izy,  'TEXT_WORK_PTR')
    _;      a.macro     (inc_zp_word, 'TEXT_WORK_PTR')
    
    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(pla) 
    _;      a(rts) 
    
def txtout(a):
    """
    Print out the contents of the text work area to the terminal. 
    """
    _;  a('TXTOUT')
    _;      a.remark    ('Print out the contents of the text work area to the') 
    _;      a.remark    ('terminal.')
    
    _;      a(phx)
    _;      a(phy)
    
    _;      a.macro     (ldxy_imm, 'TEXT_WORK') 
    _;      a(jsr,      'STROUT')

    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(plx)
    _;      a(rts) 
    
#------------------------------------------------------------------------------
# String routines
#------------------------------------------------------------------------------

def strlen(a):
    """
    Returns the length of a string.
     
    * Parameters: X/Y = Address of string (lo/hi)
    * Returns: A = length
    * Uses: KA - KB
    """
    _;  a('STRLEN')
    _;      a.remark   ('Returns the length of a string.')
    _;      a.remark   ('Parameter: X/Y = Address of string (lo/hi)')
    _;      a.remark   ('Returns: A = length')
    _;      a.remark   ('Uses: KA - KB')
    
    _;      a(phy) 
    _;      a.remark   ('Store X/Y in KA for IZY indexing')
    _;      a.macro    (stxy_zp, 'KA')
    _;      a.remark   ('IZY index')
    _;      a(ldy_imm, 0)
    
    _;  a('strlen.loop')
    _;      a.remark   ('Character loop')
    _;      a(lda_izy, 'KA')
    _;      a.remark   ('Is terminator?')
    _;      a(beq,     'strlen.exit')
    
    _;      a.remark   ('Next character')
    _;      a(iny)
    _;      a(bra,     'strlen.loop')
    
    _;  a('strlen.exit')
    _;      a.remark   ('Answer in Y, needs to be in A')
    _;      a(tya) 
    _;      a.remark   ('Clean up')
    _;      a(ply) 
    _;      a(rts) 
    
def strcpy(a):
    """
    Copy a string. 
    
    * Parameter: R1 = source string address.
    * Parameter: R3 = destination string address. 
    """
    _;  a('STRCPY')
    _;      a.remark    ('Copy a string.')
    _;      a.remark    ('R1 = source, R3 = destination')
    
    _;      a(pha)
    _;      a(phy)
    _;      a.remark    ('Index for IZY addressing') 
    _;      a(ldy_imm,  0) 
    
    _;  a('strcpy.loop')
    _;      a.remark    ('Character loop')
    _;      a(lda_izy, 'R1')
    _;      a(sta_izy, 'R3')
    _;      a.remark    ('Loaded terminator?') 
    _;      a(beq,     'strcpy.exit')
    
    _;      a.remark    ('Next character')
    _;      a(iny)
    _;      a(bra,     'strcpy.loop')
    
    _;  a('strcpy.exit')
    _;      a(ply)
    _;      a(pla) 
    _;      a(rts) 
    
def strcmp(a):
    """
    Compare two strings. 
    
    Parameter: R1 = String 1 address
    Parameter: R3 = String 2 pointer. 
    Returns: A = 1, false. A = 0 true. 
    """
    _;  a('STRCMP')
    _;      a.remark   ('Compare two strings.')
    _;      a.remark   ('R1: String 1 pointer, R3: String 2 pointer')
    _;      a.remark   ('Returns A = 0, false. A = 1 true')

    _;      a(phx) 
    _;      a(phy)
    _;      a.remark   ('X = -1 equals; X = 0 not equals; X = 1 not done')
    _;      a(ldx_imm, 1)
    _;      a.remark   ('IZY Index')
    _;      a(ldy_imm, 0)
    
    _;  a('strcmp.loop') 
    _;      a.remark   ('Character loop')
    _;      a.remark   ('Check for first terminator')
    _;      a(lda_izy, 'R1')
    _;      a(bne,     'strcmp.not_zero_1')
    
    _;      a(dex) 
    
    _;  a('strcmp.not_zero_1')
    _;      a.remark   ('Compare characters')
    _;      a(cmp_izy, 'R3')
    _;      a(bne,     'strcmp.not_equals')
    
    _;      a.remark   ('Check for second terminator')
    _;      a(lda_izy, 'R3')
    _;      a(bne,     'strcmp.not_zero_2')
    
    _;      a(dex)
    
    _;  a('strcmp.not_zero_2')
    _;      a.remark    ('Terminator check')
    _;      a(cpx_imm,  0) 
    _;      a.remark    ('Two terminators?')
    _;      a(bmi,      'strcmp.equals')
    
    _;      a.remark    ('One terminator?')
    _;      a(beq,      'strcmp.not_equals')
    
    _;      a.remark    ('Next character')
    _;      a(iny)
    _;      a(bra,      'strcmp.loop')
    
    _;  a('strcmp.not_equals')
    _;      a.remark    ('Return value')
    _;      a(lda_imm,  1)
    _;      a.macro     (skip2)
    
    _;  a('strcmp.equals')
    _;      a.remark    ('Return value')
    _;      a(lda_imm,  0)
    
    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(plx)
    _;      a(cmp_imm,  0) 
    _;      a(rts)
    
def strcat(a):
    """
    Concatenate two strings. 
    
    * Parameter: R1 = String 1 address.
    * Parameter: R3 = string 2 address. 
    * Returns: X/Y = address of new string (lo/hi -- also in R1)
    * Uses: KC
    """
    _;  a('STRCAT')
    _;      a.remark    ('Concatenate two strings')
    _;      a.remark    ('R1 = string 1, R3 = string 2')
    _;      a.remark    ('Returns: X/Y = address of new string, also in R1')
    _;      a.remark    ('Uses: KC')
    
    _;      a.remark    ('Compute length, save on stack for later')
    _;      a.macro     (ldxy_zp, 'R3')
    _;      a(phx)  
    _;      a(phy)
    _;      a(jsr,      'STRLEN')
    _;      a.remark    ('Store result in KC for addition')
    _;      a(sta_zp,   'KC')
    
    _;      a.remark    ('Compute length, save on stack for later')
    _;      a.macro     (ldxy_zp, 'R1')
    _;      a(phx)
    _;      a(phy)
    _;      a(jsr,     'STRLEN')
    
    _;      a.remark    ('Add lengths from A and KC, save A for later')
    _;      a(pha) 
    _;      a(clc)
    _;      a(adc_zp,  'KC')
    _;      a.remark    ('Add one for terminator')
    _;      a(adc_imm,  1)
    _;      a(jsr,     'MALLOC')

    _;      a.remark    ('Copy R1 string to newly allocated area')
    _;      a(pla) 
    _;      a(ply)
    _;      a(plx)
    _;      a.macro    (stxy_zp, 'R1')
    _;      a.macro    (ldxy_zp, 'HEAP_PTR')
    _;      a.macro    (stxy_zp, 'R3')
    _;      a(jsr,     'STRCPY')
    
    _;      a.remark    ('Copy R3 string to end of first string')
    _;      a(ply)
    _;      a(plx)
    _;      a.macro     (stxy_zp, 'R1')
    
    _;      a.remark    ('R3 now holds HEAP_PTR, add length of first string')
    _;      a(clc)
    _;      a(adc_zp,   'R3')
    _;      a(sta_zp,   'R3')
    _;      a(lda_imm,  0)
    _;      a(adc_zp,   add('R3', 1))
    _;      a(sta_zp,   add('R3', 1))  
    _;      a(jsr,      'STRCPY')
    
    _;      a.remark    ('Clean up')
    _;      a.macro     (ldxy_zp, 'HEAP_PTR')
    _;      a.macro     (stxy_zp, 'R1')
    _;      a(rts)  

def findmsg(a):
    """
    Find a message in a string table. 
    
    * Parameter: A = string index. 
    * Parameter: X/Y = table address (lo/hi)
    * Returns: X/Y = string address (lo/hi)
    * Uses: KA - KB
    """
    _;  a('FINDMSG')
    _;      a.remark    ('Find a message in a string table')
    _;      a.remark    ('A = string index, X,Y = table address (lo/hi)')
    _;      a.remark    ('Returns: X,Y = string address (lo/hi)')
    
    _;      a(pha) 
    _;      a.remark    ('Store in KA for IZY addressing')
    _;      a.macro     (stxy_zp, 'KA')
    _;      a.remark    ('X is now string index.')
    _;      a(tax)
    _;      a.remark    ('IZY dummy')
    _;      a(ldy_imm,  0)

    _;  a('findmsg.loop')
    _;      a.remark    ('Character loop. Dec X for each 0 seen.')
    _;      a.remark    ('Done when X = 0')
    _;      a(cpx_imm,  0)
    _;      a(beq,     'findmsg.exit')
    
    _;      a.remark    ('Increment table pointer') 
    _;      a.macro     (inc_zp_word, 'KA')
    _;      a.remark    ('Load character') 
    _;      a(lda_izy,  'KA')
    _;      a(bne,      'findmsg.no_terminator')
    
    _;      a(dex)
    _;      a.remark    ('Since a zero was found, need to advance the pointer')
    _;      a.remark    ('by one to start at the next string.')
    _;      a.macro     (inc_zp_word, 'KA')
    
    _;  a('findmsg.no_terminator')
    _;      a(bra,      'findmsg.loop')

    _;  a('findmsg.exit')
    _;      a.remark    ('KA holds found string address')
    _;      a.macro     (ldxy_zp, 'KA')
    _;      a(pla) 
    _;      a(rts) 

def bcd2chr(a):
    """
    Converts a BCD nibble to an ASCII character. Use either ``BCD2CHAR_HI`` 
    or ``BCD2CHAR_LO``.
    
    * Parameter: A = byte to convert.
    * Returns: A = ASCII char
    """
    _;  a('BCD2CHR_HI')
    _;      a.remark    ('Converts the high nibble from BCD to ASCII character')
    _;      a.remark    ('A = byte to convert. Returns A = char')
    _;      a.macro     (lsr_nibble)
    _;      a.macro     (skip2)
    
    _;  a('BCD2CHR_LO')
    _;      a.remark    ('Converts the low nibble from BCD to ASCII character')
    _;      a.remark    ('A = byte to convert. Returns A = char')
    _;      a(and_imm,  0x0f) 
    
    _;      a(clc)
    _;      a(adc_imm,  asc('0'))
    _;      a(rts) 

#------------------------------------------------------------------------------
# Floating point routines
#------------------------------------------------------------------------------

def zfac0_(a):
    """
    Zero out FAC0. 
    """
    _;  a('ZFAC0')
    _;      a.remark    ('Zero out FAC0')
    _;      a.macro     (zfac0)
    _;      a(rts) 
    
def zfac1_(a):
    """
    Zero out FAC1
    """
    _;  a('ZFAC1')
    _;      a.remark    ('Zero out FAC1')
    _;      a.macro     (zfac1)
    _;      a(rts) 
    
def mem2fac(a):
    """
    Copy a numeric value in memory to a FAC.
    
    * Uses: R1 - R4
    * Destroys: A
    """
    _;  a('MEM2FAC0')
    _;      a.remark    ('Copy number in memory to FAC0') 
    _;      a.remark    ('Uses R1 - R4, destroys: A')
    _;      a(lda_imm,  'FAC0')
    _;      a.macro     (skip2)
    
    _;  a('MEM2FAC1')
    _;      a.remark    ('Copy number in memory to FAC1')
    _;      a.remark    ('Uses R1 - R4, destroys: A')
    _;      a(lda_imm,  'FAC1')
    
    _;      a.remark    ('Memory copy')
    _;      a.macro     (stxy_zp, 'R1') 
    _;      a.remark    ('A holds FAC address')
    _;      a(tax) 
    _;      a(ldy_imm,  0) 
    _;      a.macro     (stxy_zp, 'R3')
    _;      a(lda_imm, 'SIZEOF_FAC')
    _;      a(jsr,     'MEMCPY')
    
    _;      a(rts) 
    
def fac2mem(a):
    """
    Copy a numeric value in a FAC to memory. 
    
    * Uses: R1 - R4
    * Destroys: A
    """
    _;  a('FAC2MEM0')
    _;      a.remark    ('Copy FAC0 to memory')
    _;      a.remark    ('Uses R1 - R4, destroys: A')
    _;      a(lda_imm,  'FAC0') 
    _;      a.macro     (skip2) 
    
    _;  a('FAC2MEM1')
    _;      a.remark    ('Copy FAC0 to memory')
    _;      a.remark    ('Uses R1 - R4, destroys: A')
    _;      a(lda_imm,  'FAC1')
    
    _;      a.remark    ('Memory copy')
    _;      a.macro     (stxy_zp, 'R3')
    _;      a.remark    ('A holds FAC address')
    _;      a(tax)
    _;      a(ldy_imm,  0) 
    _;      a.macro     (stxy_zp, 'R1')
    _;      a(lda_imm,  'SIZEOF_FAC')
    _;      a(jsr,      'MEMCPY')
    
    _;      a(rts) 
    
def facop(a):
    """
    Execute a floating point operation. 
    
    * Parameter: A = FPU operation
    """
    _;  a('FACOP')
    _;      a(sta_zp,   'FPU_COMMAND')
    
    _;  a('facop.loop')
    _;      a.remark    ('Busy wait until FPU has finished operation')
    _;      a(lda_zp,   'FPU_STATUS')
    _;      a(bne,      'facop.check_status')
   
    _;      a(jsr,      'IDLE')
    _;      a(bra,      'facop.loop')
    
    _;  a('facop.check_status')
    _;      a.remark    ('Clear out status for next operation')
    _;      a(stz_zp,   'FPU_STATUS')
    _;      a.remark    ('Was there an error?')
    _;      a(cmp_imm,  'FPU_OK')
    _;      a(beq,      'facop.exit')
    
    _;      a(sta_zp,   'ERRNO')
    _;      a(jmp_ind,  'YAP_ABORT_VECTOR')
    
    _;  a('facop.exit')
    _;      a(rts) 
    
def fac2str(a):
    """
    Converts a floating point accumulator value to a string. 
    
    * Returns: String in TEXT_WORK
    * Uses: KA - KE, destroys: A
    """
    _;      a.alias     ('fac2str.decimal_pos',   'KA')
    _;      a.alias     ('fac2str.digits',        'KB')
    _;      a.alias     ('fac2str.zeros',         'KC')
    _;      a.alias     ('fac2str.sign_exponent', 'KD')
    _;      a.alias     ('fac2str.exponent',      'KE')
    
    _;  a('FAC2STR0')
    _;      a.remark    ('Converts FAC0 to a string')
    _;      a.remark    ('Returns: TEXT_WORK, Uses: KA - KE, destroys: A')    
    _;      a(lda_imm,  'FAC0')
    _;      a.macro     (skip2)
    
    _;  a('FAC2STR1')
    _;      a.remark    ('Converts FAC1 to a string')
    _;      a.remark    ('Returns: TEXT_WORK, Uses: KA - KE, destroys: A') 
    _;      a(lda_imm,  'FAC1')
    
    _;      a(sta_zp,   'FAC_PTR')
    _;      a(phx) 
    _;      a(phy) 
    _;      a(stz_zp,   'fac2str.digits')
    _;      a(stz_zp,   'fac2str.zeros')
    _;      a.remark    ('Set default decimal point position to an') 
    _;      a.remark    ('unattainable value')
    _;      a(lda_imm,  0xff)
    _;      a(sta_zp,   'fac2str.decimal_pos')
    _;      a(jsr,      'TXTRST')
        
    _;      a.remark    ('Grab for easy access')
    _;      a(ldy_imm,  'FAC_SIGN')
    _;      a(lda_imm,  'SIGN_EXPONENT')
    _;      a(and_izy,  'FAC_PTR')
    _;      a(sta_zp,   'fac2str.sign_exponent')
    
    _;      a(ldy_imm,  'FAC_EXPONENT')
    _;      a(lda_izy,  'FAC_PTR')
    _;      a(sta_zp,   'fac2str.exponent')

    _;      a.remark    ('Print out in SN if the exponent is> 6')
    _;      a(cmp_imm,  7)
    _;      a(bmi,      'fac2str.check_digits')
    _;      a(jmp_abs,  'sci_notation')
    
    _;  a('fac2str.check_digits')
    _;      a.remark    ('Print in SN also if the printable digits > 7')
    _;      a(jsr,      'count_digits')
    _;      a(lda_zp,   'fac2str.digits')
    _;      a(cmp_imm,  8)
    _;      a(bmi,      'fac2str.normal_notation')
    _;      a(jmp_abs,  'sci_notation')
    
    _;  a('fac2str.normal_notation')
    _;      a(jsr,      'put_mantissa_sign')
    
    _;      a.remark    ('Check sign of exponent')
    _;      a(lda_zp,   'fac2str.sign_exponent')
    _;      a(beq,      'fac2str.compute_decimal_pos')
    
    _;      a.remark    ('Negative exponent value always starts with "0."')
    _;      a(lda_imm,  asc('0'))
    _;      a(jsr,      'CHRPUT')
    _;      a(lda_imm,  asc('.'))
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('More leading zeros if the exponent is > 1') 
    _;      a(lda_zp,   'fac2str.exponent')
    _;      a(cmp_imm,  2) 
    _;      a(bmi,      'fac2str.process_digits')
    
    _;      a.remark    ('Exponent becomes counter, put zeros until zero')
    _;      a(tax)
    
    _;  a('fac2str.leading_loop')
    _;      a(dex)
    _;      a(beq,      'fac2str.process_digits')
    _;      a(lda_imm,  asc('0')) 
    _;      a(jsr,      'CHRPUT')
    _;      a(dec_zp,   'fac2str.digits')
    _;      a(bra,      'fac2str.leading_loop')
    
    _;  a('fac2str.compute_decimal_pos')
    _;      a.remark    ('digits count decreases when emitted, so ')
    _;      a.remark    ('decimal_pos = digits - exponent - 1')
    _;      a(lda_zp,   'fac2str.digits')
    _;      a(sec)
    _;      a(sbc_zp,   'fac2str.exponent')
    _;      a(sta_zp,   'fac2str.decimal_pos')
    _;      a(dec_zp,   'fac2str.decimal_pos')
    
    _;  a('fac2str.process_digits')
    _;      a.remark    ('Working top-down. Done when Y = 0 (at sign value)')
    _;      a(ldy_imm,  'FAC_MANTISSA')
    
    _;  a('fac2str.mantissa_loop')
    _;      a.remark    ('High nibble')
    _;      a(lda_izy,  'FAC_PTR')
    _;      a.remark    ('Save across BCD2CHR call')
    _;      a(pha) 
    _;      a(jsr,      'BCD2CHR_HI')
    _;      a(jsr,      'put_digit')
    _;      a.remark    ('Pull byte digits now in case of early exit')
    _;      a(pla)
    _;      a.remark    ('Have all digits been emitted?')
    _;      a(ldx_zp,   'fac2str.digits')
    _;      a(beq,      'fac2str.exit')
    
    _;      a.remark    ('Low nibble')
    _;      a(jsr,      'BCD2CHR_LO')
    _;      a(jsr,      'put_digit')
    _;      a.remark    ('Have all digits been emitted?')
    _;      a(lda_zp,   'fac2str.digits')
    _;      a(beq,      'fac2str.exit')
    
    _;      a.remark    ('Next mantissa byte')
    _;      a(dey) 
    _;      a(bra,      'fac2str.mantissa_loop')
    
    _;  a('fac2str.exit')
    _;      a.remark    ('Terminate string')
    _;      a(lda_imm,  0)
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('Clean up')
    _;      a(ply)
    _;      a(plx)
    _;      a(rts) 
    
    # -----
    
    _;  a('sci_notation')
    _;      a(jsr,      'put_mantissa_sign')
    _;      a(ldy_imm,  'FAC_MANTISSA')
    _;      a(lda_izy,  'FAC_PTR')
    
    _;  a('sci_notation.mantissa_loop')
    _;      a(lda_izy,  'FAC_PTR')
    _;      a.remark    ('High nibble, save across BCD2CHR call')
    _;      a(pha) 
    _;      a(jsr,      'BCD2CHR_HI')
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('If this is the first digit, put decimal point')
    _;      a(cpy_imm,  'FAC_MANTISSA')
    _;      a(bne,      'sci_notation.low_nibble')
    
    _;      a(lda_imm,  asc('.'))
    _;      a(jsr,      'CHRPUT')
    
    _;  a('sci_notation.low_nibble')
    _;      a.remark    ('Low nibble, restore byte')
    _;      a(pla) 
    _;      a.remark    ('Only printing 7 digits')
    _;      a(cpy_imm,  1)
    _;      a(beq,      'sci_notation.exponent')
    _;      a(jsr,      'BCD2CHR_LO')
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('Next byte')
    _;      a(dey)
    _;      a(bra,      'sci_notation.mantissa_loop')
    
    _;  a('sci_notation.exponent')
    _;      a(lda_imm,  asc('E'))
    _;      a(jsr,      'CHRPUT')
    _;      a(lda_zp,   'fac2str.sign_exponent')
    _;      a(beq,      'sci_notation.plus')
    
    _;      a(lda_imm,  asc('-'))
    _;      a.macro     (skip2) 
    
    _;  a('sci_notation.plus')
    _;      a(lda_imm,  asc('+'))
    _;      a(jsr,      'CHRPUT')
    
    _;      a(lda_zp,   'fac2str.exponent')
    _;      a.remark    ('High nibble, save across BCD2CHR call')
    _;      a(pha)
    _;      a(jsr,      'BCD2CHR_HI')
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('Low nibble, restore byte')
    _;      a(pla)
    _;      a(jsr,      'BCD2CHR_LO')
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('Terminate string')
    _;      a(lda_imm,  0)
    _;      a(jsr,      'CHRPUT')
    
    _;      a.remark    ('Need to restore registers saved in fac2str')
    _;      a(ply)
    _;      a(plx)
    _;      a(rts) 
    
    # ------
    
    _;  a('put_digit')
    _;      a.remark   ('Put digit to the text work area. Add decimal point if')
    _;      a.remark   ('needed. A = digit to put')
    
    _;      a.remark   ('Save for later')
    _;      a(pha)
    
    _;      a(lda_zp,  'fac2str.digits')
    _;      a(cmp_zp,  'fac2str.decimal_pos')
    _;      a(bne,     'put_digit.no_decimal_point')
    _;      a(lda_imm, asc('.'))
    _;      a(jsr,     'CHRPUT')
    
    _;  a('put_digit.no_decimal_point')
    _;      a.remark    ('Restore digit')
    _;      a(pla)
    _;      a(jsr,      'CHRPUT')
    _;      a.remark    ('Decrement as digits are emitted, done when zero')
    _;      a(dec_zp,  'fac2str.digits')
    
    _;  a(rts) 
    
    # -----
    
    _;  a('put_mantissa_sign')
    _;      a.remark    ('Put a "-" if mantissa sign is set') 
    _;      a.remark    ('Destroys: A, Y')
    
    _;      a(ldy_imm,  'FAC_SIGN')
    _;      a(lda_izy,  'FAC_PTR')
    _;      a(and_imm,  'SIGN_MANTISSA') 
    _;      a(beq,      'put_mantissa_sign.exit')
    
    _;      a(lda_imm,  asc('-'))
    _;      a(jsr,      'CHRPUT')
    
    _;  a('put_mantissa_sign.exit')
    _;      a(rts) 
    
    # -----
    
    _;  a('count_digit')
    _;      a.remark    ('A = digit to count')
    _;      a(cmp_imm,  0)
    _;      a(bne,      'count_digit.not_zero')
    
    _;      a.remark    ('Zeros do not count unless another non-zero is found')
    _;      a(inc_zp,   'fac2str.zeros')
    _;      a(bra,      'count_digit.exit')
    
    _;  a('count_digit.not_zero')
    _;      a(inc_zp,   'fac2str.digits')
    _;      a.remark    ('Include any zeros that have been seen up to ')
    _;      a.remark    ('this point and not yet counted')
    _;      a(lda_zp,   'fac2str.zeros')
    _;      a(clc) 
    _;      a(adc_zp,   'fac2str.digits')
    _;      a(sta_zp,   'fac2str.digits')
    _;      a(stz_zp,   'fac2str.zeros')
    
    _;  a('count_digit.exit')
    _;      a(rts) 
    
    # -----
    
    _;  a('count_digits')
    _;      a.remark    ('Determine the number of digits that need to be')
    _;      a.remark    ('displayed. Do not count the zero before the decimal')
    _;      a.remark    ('point if 0.XXXX')
    
    _;      a(lda_zp,   'fac2str.sign_exponent')
    _;      a(beq,      'count_digits.no_leading')
    
    _;      a.remark    ('If the exponent sign is negative, count up the')
    _;      a.remark    ('leading zeros if the exponent is greater than one.')
    _;      a.remark    ('Decimal point has to move two spots for a leading') 
    _;      a.remark    ('zero to appear')
    _;      a(lda_zp,   'fac2str.exponent')
    _;      a(cmp_imm,  1)
    _;      a(bmi,      'count_digits.no_leading')
    
    _;      a(sec) 
    _;      a(sbc_imm,  1) 
    _;      a(sta_zp,   'fac2str.digits')
    
    _;  a('count_digits.no_leading')
    _;      a(ldy_imm,  'FAC_MANTISSA')
    
    _;  a('count_digits.mantissa_loop')
    _;      a(lda_izy,  'FAC_PTR')
    
    _;      a.remark    ('Low nibble, save byte for later')
    _;      a(pha) 
    _;      a.macro      (lsr_nibble) 
    _;      a(jsr,       'count_digit')
    
    _;      a.remark    ('High nibble, restore byte')
    _;      a(pla)
    _;      a(and_imm,  0x0f)
    _;      a(jsr,      'count_digit')
    
    _;      a.remark    ('Done counting digits?')
    _;      a(dey) 
    _;      a(bne,      'count_digits.mantissa_loop')
    
    _;      a.remark    ('If exponent is positive, digits must be >= exponent')
    _;      a(lda_zp,   'fac2str.sign_exponent')
    _;      a(bne,      'count_digits.exit')
    
    _;      a(lda_zp,   'fac2str.exponent')
    _;      a(clc)
    _;      a(adc_imm,  1)
    _;      a(cmp_zp,   'fac2str.digits')
    _;      a(bmi,      'count_digits.exit')
    
    _;      a(sta_zp,   'fac2str.digits')
    
    _;  a('count_digits.exit')
    _;      a(rts)
    
