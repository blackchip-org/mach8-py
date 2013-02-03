#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: io.py 81 2011-11-07 13:12:22Z mcgann $
#------------------------------------------------------------------------------
from mach8 import aliases, memmap, vm
import sys 
import fcntl
import os 
import errno
import operator

#------------------------------------------------------------------------------
# Terminal device
#------------------------------------------------------------------------------

class TerminalOutput(object):
    """
    Output terminal handler for use as an action in JiffyTimer. 
    """
    
    listeners = None 
    
    buffer_count = 0 
    
    flush_interval = 20
    
    def __init__(self, mem, destination=None): 
        self.mem = mem
        self.destination = destination
        self.listeners = list() 
        
    def __call__(self):
        # Is there anything to send? 
        if not self.mem.is_set(memmap.TERM_STATUS, aliases.TERM_TX_READY): 
            return
        output_char = self.mem[memmap.TERM_OUTPUT] 
        [listener(output_char) for listener in self.listeners] 

        do_flush = False
        if output_char == '\n': 
            self.buffer_count = 0
        else: 
            self.buffer_count += 1
        if self.buffer_count >= self.flush_interval: 
            do_flush = True
            self.buffer_count = 0
            
        # Setting default destination to stdout in the constructor doesn't seem 
        # to work when running the monitor test suite--the object is always
        # an instance of IORedirector and things don't work as expected.  
        try:
            if self.destination is not None:  
                self.destination.write(chr(output_char))
                if do_flush: 
                    self.destination.flush()
            else:
                sys.stdout.write(chr(output_char))
                if do_flush:
                    sys.stdout.flush()  
            self.mem.clear_bits(memmap.TERM_STATUS, aliases.TERM_TX_READY)
        except IOError as (code, message): 
            if code == errno.EAGAIN: 
                pass
            else:
                raise

class TerminalInput(object):
    """
    Input terminal handler for use as an action in JiffyTimer. 
    """
    
    listeners = None 
    
    def __init__(self, mem, source=None):
        if source is None: 
            source = self.getch
        self.source = source 
        self.mem = mem
        self.listeners = list() 
        self._fcntl_settings = None 
        
    def start(self):   
        """
        Sets input to non-blocking. 
        """
        # StringIO object doesn't have a file descriptor.      
        if not hasattr(sys.stdin, 'fileno'): 
            self._fcntl_settings = None 
        else:
            fd = sys.stdin.fileno()
            fcntl_settings = fcntl.fcntl(fd, fcntl.F_GETFL)    
            fcntl.fcntl(fd, fcntl.F_SETFL, fcntl_settings | os.O_NONBLOCK)        
            self._fcnt_settings = fcntl_settings

    def stop(self):
        """
        Resets input to previous settings. 
        """
        if self._fcntl_settings is not None: 
            fd = sys.stdin.fileno()
            fcntl.fcntl(fd, fcntl.F_SETFL, self._fcntl_settings)
    
    def getch(self):
        """
        Default function to get one character of input from stdin.  
        """
        return sys.stdin.read(1)
    
    def __call__(self):
        # Don't read from terminal if nobody is waiting for input
        if not self.mem.is_set(memmap.TERM_STATUS, aliases.TERM_RX_REQUEST):
            return
        # If RX ready is still set, the last character has not been consumed
        # yet
        if self.mem.is_set(memmap.TERM_STATUS, aliases.TERM_RX_READY):
            return
    
        try: 
            input_char = self.source()
            if len(input_char) == 0: 
                return 
            [listener(input_char) for listener in self.listeners]
            self.mem[memmap.TERM_INPUT] = ord(input_char)
            self.mem.set_bits(memmap.TERM_STATUS, aliases.TERM_RX_READY)
        except IOError as (code, message):
            # Non-blocking read from terminal, attempt again in next loop if
            # not a real IO error
            if code != errno.EAGAIN: 
                raise IOError, (code, message)

            
#------------------------------------------------------------------------------
# FPU
#------------------------------------------------------------------------------

FPU_BINARY_MAP = { 
    aliases.FPU_ADD:    operator.add, 
    aliases.FPU_SUB:    operator.sub, 
    aliases.FPU_MUL:    operator.mul, 
    aliases.FPU_DIV:    operator.div, 
}

FPU_COMPARE_MAP = { 
    aliases.FPU_EQ: operator.eq, 
    aliases.FPU_NE: operator.ne, 
    aliases.FPU_GT: operator.gt,
    aliases.FPU_GE: operator.ge, 
    aliases.FPU_LT: operator.lt, 
    aliases.FPU_LE: operator.le,  
}

_f0_start = aliases.FAC0 
_f0_end = _f0_start + aliases.SIZEOF_FAC
_f1_start = aliases.FAC1 
_f1_end = _f1_start + aliases.SIZEOF_FAC

class FPU(object):
    """
    Floating point processing unit (aka, the Cheat Stick)
    """
    
    def __init__(self, mem):
        self.mem = mem
        
    def __call__(self):
        cmd = self.mem[memmap.FPU_COMMAND]
        if cmd == 0: 
            return
        op1 = vm.fac2py(self.mem[_f0_start:_f0_end]) 
        op2 = vm.fac2py(self.mem[_f1_start:_f1_end])
        result = 0
        status = aliases.FPU_OK
        if cmd in FPU_BINARY_MAP: 
            try:
                result = FPU_BINARY_MAP[cmd](op1, op2) 
            except ZeroDivisionError: 
                status = aliases.ERR_FPU_DIVISION_BY_ZERO 
        elif cmd in FPU_COMPARE_MAP: 
            cmpresult = FPU_COMPARE_MAP[cmd](op1, op2) 
            result = 1 if cmpresult else 0 
        else:
            status = aliases.ERR_FPU_INVALID_COMMAND 
        self.mem[_f0_start:_f0_end] = vm.py2fac(result) 
        self.mem[memmap.FPU_COMMAND] = 0 
        self.mem[memmap.FPU_STATUS] = status 

