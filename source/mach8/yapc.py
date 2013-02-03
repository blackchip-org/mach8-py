#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: yapc.py 75 2011-11-04 20:21:51Z mcgann $
#------------------------------------------------------------------------------
"""
YAP 'compiler'
"""
from mach8.assembly import * 
from mach8 import memmap, tools 

compiler_factory = None 
"""
Function invoked to get a new instance of a Compiler object. 
"""

class Compiler(object):
    
    def __init__(self, mach, origin=memmap.PROGRAM_START, heap=memmap.HEAP):
        self.origin = origin
        self.a = tools.Assembler(mach.mem, origin=origin, meta=mach.meta)
        self.mem = mach.mem 
        self.meta = mach.meta 
        self.a.label('YAP:HEAP', heap) 
        self.interns = dict() 
        self.flow_stack = []
        self.flow_types = []
        
    #--------------------------------------------------------------------------
    # Statements
    #--------------------------------------------------------------------------    
    def done(self):
        """
        Jump to the YAP_EXIT_VECTOR for cleanup and return to monitor. NOP out
        the jump to the YAP_INCOMPLETE that was placed at the start of the 
        program by NEW()
        """
        a = self.a 
        
        _;      a.remark    ('DONE()')
        _;      a(jmp_ind,  'YAP_EXIT_VECTOR')
        
        a.position = memmap.PROGRAM_START
        
        _;      a.remark    ('NEW()')
        _;      a(nop)
        _;      a(nop)
        _;      a(nop) 
        
    def new(self):
        """
        Place a jump to the YAP_INCOMPLETE error and NOP out later when DONE
        is called. Call WARM_START to reset all vectors that may have 
        changed during previous execution. 
        """
        a = self.a 
        
        _;      a.remark    ('NEW()')
        _;      a(jmp_abs,  'YAP_INCOMPLETE')
        _;      a(jsr,      'WARM_START')
            
    def print_(self, *args):
        """
        For each argument in *args*, call print_one
        """
        a = self.a 
        
        _;      a.remark    ('PRINT(' + ', '.join(map(repr, args)) + ')')
        
        map(self.print_one, args) 

    def println(self, *args):
        """
        For each argument in *args*, call print_one and then write out a 
        trailing newline.
        """
        a = self.a 
        
        _;      a.remark    ('PRINTLN(' + ', '.join(map(repr, args)) + ')')
        
        map(self.print_one, args) 
        
        _;      a(lda_imm,  'CHR_LINE_FEED')
        _;      a(jsr,      'CHROUT')
        
    #--------------------------------------------------------------------------
    # Supporting methods
    #--------------------------------------------------------------------------   
    def malloc(self, size):
        """
        Allocate *size* number of bytes memory on the heap for static values. 
        Returns the pointer to the newly allocated area. 
        """
        ptr = self.mem[memmap.HEAP_PTR::2] - size 
        self.mem[memmap.HEAP_PTR::2] = ptr 
        return ptr
        
    def print_one(self, arg):
        """
        Print out the string representation of the *arg* using PRIMM.
        """
        a = self.a 
        
        _;      a(jsr,      'PRIMM')
        _;      a.data      (str(arg), 0) 
    