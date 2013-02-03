#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: mach.py 73 2011-10-27 12:44:53Z mcgann $
#------------------------------------------------------------------------------
"""
The Mach-8 virtual computer and supporting classes. 
"""
from mach8 import aliases, io, memmap, memory, rom, tools, x6502, yapc


BLOCK_ZERO_PAGE = 'zero_page'
"""
Name for the zero page memory block: ``$0000 - $00FF``
"""

BLOCK_STACK = 'stack'
"""
Name for the stack block: ``$0100 - $01FF``
"""

BLOCK_SCRATCH = 'scratch' 
"""
Name for the block reserved for scratch space: ``$0200 - $05FF``
"""

BLOCK_ROM = 'rom' 
"""
Name for the kernel and runtime block: ``$0600 - $1FFF``
"""

BLOCK_PROGRAM = 'program' 
"""
Name for the block of memory for user programs: ``$2000 - $FFEF``
"""

BLOCK_VECTOR = 'vector'
"""
Name for the block containg vectors and jump tables: ``$FFF0 - $FFFF``
"""

class JiffyTimer(object):
    """
    A series of *actions* that are executed at a certain *interval*. Each 
    time :meth:`cycle` is invoked, a counter is incremented and if it equals 
    the *interval* count, all *actions* in the sequence are called in iteration 
    order. Actions registered should be callable objects.
    """

    actions = None 
    """
    List of actions to be called. 
    """
    
    interval = 0
    """
    The number of times :meth:`cycle` needs to be called before actions are
    executed. 
    """
    
    count = 0 
    """
    Current numer of times :meth:`cycle` has been called -- resets to zero 
    when the actions are called. 
    """
    
    def __init__(self, actions, interval=100):
        self.actions = list(actions)
        self.interval = interval
        self.count = 0
                    
    def service(self):
        """
        Service all actions immediately and reset the internal counter to
        zero. 
        """
        [action() for action in self.actions]
        self.count = 0 
                        
    def cycle(self):
        """
        Increment the internal counter and if it is equal to the *interval*
        parameter, execute all actions. 
        """
        self.count += 1
        if self.count >= self.interval: 
            self.service() 
            
            
class Computer(object):
    
    reset_vector = None
    
    step = False 
    
    breakpoints = None 
    
    cycles = 0 
    
    limit = None 
    
    running = False 
    
    def __init__(self):   
        bank = memory.Bank() 
        bank.map(memory.Block(pages=0x01), 0x0000, BLOCK_ZERO_PAGE) 
        bank.map(memory.Block(pages=0x01), 0x0100, BLOCK_STACK) 
        bank.map(memory.Block(pages=0x04), 0x0200, BLOCK_SCRATCH) 
        bank.map(memory.Block(pages=0x1a), 0x0600, BLOCK_ROM) 
        bank.map(memory.Block(pages=0xdf), 0x2000, BLOCK_PROGRAM) 
        bank.map(memory.Block(pages=0x01), 0xff00, BLOCK_VECTOR) 
        
        self.mem = bank
        self.meta = tools.MetaSource() 
        self.cpu = x6502.CPU(self.mem) 
        
        self.terminal_output = io.TerminalOutput(self.mem) 
        self.terminal_input = io.TerminalInput(self.mem) 
        self.fpu = io.FPU(self.mem)
        actions = [self.terminal_output, self.terminal_input, self.fpu]
        self.timer = JiffyTimer(actions)
         
        self.breakpoints = set() 
        self.reset_vector = memmap.ROM_START - 1
        self.cpu.run_listeners += [self._idle_listener, self._monitor_listener]
        yapc.compiler_factory = lambda: yapc.Compiler(self) 
        
        self._reset()
        
    def _reset(self):
        self.mem.clear() 
        self.meta.reset() 
        
        self.mem.find(BLOCK_ROM).read_only = False
        self._fill_system_symbols()
        self._fill_aliases()
        self._assemble_rom() 
        self.mem.find(BLOCK_ROM).read_only = True 
        
        self.breakpoints = set() 
        self.cpu.pc = self.reset_vector
        
    def reset(self):
        self._reset() 
        self.run() 
        
    def run(self):
        self.cpu.exit = None 
        self.running = True 
        self.cycles = 0
        self.terminal_input.start() 
        try:
            while self.cpu.exit is None:
                if not self.cpu.i: 
                    self.timer.cycle()  
                self.cpu.next() 
                if self.step: 
                    self.cpu.exit = x6502.EXIT_STEP 
                # Break if the PC is about to be address
                elif self.cpu.pc + 1 in self.breakpoints:
                    self.cpu.exit = x6502.EXIT_BREAKPOINT
                self.cycles += 1
                if self.limit is not None and self.cycles >= self.limit: 
                    raise LimitExceededError('Execution limit reached at ' + 
                                             '{:d} cycles'.format(self.cycles))
        except: 
            self.cpu.exit = x6502.EXIT_TRAP 
            raise  
        finally: 
            self.terminal_input.stop() 
            self.step = False 
            self.running = False 
            self.timer.service() 
            
    def _idle_listener(self, address, instr):
        if address == self.meta['IDLE']:
            self.timer.service() 
            
    def _monitor_listener(self, address, instr):
        if address == self.meta['MONITOR']:
            self.cpu.exit = x6502.EXIT_MONITOR
        
    #--------------------------------------------------------------------------
    # Initializing methods
    #--------------------------------------------------------------------------    
    def _fill_system_symbols(self):
        """
        Add all elements in the memmap module to the symbol table. 
        """
        for symbol in dir(memmap): 
            if symbol[0] != '_' and symbol[-1] != '_':
                value = getattr(memmap, '__dict__')[symbol]
                self.meta.define_label(symbol, value, reserved=True)

    def _fill_aliases(self):
        """
        Add all elements in the alias module to the symbol table. 
        """
        for alias in dir(aliases): 
            if alias[0] != '_' and alias[-1] != '_':
                value = getattr(aliases, '__dict__')[alias]
                if isinstance(value, int): 
                    self.meta.define_alias(alias, value, reserved=True) 

    def _assemble_rom(self):
        """
        Assemble all routines in the rom module. 
        """
        asm = tools.Assembler(self.mem, origin=memmap.ROM_START, 
                              meta=self.meta)
        
        for routine_name in rom.__all__: 
            routine = getattr(rom, routine_name)
            routine(asm)
        asm.verify() 
                    
        
#------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------
class LimitExceededError(Exception):
    """
    CPU has executed more instructions than allowed. 
    """

        
        
        