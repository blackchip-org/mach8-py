#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: x6502.py 73 2011-10-27 12:44:53Z mcgann $
#------------------------------------------------------------------------------
from mach8 import addressing as am, operations, memmap, memory, vm

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------
A  = 'A' 
X  = 'X'
Y  = 'Y'
SP = 'SP'
SR = 'SR'

C = 'C'
Z = 'Z'
I = 'I' 
D = 'D' 
B = 'B' 
V = 'V'
N = 'N' 

EXIT_BREAK = 'break'
"""
CPU received a :data:`BRK` instruction. 
"""

EXIT_STOP = 'stop'
"""
A :class:`StopProcessor` exception was raised. 
"""

EXIT_STEP = 'step'
"""
CPU is being debugged and stopped after execution of an instruction. 
"""

EXIT_TRAP = 'trap' 
"""
An unexpected exception was raised during execution. 
"""

EXIT_MONITOR = 'monitor'
"""
PC was equal to the pseudo-entry point for the monitor. 
"""

EXIT_BREAKPOINT = 'breakpoint'
"""
PC was equal to a breakpoint address. 
"""

#------------------------------------------------------------------------------
# Instruction
#------------------------------------------------------------------------------
class Instruction(object):
    """
    CPU instruction. 
    """
    
    opcode = None 
    """
    Byte value that denotes this instruction. 
    """
    
    operation = None 
    """
    Constant from :mod:`mach8.operations`
    """
    
    addressing_mode = None
    """
    Constant from :mod:`mach8.addressing`
    """
    
    execute = None
    """
    Function to run to execute this instruction, from :mod:`mach8.executors`
    """ 
    
    def __init__(self, opcode, operation, addressing_mode, execute):
        self.opcode = opcode
        self.operation = operation
        self.addressing_mode = addressing_mode
        self.execute = execute
        
    def __str__(self):
        return str(self.instruction) + "_" + str(self.addressing_mode) 
    
def _nul(cpu, i):
    raise IllegalInstructionError('NUL instruction')

NUL = Instruction(0xff, '?XX', am.IMP, _nul) 

#------------------------------------------------------------------------------
# Instruction set
#------------------------------------------------------------------------------
def get_instruction_set():
    """
    Returns a dictionary containing all of the instructions recognized by the 
    x6502 CPU. Values are :class:`Instruction` objects keyed by opcode. 
    """
    from mach8 import instructions
    
    instruction_set = dict() 
    for op_name in instructions.__all__: 
        op = getattr(instructions, op_name)
        if op.opcode in instruction_set: 
            raise ValueError('Duplicate opcode: {}', vm.hex8(op.opcode)) 
        instruction_set[op.opcode] = op
    return instruction_set

#------------------------------------------------------------------------------
# CPU
#------------------------------------------------------------------------------
STACK_VALUE = 'value' 
STACK_ADDRESS = 'address'
STACK_NONE = 'none' 

