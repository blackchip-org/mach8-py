:mod:`mach8.memory` --- Runtime memory store
============================================

This module includes the runtime memory store, memory inspector, and 
program counter. 

Storage
------- 

.. automodule:: mach8.memory 

.. autoclass:: mach8.memory.Memory 
  
   .. autoattribute:: read_only

   .. autoattribute:: load_listeners

   .. autoattribute:: store_listeners

.. autoclass:: mach8.memory.Block

   .. automethod:: mach8.memory.Block.clear

.. autoclass:: mach8.memory.Bank

   .. automethod:: mach8.memory.Bank.map

   .. automethod:: mach8.memory.Bank.clear
   
Inspector
---------

.. autofunction:: mach8.memory.inspect

.. autofunction:: mach8.memory.dump

ProgramCounter
--------------

.. autoclass:: ProgramCounter

.. autoattribute:: mach8.memory.ProgramCounter.position

.. automethod:: mach8.memory.ProgramCounter.load

.. automethod:: mach8.memory.ProgramCounter.load2

.. automethod:: mach8.memory.ProgramCounter.store

.. automethod:: mach8.memory.ProgramCounter.store2

Exceptions
----------

.. autoexception:: AddressBusError
		 
.. autoexception:: ReadOnlyError



