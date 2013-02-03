#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: monitor.py 146 2012-03-22 02:12:42Z mcgann $
#------------------------------------------------------------------------------
from mach8 import aliases, demo, vm, helptext, tools, mach, memmap, memory, \
    x6502, operations, version
import code
import os
import re
import sys


DEFAULT_LINES = 40 

def istart(comp, address):
    from instructions import jmp_abs 
    comp.mem[memmap.ISTART] = jmp_abs.opcode
    comp.mem[memmap.ISTART + 1::2] = address
    comp.cpu.sp = 0xff
    comp.cpu.push2(comp.meta['MONITOR'] - 1) 
    comp.cpu.pc = memmap.ISTART - 1
    comp.run() 

class Configuration(object):
    err = False
    _exe = False 
    term = False 
    lines = DEFAULT_LINES 
    
    def __init__(self, comp):
        self.comp = comp
        self._d = tools.Disassembler(comp.mem, meta=comp.meta) 
        
    def _run_listener(self, address, instruction):
        result = self._d.dump(address)
        print str(result) 
        
    @property
    def exe(self):
        return self._exe 
    
    @exe.setter
    def exe(self, value):
        if value and not self._exe: 
            self.comp.cpu.run_listeners += [self._run_listener]
        elif not value and self._exe: 
            self.comp.cpu.run_listeners.remove(self._run_listener) 
        self._exe = value     

class MonitorError(Exception):
    """ 
    Raised to show an error message.
    """
    
ERROR_TEXT_MAP = {
    ValueError:                     'Illegal argument(s)',
    TypeError:                      'Illegal argument(s)',
    AttributeError:                 'Syntax error',
    NameError:                      'Syntax error',
    KeyboardInterrupt:              'Stop',
    MonitorError:                   None, 
    mach.LimitExceededError:        'Limit exceeded',
    tools.SymbolConflictError:      'Already defined',
    tools.SymbolUndefinedError:     'Unknown symbol',
    tools.SymbolReservedError:      'Reserved symbol',
    tools.SymbolUnresolvedError:    'Unresolved references',
    x6502.StackError:               'Stack error',
}

class _Monitor(code.InteractiveConsole):
    
    def __init__(self, locals, config, comp, filename="<console>",
                 histfile=os.path.expanduser("~/.mach8-monitor-history")):
        code.InteractiveConsole.__init__(self, locals, filename)
        if histfile is not None:
            self.init_history(histfile)
        self.comp = comp
        self.config = config
        
    def init_history(self, histfile):
        import readline
        import atexit
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(histfile)
            except IOError:
                pass
            atexit.register(self.save_history, histfile)

    def save_history(self, histfile):
        import readline
        readline.write_history_file(histfile)
        
    def write(self, data):
        """
        Overridden to write to standard out instead. 
        """
        sys.stdout.write(data) 
        
    def showsyntaxerror(self, filename=''):
        self.write('? Syntax error\n')
        
    def showtraceback(self):
        exetype, message = sys.exc_info()[0:2]
        if self.config.err:
            code.InteractiveConsole.showtraceback(self)
        else:
            if exetype in ERROR_TEXT_MAP and ERROR_TEXT_MAP[exetype] is None:
                self.write('? {}\n'.format(message)) 
            else: 
                self.write('? {}\n'.format(ERROR_TEXT_MAP.get(exetype, 
                                           'Internal error')))

