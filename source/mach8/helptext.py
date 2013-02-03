#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: helptext.py 144 2012-03-19 22:09:00Z mcgann $
#------------------------------------------------------------------------------
"""
Help text for monitor commands. 
"""

MONITOR = """
=== Monitor Commands ===

a: Assemble
b: Breakpoints 
c: CPU status
d: Disassemble
f: Find symbol 
g: Go (resume execution)
k: sKip next routine
l: Load program 
m: Memory dump
n: show Next
r: Run  
s: Step
t: backTrace 
q: Quit
v: Verify references
w: Watch memory
x: eXit from routine 
y: sYmbol lookup
z: Zero state (reset) 

=== Bound objects ===

cpu:  mach8.x6502.CPU 
conf: mach8.monitor.Configuration
mem:  mach8.memory.Bank
meta: mach8.tools.MetaSource

- Type 'help(x)' for more information on command or object 'x'.
- Blank line repeats previous command. 
"""

MONITOR_A = """
=== Assemble ===

a(instruction, [arg])
    Assemble instruction at the current address. Argument is optional if the
    instruction does not take an argument. 

a(name)
    Define a label at the current address. 
    
a.alias(name, value) 
    Alias a symbolic name to an arbitrary value. 
    
a.auto_label()
    Return a unique label name -- useful in macro definitions. 
    
a.data(*args) 
    Enter data elements at the current address. Elements can be ASCII strings, 
    or numeric values. 
    
a.label(name, address)
    Define a label at the specified address. 
    
a.macro(function, [*args])
    Invoke a macro. 
    
a.position
    Current assembly address. 
    
a.remark(text) 
    Add a descriptive comment at the current assembly address. 
"""

MONITOR_B = """
=== Breakpoints ===

b(location)
    Add/remove breakpoint at address or symbol. 

b
    List all breakpoints. 
    
b(0)
    Clear all breakpoints. 
"""
    
MONITOR_C = """
=== CPU status === 

pc = Program counter
sr = Status register (flag contents) 
ac = Accumulator register
xr = X index register
yr = Y index register
sp = Stack pointer

n  = Sign (negative) flag
v  = Overflow flag
b  = Break flag
d  = Decimal (BCD) math flag
i  = Interrupt disable flag 
z  = Zero (equals) flag
c  = Carry flag
"""

MONITOR_D = """
=== Disassemble ===

d(begin=None, end=None)    
    Disassemble from begin to end. If end is not specified, show 'conf.lines' 
    of output. If begin is not specified, continue disassembly from previous 
    'd' command. 
    
d 
    Show next 'conf.lines' of output.  
"""

MONITOR_F = """
=== Find symbol ===

f(pattern)
    Find all symbols that contain the specified pattern.
    
f
    Find all symbols. 
"""

MONITOR_G = """
=== Go ===

g
    Continue execution at the location of the program counter. 
"""

MONITOR_K = """
=== sKip next routine ===

k
    If the next instruction is a 'jsr', run that routine and stop when it
    returns. Otherwise, this behaves as a step command. 
"""

MONITOR_L = """
=== Load program ===

l('asm.name')   
    Load assembly module at PROGRAM_START.

l('yap.name')   
    Load YAP module at PROGRAM_START.
"""

MONITOR_M = """
=== Memory dump ===

m(begin=None, end=None)    
    Show memory from begin to end. If end is not specified, show a page of 
    memory. If begin is not specified, continue memory dump from previous 
    'm' command. 
    
m 
    Show next page of memory. 
"""

MONITOR_N = """
=== show Next ===

n
    Show the next instruction that will be executed.
"""

MONITOR_R = """
=== Run ===

r(location)
    Run program at address or symbol as if jumping to a subroutine. 
    
r 
    Run program at PROGRAM_START.
"""

MONITOR_S = """
=== Step ===

s
    Continue execution and stop after executing the next instruction.
"""

MONITOR_T = """
=== backTrace ==

t
    Shows a trace of each execution frame. Columns are: 
    
    - Address where jsr was invoked, or address of <current> frame
    - Number of data items on the stack for this frame 
    - jsr instruction that was invoked, or <current>
""" 
    
MONITOR_Q = """
=== Quit ===

q
    Quit monitor -- 'quit' and 'exit' can also be used. 
"""

MONITOR_V = """
=== Verify references ===

v
    Shows any unresolved references by listing the address where the reference
    is, the type of reference, and the label name (followed by the expression
    if found within). Types of references are as follows: 
    
    - abs: Absolute 16-bit address
    - zp:  Absolute 8-bit zero page address
    - rel: Relative 8-bit displacement 
    - val: 8-bit value
"""

MONITOR_W = """
=== Watch memory ===

w(location)
    Add/remove a memory watch at address or symbol. 

w
    List all watches. 
    
w(0)
    Clear all watches. 
"""

MONITOR_X = """
=== eXit from routine ===

x
    Continue running and stop after exiting the current routine. 
"""

MONITOR_Y = """
=== sYmbol lookup ===

y(symbol)
    Lookup the address for the given symbol. 
"""

MONITOR_Z = """
=== Zero state ===

z
    Warm-restart the Mach-8. 
"""



