#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: console.py 111 2011-12-18 12:33:04Z mcgann $
#------------------------------------------------------------------------------
"""
Entry point for running the Mach-8 from a terminal console. 

The Mach-8 can be started from the command line by invoking the 
following:

  >>> python -m mach8.console

Invoking with ``-h`` or ``--help`` will display the following usage::

  usage: mach8 [options]
  
  optional arguments:
    -h, --help     show this help message and exit
    -p, --profile  execute using the profiler
    -v, --version  print version
"""
from mach8 import mach, monitor, x6502, version 
import argparse
import signal 

PROG = 'mach8' 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=PROG, 
                                     usage='%(prog)s [options]')
    parser.add_argument('-p', '--profile', action='store_true', 
                        help='execute using the profiler')
    parser.add_argument('-v', '--version', action='store_true', 
                        help='print version')
    
    def invalid_command_line(cls, message):
        print '{}: ERROR: {}\n'.format(PROG, message)
        parser.print_help()
        exit(2)
    
    argparse.ArgumentParser.error = invalid_command_line
    args = parser.parse_args()
    
    if args.version: 
        print version.full_string()
        exit(0)
    
    comp = mach.Computer() 

    def interrupt_handler(*args):
        # If the CPU is running, let it complete the current instruction
        # before returning to the monitor. 
        if comp.running:
            comp.cpu.exit = x6502.EXIT_STOP  
        else:
            raise KeyboardInterrupt
        
    signal.signal(signal.SIGINT, interrupt_handler) 
    
    comp.reset() 
    shell = monitor.Shell(comp) 
    if args.profile: 
        import cProfile
        cProfile.run('shell.run()', sort=2) 
    else:
        shell.run() 

    

