from mach8.assembly import * 
from mach8 import memmap, memory, tools, vm, mach, x6502
from pprint import pprint 

comp = mach.Computer() 
mem = comp.mem
meta = comp.meta
a = tools.Assembler(mem, origin=memmap.PROGRAM_START, meta=meta) 
