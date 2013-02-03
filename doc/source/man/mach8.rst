mach8
=====

Synopsis
--------
mach [options]

Description
-----------
The Mach-8 is a 6502 emulator written in Python. It has no practical purpose. 

-p, --profile
   Import the ``cProfile`` module and run execution through the profiler. 
   A report is generated to standard output upon program completion. 
   
-v, --version
   Prints out version, RCS revision, and RCS date information.
   
-h, --help
   Prints out usage information. 
   
At the monitor prompt, type ``help`` for a list of the available commands. 

Packages
--------
HTML documentation of the code can be installed with the ``mach8-doc`` package
and is placed in /usr/share/doc/mach8/html.

Bugs
----
The emulator may run slower than the actual hardware but tests have yet to 
confirm or deny this claim. 

The non-GNU folks, in general, abhor info documents, and create manual pages 
instead. No info document of this manual page exists. 

See Also
--------
6502-addressing(7), 6502-instructions(7), mach8-aliases(7), 
mach8-expressions(7), mach8-memmap(7), mach8-rom(7)