class Shell(object):
                    
    def __init__(self, comp):   
        
        self.comp = comp
        self.mem = comp.mem 
        self.cpu = comp.cpu
        self.meta = comp.meta
        self.memory_position = 0
        self.demo = demo.LessonPrinter(demo.TEXT)
        
        self.config = Configuration(comp) 
        self.asm = tools.Assembler(self.mem, memmap.PROGRAM_START, self.meta) 
        self.dsm = tools.Disassembler(self.mem, memmap.PROGRAM_START, self.meta) 
        self.dsm_util = tools.Disassembler(self.mem, 0, self.meta) 
        self.watches = set() 
        self.mem.store_listeners += [self._memory_watcher]
        
        self.locals = {
            'a':       self.asm, 
            'again':   self.demo.again, 
            'b':       self.b, 
            'back':    self.demo.back, 
            'c':       self.c, 
            'd':       self.d,
            'demo':    self.demo.next, 
            'exit':    quit,
            'f':       self.f, 
            'g':       self.g, 
            'help':    self.help, 
            'k':       self.k, 
            'l':       self.l, 
            'm':       self.m,  
            'n':       self.n, 
            'r':       self.r, 
            's':       self.s, 
            't':       self.t, 
            'q':       quit, 
            'quit':    quit, 
            'v':       self.v, 
            'version': self.version, 
            'w':       self.w, 
            'x':       self.x, 
            'y':       self.y, 
            'z':       self.z, 
            
            'comp':    self.comp, 
            'conf':    self.config, 
            'cpu':     self.cpu,
            'mem':     self.mem,
            'meta':    self.meta, 
        }        
        
        self.shortcuts = ('again', 'b', 'back', 'c', 'd', 'demo', 'exit', 'f', 
                          'g', 'help', 'k', 'm', 'n', 'r', 's', 't', 'q', 
                          'quit', 'v', 'version', 'w', 'x', 'y', 'z')
        
        self.helptext = { 
            self.asm:  helptext.MONITOR_A, 
            self.b:    helptext.MONITOR_B, 
            self.c:    helptext.MONITOR_C,
            self.d:    helptext.MONITOR_D, 
            self.f:    helptext.MONITOR_F, 
            self.g:    helptext.MONITOR_G, 
            self.k:    helptext.MONITOR_K, 
            self.l:    helptext.MONITOR_L,
            self.m:    helptext.MONITOR_M,
            self.n:    helptext.MONITOR_N,  
            self.r:    helptext.MONITOR_R, 
            self.s:    helptext.MONITOR_S,
            self.t:    helptext.MONITOR_T, 
            quit:      helptext.MONITOR_Q,
            self.v:    helptext.MONITOR_V, 
            self.w:    helptext.MONITOR_W, 
            self.x:    helptext.MONITOR_X, 
            self.y:    helptext.MONITOR_Y, 
            self.z:    helptext.MONITOR_Z, 
        }
        
        self.interactive = True 
        self.last_command = '' 
        self._frame = 0
        
    def _labels_at_address(self, address):
        label_set = self.meta.get_labels(address) 
        if len(label_set) > 0: 
            labels = ': ' + ', '.join(sorted(label_set))
        else:
            labels = ''
        return labels
                        
    def b(self, location=None):
        if location is None: 
            for address in sorted(self.comp.breakpoints): 
                print vm.hex16(address) + self._labels_at_address(address) 
        else: 
            address = self.meta[location] 
            if address == 0: 
                self.comp.breakpoints.clear() 
            elif address in self.comp.breakpoints: 
                self.comp.breakpoints.remove(address)
            else:
                self.comp.breakpoints.add(address) 
        
    def c(self):
        print str(self.cpu) 
        
    def d(self, begin=None, end=None):
        if begin is not None: 
            self.dsm.position = vm.mask16(self.meta[begin]) 
        if end is not None: 
            for result in self.dsm(begin, self.meta[end]):
                print str(result) 
        else: 
            line_count = 0
            done = False
            while not done: 
                lines = str(self.dsm.next()).splitlines() 
                for line in lines: 
                    print line 
                    line_count += 1
                    if line_count > self.config.lines: 
                        done = True
                        break         
        
    def f(self, pattern=None):
        if pattern is None: 
            pattern = '.*'
        symbols = sorted(list(self.meta.labels.keys()))
        lines = list() 
        for symbol in symbols: 
            if not re.search(pattern, symbol) is None: 
                lines.append(vm.hex16(vm.mask16(self.meta[symbol])) + 
                             " = " + symbol)
        print '\n'.join(lines) 
        
    def g(self):
        self.comp.run() 
        if self.cpu.exit != x6502.EXIT_MONITOR: 
            print str(self.cpu) 
            
    def help(self, command=None):
        if command is None: 
            print helptext.MONITOR
        elif command in self.helptext: 
            print self.helptext[command]
        else:
            help(command) 
              
    def _stop_at_frame(self, stop_at, notice):
        self.frame = 0
        def listener(address, instr):
            if instr.operation == operations.JSR: 
                self.frame += 1
            elif instr.operation == operations.RTS: 
                self.frame -= 1
            if self.frame == stop_at: 
                self.cpu.exit = x6502.EXIT_STEP 
        self.cpu.run_listeners += [listener]
        try:
            self.comp.run() 
        finally: 
            self.comp.cpu.run_listeners.remove(listener) 
            if self.cpu.exit == x6502.EXIT_STEP: 
                print notice
                print self.dsm_util.dump(self.cpu.pc + 1)
            else: 
                print str(self.cpu) 
                        
    def k(self):
        self._stop_at_frame(0, '[skip]')
            
    def l(self, name):
        import importlib 
        try:
            module = importlib.import_module(name) 
        except ImportError: 
            raise MonitorError('File not found')
        
        if hasattr(module, 'assemble'):
            asm = tools.Assembler(self.mem, origin=memmap.PROGRAM_START,
                                  meta=self.meta) 
            self.meta.clear(memmap.PROGRAM_START, memmap.HEAP)
            module.assemble(asm) 
        elif hasattr(module, 'compile'):
            self.meta.clear(memmap.PROGRAM_START, memmap.HEAP) 
            module.compile() 
        else: 
            raise MonitorError('Invalid program')
        
        # Reset back to binary math
        self.cpu.d = False
        
    def m(self, begin=None, end=None):
        if begin is None: 
            begin = self.memory_position
        begin = self.meta[begin]
        if end is None: 
            end = begin + vm.PAGE_SIZE - 1
        end = self.meta[end]
        for line in memory.inspect(self.mem, begin, end):
            print line
        self.memory_position = vm.mask16(end + 1) 
        
    def n(self):
        print self.dsm_util.dump(self.cpu.pc + 1)
        
    def r(self, address=None):
        if address is None: 
            address = self.meta['PROGRAM_START']
        address = vm.size16(self.meta[address])
        self.cpu.push2(self.meta['MONITOR'] - 1) 
        istart(self.comp, address)     
        if self.cpu.exit != x6502.EXIT_MONITOR: 
            print str(self.cpu) 
            
    def s(self, address=None):
        self.comp.step = True
        if address is None: 
            self.comp.run() 
        else: 
            istart(self.comp, self.meta[address]) 
        if self.cpu.exit == x6502.EXIT_STEP: 
            print '[step]'
            print self.dsm_util.dump(self.cpu.pc + 1)
        else: 
            print str(self.cpu) 
        
    def t(self):
        pos = self.cpu.sp + 1
        stack = self.cpu.stack_contents
        address = self.cpu.pc + 1
        routine = '<current>'
        items = 0
        while pos < len(stack):
            if stack[pos] == x6502.STACK_VALUE: 
                items += 1
                pos += 1
            elif stack[pos] == x6502.STACK_ADDRESS:
                print '{} {:2d} {}'.format(vm.hex16(address), items, routine) 
                return_address = self.mem[memmap.STACK_PAGE + pos::2] 
                if return_address + 1 == self.meta['MONITOR']:
                    break 
                address = return_address - 2
                jsr_to = self.mem[address + 1::2]
                routine = self.meta.get_argument(address) 
                if routine is None: 
                    routine = 'jsr ' + vm.hex16(jsr_to)
                else: 
                    routine = 'jsr ' + routine
                pos += 2
                items = 0
            else: 
                raise x6502.StackError('Corrupt stack') 
        
    def v(self):
        reference_lists = self.meta.get_unresolved().values()  
        if len(reference_lists) == 0:
            return
        results = []
        for reference_list in reference_lists: 
            results += [r for r in reference_list]
        for r in sorted(results, key=lambda x: x.address):  
                expr_str = '' if r.expr is None else ': ' + str(r.expr)
                print '{} {:3s} {:s}{:s}'.format(vm.hex16(r.address), r.type, 
                                                 r.ref, expr_str)
              
    def version(self):
        print 'Mach-8 Version {} ({}: {})'.format(version.string(), 
                                                  version.rcs_revision(), 
                                                  version.rcs_date())
        
    def w(self, location=None):
        if location is None: 
            for address in sorted(self.watches): 
                print vm.hex16(address) + self._labels_at_address(address)
        else: 
            address = self.meta[location] 
            if address == 0: 
                self.watches.clear() 
            elif address in self.watches: 
                self.watches.remove(address)
            else:
                self.watches.add(address) 
            
    def x(self):
        self._stop_at_frame(-1, '[exit]')
          
    def y(self, symbol):
        return self.meta[symbol]
    
    def z(self):
        self.comp.reset() 
        print str(self.comp.cpu) 
        print("\nType 'help' for the monitor command list.\n")
        
    def _memory_watcher(self, address, value):
        if address in self.watches: 
            print 'mem {} <-= {}{}'.format(vm.hex16(address), vm.hex8(value), 
                                           self._labels_at_address(address))  
            
    def run(self):
        if not self.interactive:
            self.engine = _Monitor(self.locals, self.config, self.comp, 
                                   histfile=None)
        else:
            self.engine = _Monitor(self.locals, self.config, self.comp)
        self.engine.push('from mach8.assembly import *') 
        self.engine.push('from pprint import pprint')
        
        print str(self.comp.cpu) 
        print("\nType 'help' for the monitor command list.\n")
              
        sys.ps1 = 'mach8> ' 
        try:
            while True: 
                try:
                    line = self.engine.raw_input(sys.ps1)
                    sys.ps1 = 'mach8> ' 
                    if not self.interactive: 
                        sys.stdout.write(line + '\n')
                    if line == '': 
                        line = self.last_command 
                    if line.strip() in self.shortcuts: 
                        self.engine.push(line + '()')
                    else:
                        self.engine.push(line)
                    self.last_command = line 
                except KeyboardInterrupt: 
                    pass 
        except EOFError:
            print '\n'
            
    
        
                        