class CPU(object):
    """
    The x6502 central processing unit. Uses :class:`memory 
    <mach8.memory.Memory>` backed by *mem*. 
    """
    
    exit = None
    """
    Set this attribute to one of the :ref:`exit codes <exit_codes>` to cause
    the CPU to stop. Is set to ``None`` when executing normally. 
    """

    flag_listeners = None 
    """
    List of listeners to be called when a flag is set or cleared. Listeners
    should be callables that accept two arguments --- name and value (bool). 
    """
    
    register_listeners = None 
    """
    List of listeners to be called when a value is stored to a register. 
    Listeners should be callables that accept two arguments --- name and value. 
    """
    
    run_listeners = None 
    """
    List of listeners to be called when before each instruciton is executed.
    Listeners should be callables that accept two arguments --- 
    address, and :class:`Instruction`. 
    """
    
    def __init__(self, mem):
        self._mem = mem 
        self._pc = memory.ProgramCounter(self.mem, increment_first=True) 
        self._registers = {
            A : 0x00,
            X : 0x00,
            Y : 0x00,
            SP: 0xff,
            SR: 0x20,   
        }
        self.register_listeners = list() 
        self.flag_listeners = list() 
        self.run_listeners = list() 
        self.frame_listeners = list() 
        self.stack_listeners = list() 
        self._instruction_set = get_instruction_set() 
        
        self.stack_contents = [STACK_NONE] * 256
        
    def fetch(self):
        """
        Increments the program counter by one and loads the byte at that
        location. Raises an :class:`OverflowError` if the program counter
        is not valid.  
        """
        return self._pc.load() 
    
    def fetch2(self):
        """
        Similar to :meth:`fetch`, but loads a word. Rasies an 
        :class:`OverflowError` if the program counter is not valid. 
        """
        return self._pc.load2() 
    
    def next(self):
        """
        Executes the next instruction.
        """
        try:
            opcode = self.fetch()
            address = self.pc 
            try:
                instruction = self._instruction_set[opcode] 
            except KeyError: 
                raise IllegalInstructionError('Invalid opcode: {}' 
                                              .format(vm.hex8(opcode))) 
            instruction.execute(self, instruction.operation, 
                                instruction.addressing_mode)
            [listener(address, instruction) for listener in self.run_listeners]
        except: 
            self.exit = EXIT_TRAP 
            raise   
        
    def _push(self, value, type):
        self.mem[memmap.STACK_PAGE + self.sp] = vm.size8(value) 
        self.stack_contents[self.sp] = type
        self.sp = (self.sp - 1)  & vm.BITS8 
        if self.sp == vm.BITS8: 
            raise StackError('Stack overflow')
        
    def push(self, value):
        """
        Pushes an unsigned byte, *value*, to the stack. Raises an 
        :class:`OverflowError` if *value* is not an unsigned byte. Raises a 
        :class:`StackError` on a stack overflow.
        """
        self._push(value, STACK_VALUE) 
        
    def push2(self, value):
        """
        Pushes an unsigned word, *value*, to the stack. Raises an 
        :class:`OverflowError` if *value* is not an unsigned word. Raises a
        :class:`StackError` on a stack overflow. 
        """ 
        self._push(vm.hb(value), STACK_ADDRESS)
        self._push(vm.lb(value), STACK_ADDRESS) 
        
    def _pull(self, type):
        self.sp = (self.sp + 1) & vm.BITS8 
        if self.sp == 0: 
            raise StackError('Stack underflow')
        if self.stack_contents[self.sp] != type: 
            raise StackError('Corrupt stack, expected {} but pulled {}, sp: {}'
                             .format(type, self.stack_contents[self.sp], 
                                     vm.hex8(self.sp)))
            
        return self.mem[memmap.STACK_PAGE + self.sp] 
    
    def pull(self):
        """
        Pulls (pops) a byte from the stack. Raises a :class:`StackError` on 
        a stack underflow. 
        """ 
        return self._pull(STACK_VALUE) 

    def pull2(self):
        """
        Pulls (pops) a word from the stack. Raises a :class:`StackError` on 
        a stack underflow. 
        """         
        return vm.word(self._pull(STACK_ADDRESS), self._pull(STACK_ADDRESS)) 
            
    def _set_register(self, name, value, on=0):
        value = vm.size8(value)
        self._registers[name] = value | on
        [event(name, value) for event in self.register_listeners]

    def _set_flag(self, name, value, bit):
        if value: 
            self._registers[SR] |= bit 
        else:
            self._registers[SR] &= ~bit
        self._registers[SR] |= vm.BIT5
        [event(name, value) for event in self.flag_listeners]
            
    @property
    def mem(self):
        """
        :class:`Memory <mach8.memory.Memory>` address space this CPU is using. 
        """
        return self._mem 
    
    @property 
    def pc(self):
        """
        Program counter. 
        """
        return self._pc.position
        
    @pc.setter
    def pc(self, value):
        self._pc.position = value 
                   
    @property 
    def a(self):
        """
        Accumulator register. 
        """
        return self._registers[A]
        
    @a.setter
    def a(self, value):
        self._set_register(A, value) 
            
    @property 
    def x(self):
        """
        X register.
        """
        return self._registers[X]
        
    @x.setter
    def x(self, value):
        self._set_register(X, value)   
    
    @property 
    def y(self):
        """
        Y register. 
        """
        return self._registers[Y]
        
    @y.setter
    def y(self, value):
        self._set_register(Y, value)  
    
    @property 
    def sp(self):
        """
        Stack pointer. 
        """
        return self._registers[SP]
        
    @sp.setter
    def sp(self, value):
        self._set_register(SP, value) 
        
    @property 
    def sr(self):
        """
        Status register which contains all the flag bits. Bits 5 is hard-wired 
        on and its value cannot be changed.  
        """
        return self._registers[SR]
        
    @sr.setter
    def sr(self, value):
        self._set_register(SR, value, on=vm.BIT5)
    
    @property
    def c(self):
        """
        Carry flag, bit 0.
        
        * Addition: Set if there a left over carry bit after performing the
          operation. This flag should be cleared before starting
          addition. If set, this adds one to the result.
        
        * Subtraction: Acts as the 'borrow' flag and is the inverse of the
          carry. Clear if there is a bit that needs to be borrowed after
          performing the operation. This flag should be set before starting
          subtraction. If clear, this subtracts one from the result.
        
        * Shifting: Holds the value of the bit that was shifted out.
        
        Branches can be made based on the status of this flag using the
        :data:`bcc` and :data:`bcs` operations.
        """
        return self.sr & vm.BIT0 != 0 
    
    @c.setter
    def c(self, value):
        self._set_flag(C, value, vm.BIT0)
        
    @property
    def z(self):
        """
        Zero flag, bit 1.
        
        Set when a register is loaded with a zero value.
        """
        return self.sr & vm.BIT1 != 0 
    
    @z.setter
    def z(self, value):
        self._set_flag(Z, value, vm.BIT1)
        
    @property
    def i(self):
        """
        Interrupt disable flag, bit 2.
        
        Normally this flag is used to ignore the state of the IRQ line and
        is set to prevent the CPU from running the interrupt service
        routine. Since interrupts are not implemented in the Mach-8, this flag
        is used instead to block the :class:`JiffyTimer` from servicing
        registered actions.
        """
        return self.sr & vm.BIT2 != 0 
    
    @i.setter
    def i(self, value):
        self._set_flag(I, value, vm.BIT2)
        
    @property
    def d(self):
        """
        Decimal math (BCD) flag, bit 3.
        
        When set, addition and subtraction is based on BCD numbers instead
        of binary numbers. When clear, ``$09 + $01 = $0A``, and when set,
        ``$09 + $01 = $10``.
        """
        return self.sr & vm.BIT3 != 0 
    
    @d.setter
    def d(self, value):
        self._set_flag(D, value, vm.BIT3)
        
    @property
    def b(self):
        """
        Break flag, bit 4.
        
        In the Mach-8, this flag is set when a break instruction is
        encountered and the CPU is stopped. On a real 6502, this generates
        an interrupt.
        """
        return self.sr & vm.BIT4 != 0 
    
    @b.setter
    def b(self, value):
        self._set_flag(B, value, vm.BIT4)
        
    @property
    def v(self):
        """
        Overflow flag, bit 6.
        
        This flag is set when an arithmetic operation causes an overflow on
        a signed value. For example, the operation ``$7F + $01`` sets the
        bit since the answer, 128, is too large to fit in a single signed
        byte.
        """
        return self.sr & vm.BIT6 != 0 
    
    @v.setter
    def v(self, value):
        self._set_flag(V, value, vm.BIT6)
        
    @property
    def n(self):
        """
        Sign (negative) flag, bit 7.
        
        Set to the match bit 7 of a value when a register is set.
        """
        return self.sr & vm.BIT7 != 0 
    
    @n.setter
    def n(self, value):
        self._set_flag(N, value, vm.BIT7)
        
    def __str__(self):
        reason = '[' + self.exit + ']\n' if self.exit is not None else ''
        return ('{reason:} pc  sr ac xr yr sp  n v - b d i z c\n'
                '{pc:04x} {sr:02x} {a:02x} {x:02x} {y:02x} {sp:02x} '
                ' {n:} {v:} {on:} {b:} {d:} {i:} {z:} {c:}'.format(
                reason = reason,
                pc = self.pc, 
                sr = self.sr, 
                a  = self.a, 
                x  = self.x, 
                y  = self.y, 
                sp = self.sp, 
                n  = bit_char(self.n),
                v  = bit_char(self.v), 
                on = bit_char(True),
                b  = bit_char(self.b), 
                d  = bit_char(self.d), 
                i  = bit_char(self.i), 
                z  = bit_char(self.z), 
                c  = bit_char(self.c)))        
        
#------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------
class StopProcessor(Exception):
    """
    Used in debugging to force the CPU to stop execution immediately. 
    """
    
class IllegalInstructionError(Exception):
    """
    An invalid opcode was encountered. 
    """
    
class StackError(Exception):
    """
    Either one of the following occurred: 
    
    * A push operation when the stack was full. 
    * A pull operation when the stack was empty. 
    * An RTS operation without cleaning up the stack. 
    """ 
    
#------------------------------------------------------------------------------
# Internal functions
#------------------------------------------------------------------------------
bit_char = lambda value: '*' if value else '.'
