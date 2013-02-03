#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: memory.py 82 2011-11-16 02:08:42Z mcgann $
#------------------------------------------------------------------------------
"""
The memory system consists of two concrete classes. The :class:`Block` class 
represents segments of memory that are then combined together in the 
:class:`Bank` class to create a memory address space. :class:`Block` objects 
are added to a :class:`Bank` by mapping to an address location. This allows 
portions of memory to be easily cleared at runtime and can be useful in the 
future for loading in static memory blocks, like 'cartridges', as needed. The 
following code sample creates a new bank with separate blocks for the zero page,
stack, and the remaining area of memory::

   zero_page = memory.Block(pages=1) 
   stack     = memory.Block(pages=1)
   ram       = memory.Block(pages=254)   

   bank = memory.Bank()
   bank.map(zero_page, 0x0000, 'zero_page')
   bank.map(stack,     0x0100, 'stack')
   bank.map(ram,       0x0200, 'ram')

Blocks are given names when mapped and can later be referenced by this name.
If mapping regions is not desired, a block object alone can be used as a
full memory address space. 
"""
from array import array
from mach8 import vm
import itertools
import collections

#==============================================================================
# Storage
#==============================================================================
class Memory(object):
    """
    The :class:`Memory` class is the base class for :class:`Block` and
    :class:`Bank`. It provides get and set item support with slices, memory
    listeners, and read-only toggle support.
    
    .. data:: m[address]

      Gets or sets memory values at the specified *address*.

      Slice syntax can be used but varies from the usual rules in the
      following ways:

      * Only 1 and 2 are allowed for step values. If the step is 2, words
        are returned instead of bytes. Other values raise a
        :class:`ValueError`.
      * A start index is always required and a :class:`ValueError` is raised
        if it is missing. Unbounded slices don't make sense when working with
        a memory address space.
      * If the stop index is omitted, a single value is returned. This allows
        a word to be easily accessed with ``[x::2]`` syntax.
      * When storing a sequence of bytes or words with a slice, the length of
        the slice and the length of the sequence, converted to bytes, must be
        the same. If not, a :class:`ValueError` is raised.

      The memory that contains the following bytes::

      $1000: 34 12 78 56

      applies to the indexes listed below:

      ===================== ============================
      Index                 Result
      ===================== ============================
      ``[0x1000]``          ``0x34``
      ``[0x1000:0x1004]``   ``[0x34, 0x12, 0x78, 0x56]``
      ``[0x1000::2]``       ``0x1234``
      ``[0x1000:0x1004:2]`` ``[0x1234, 0x5678]``
      ===================== ============================

      Values stored into memory must fit within a unsigned byte or an
      :class:`OverflowError` is raised.
    """
    
    read_only = False 
    """
    If set to ``True``, writes to memory raise a :class:`ReadOnlyError`\.
    """
      
    load_listeners = None 
    """
    List of listeners that are notified when a byte is loaded from memory. A 
    listener is a callable that accepts two parameters --- :data:`address` and 
    :data:`value`.
    """
    
    store_listeners = None 
    """
    List of listeners that are notified when a byte is stored to memory. A 
    listener is a callable that accepts two parameters --- :data:`address` and 
    :data:`value`.
    """
    
    def __init__(self):
        self.load_listeners = list()
        self.store_listeners = list() 
        
    def __getitem__(self, index):
        if isinstance(index, slice):
            values = [self._getitem_single(i) for i in _slice_iterator(index)]
            # Combine into words if necessary.
            value = _get_values_sliced(index, values) 
        else:
            value = self._getitem_single(index)
        return value 
    
    def __setitem__(self, index, value):
        if isinstance(index, slice): 
            # Decompose into bytes if necessary. 
            values = _set_values_sliced(index, value) 
            for i, value in enumerate(values): 
                self._setitem_single(index.start + i, value) 
        else:
            self._setitem_single(index, value) 
            
    def _getitem_single(self, index):
        """
        Notifies listeners for each byte load and calls abstract _load
        """
        value = self._load(vm.size16(index)) 
        [listener(index, value) for listener in self.load_listeners]
        return value
     
    def _setitem_single(self, index, value):
        """
        Notifies listeners for each byte store and calls abstract _load. 
        Emits warning if read only. 
        """
        if self.read_only: 
            raise ReadOnlyError('Write {} to read-only location {}'
                                .format(vm.hex8(value), vm.hex16(index)))
        else:
            self._store(vm.size16(index), value)
            [listener(index, value) for listener in self.store_listeners]
    
    def _load(self, index):
        """
        Load a single byte.
        """
        raise NotImplementedError

    def _store(self, index, value):
        """
        Store a single byte. 
        """
        raise NotImplementedError
    
    def set_bits(self, address, bit_mask):
        """
        Sets the bits specified in *bit_mask* at *address*.
        """
        self[address] = (self[address] | bit_mask) & vm.BITS8 
        
    def clear_bits(self, address, bit_mask):
        """
        Clears the bits specified in *bit_mask* at *address*. 
        """
        self[address] = (self[address] & ~bit_mask) & vm.BITS8
           
    def is_set(self, address, bit_mask):
        """
        Returns ``True`` if the any bits in the *bit_mask* are set at
        *address*. 
        """
        return self[address] & bit_mask != 0             
        
class Block(Memory):
    """
    Creates a segment of memory that contains a number of 256-byte *pages*. 
    Pages are lazily allocated as needed. If *pages* is not greater than zero, 
    an :class:`AssertionError` is raised. 
    
    This class includes all the attributes and methods from :class:`Memory` 
    with the following additions:
    
    .. function:: len(b)

       Returns the size, in bytes, of this memory block.
    """

    def __init__(self, pages):
        assert pages > 0 
        super(Block, self).__init__() 
        self._page_count = pages 
        self._pages = collections.defaultdict(_create_page) 
        
    def __len__(self):
        return self._page_count * vm.PAGE_SIZE

    def _find_page(self, index):
        """
        Given an index, find the page that index belongs to and the offset 
        into that page.
        """
        page = index / vm.PAGE_SIZE
        offset = index % vm.PAGE_SIZE
        if page < 0 or page >= self._page_count: 
            raise IndexError('Invalid page for index: {}'
                             .format(vm.hex16(index))) 
        return page, offset 
            
    def _load(self, index):
        """
        Load a byte.
        """
        page, offset = self._find_page(index) 
        return self._pages[page][offset]
    
    def _store(self, index, value):
        """
        Store a byte. 
        """
        page, offset = self._find_page(index) 
        self._pages[page][offset] = value 
            
    def clear(self):
        """
        Zero out the contents of this block. If this block is read only, this
        method does nothing.
        """
        if not self.read_only: 
            self._pages.clear() 
    
    
class Bank(Memory):
    """
    Maps :class:`Block` objects into a memory address space. Initially,
    the :class:`Bank` object contains no blocks. Use :func:`map` to add
    blocks. It includes all the attributes and methods from :class:`Memory`
    with the following additions:

    .. attribute:: m[address]

       Raises an :class:`AddressBusWarning` if the *address* does
       not map to a block. 
    """

    def __init__(self):
        super(Bank, self).__init__() 
        self._blocks = list()
        self._block_by_name = dict() 

    def _find_block(self, address):
        """
        Given an address, find the block it is mapped to and the index into 
        that block. 
        """
        for block, start_address in self._blocks: 
            if (address >= start_address and 
                address < start_address + len(block)): 
                return block, address - start_address 
        raise AddressBusError('No such address: {}'.format(vm.hex16(address)))
    
    def _load(self, index):
        """
        Loads a byte. 
        """
        block, index = self._find_block(index)
        return block[index]
    
    def _store(self, index, value):
        """
        Stores a byte. 
        """
        block, index = self._find_block(index) 
        block[index] = value 
            
    def map(self, block, address, name):
        """
        Maps the *block* to the given *address* and assigns it with *name*.
        If the *name* is already in use, a :class:`ValueException` is raised.
        Raises an :class:`OverflowError` if the address is not in the allowable
        range. 
        """
        if name in self._block_by_name: 
            raise ValueError('Block with name {} already exists'.format(name)) 
        self._blocks += [(block, vm.size16(address))]
        self._block_by_name[name] = block 
        
    def clear(self):
        """
        Zero out all the contents of all blocks that are not marked as
        read only.  
        """
        [block.clear() for block, address in self._blocks]

    def find(self, block):
        """
        Returns a block, given an address or block name. Raises an 
        :class:`AddressBusError` if the address does not map to a block and 
        a :class:`KeyError` if there is no block by the given name. 
        """
        if isinstance(block, int): 
            address = block 
            return self._find_block(address)[0]
        else: 
            name = block
            return self._block_by_name[name]
        
#==============================================================================
# Inspector
#==============================================================================

def inspect(mem, start, stop):
    """
    Provides a hex dump of memory, *mem*, from *start* to *stop* address. A
    generator of strings is returned that provides one line of dump per
    iteration.

    Each line contains 16 bytes of memory which shows the current line
    address, hex values, and then ASCII values. ASCII values are shown
    if the byte value is in the range of (0x20, 0x7f], otherwise a '.'
    is shown.

    Full lines are always shown on paragraph boundaries. A dump with the
    range of ``0x08`` to ``0x09`` will show the line for ``0x00`` to ``0x0f``.
    Bytes not in the range are omitted with blanks.
    
    Values for *start* and *stop* that are out of range are truncated to 
    16-bits. If *start* is greater than *stop*, no values are returned. 

    For memory with the following::

      >>> mem[0x00:0x10] = vm.bstr('ABCDEFGHIJKLMNOP')                            
      >>> mem[0x10:0x20] = vm.bstr('abcdefghijklmnop')                            

    Calling ``inspect(mem, 0x00, 0x10)`` returns the following two strings::

      $0000: 41 42 43 44 45 46 47 48  49 4a 4b 4c 4d 4e 4f 50  ABCDEFGHIJKLMNOP  
      $0010: 61 62 63 64 65 66 67 68  69 6a 6b 6c 6d 6e 6f 70  abcdefghijklmnop  

    Calling ``inspect(mem, 0x08, 0x18)`` returns the following::

      $0000:                          49 4a 4b 4c 4d 4e 4f 50          IJKLMNOP  
      $0010: 61 62 63 64 65 66 67 68                           abcdefgh          
    """        
    columns = 16 
        
    # Always start at and print a 'full' line. 
    pos = start - (start % columns)
    column_stop = stop - (stop % columns) + columns

    while pos < column_stop and stop >= start:
        line = ['${:04x}:'.format(vm.mask16(pos))]
        
        # Hex portion
        for i in xrange(columns): 
            # Put a spacer after 8 bytes for readability
            if i == columns / 2: 
                line += [' ']
            value = mem[vm.mask16(pos)]
            # Print if within range, otherwise print blanks
            if pos >= start and pos <= stop: 
                line += [' {:02x}'.format(value)] 
            else:
                line += ['   ']
            pos += 1
            
        # Rewind for ASCII portion
        pos -= columns 
        line += ['  ']
        for i in xrange(columns): 
            value = mem[vm.mask16(pos)]
            # Print if within range, otherwise print blanks
            if pos >= start and pos <= stop: 
                if not _is_ascii_printable(value): 
                    strv = '.'
                else:
                    strv = chr(value)
                line += [strv]
            else:
                line += [' ']
            pos += 1
        yield ''.join(line).strip()

def dump(mem, start, stop):
    """
    Invokes :func:`inspect` and returns the result as one string. 
    """
    lines = list()
    for line in inspect(mem, start, stop): 
        lines += [line] 
    return '\n'.join(lines) 
    
#==============================================================================
# ProgramCounter
#==============================================================================
class ProgramCounter(object):
    """
    This class behaves as a program counter and maintains a pointer to a
    position in memory. The :meth:`load` and :meth:`store` methods are
    called to access memory at the current position and to advance the
    pointer.

    Creates a program counter backed by :class:`Memory` provided in
    *mem*\. The initial position of the program counter is set to
    *origin*. When the pointer's address is set to a value that does
    not fit within 16-bits, an :class:`OverflowError` is raised on the next 
    :meth:`load` or :meth:`store` operation. Normally, the program counter is 
    advanced after a :meth:`load` or :meth:`store` operation. If 
    *increment_first* is ``True``, the counter is incremented before loading 
    from memory.
    """

    position = 0 
    """
    Current address pointer of the program counter. 
    """
    
    increment_first = False 
    """
    If *increment_first* is ``True``, the counter is incremented before loading 
    from memory.
    """
    
    def __init__(self, mem, origin=0, increment_first=False):
        self.mem = mem
        self.position = origin
        self.increment_first = increment_first 
            
    def load(self):
        """
        Loads a byte from the current position and advances the position by
        one. If *increment_first* is ``True``, the position is advanced
        before loading the byte. Raises an :class:`OverflowError` if the 
        :attr:`position` is invalid. 
        """
        if self.increment_first: 
            self.position += 1
        value = self.mem[vm.size16(self.position)]
        if not self.increment_first: 
            self.position += 1
        return value
    
    def load2(self):
        """
        Loads a word from the current position and advances the position by
        two. If *increment_first* is ``True``, the position is advanced
        before loading the word. Raises an :class:`OverflowError` if the 
        :attr:`position` is invalid. 
        """
        if self.increment_first: 
            self.position += 1
        value = self.mem[vm.size16(self.position)::2]
        if self.increment_first: 
            self.position += 1 
        else: 
            self.position += 2
        return value 
    
    def store(self, value):
        """
        Stores a byte at the current position and advances the position by
        one. If *increment_first* is ``True``, the position is advanced
        before storing the byte. Raises an :class:`OverflowError` if the 
        :attr:`position` is invalid.
        """
        self.mem[self.position] = value
        self.position += 1
        
    def store2(self, value):
        """
        Stores a word at the current position and advances the position by
        two. If *increment_first* is ``True``, the position is advanced
        before storing the word. Raises an :class:`OverflowError` if the 
        :attr:`position` is invalid.
        """
        self.mem[self.position::2] = value
        self.position += 2
            
#==============================================================================
# Exceptions 
#==============================================================================

class AddressBusError(Exception):
    """
    A memory address in a :class:`Bank` was referenced that has no block
    mapped to it.
    """
    
class ReadOnlyError(Exception):
    """
    An attempt was made to write to memory that is marked as
    read-only.
    """

#==============================================================================
# Internal functions
#==============================================================================
def _create_page():
    """
    Allocates a zero filled 256 byte page of memory.
    """
    return array('B', itertools.islice(itertools.cycle((0,)), vm.PAGE_SIZE))

def _slice_iterator(index):
    """
    Return an iterator over the indexes based on the provided slice. Use a step
    of one since splits will happen later. 
    """
    if index.start is None: 
        raise ValueError('Slice must contain a start index')
    stop = index.stop 
    
    if stop is None: 
        stop = index.start + index.step
    return xrange(index.start, stop)
    
def _get_values_sliced(index, value):
    """
    Given the list of values retrieved in a get, combine into words if 
    necessary, or delist if no stop value provided.  
    """
    if index.step is None or index.step == 1: 
        pass
    elif index.step == 2:
        value = vm.to_words(value) 
    else:
        raise ValueError('Invalid step: {}'.format(index.step)) 
    
    if index.stop is None: 
        value = value[0]
    return value 

def _set_values_sliced(index, values):
    """
    Given the list of values to set, decompose from words to bytes if 
    necessary and turn into a list of no stop value provided. 
    """
    if index.start == None: 
        raise ValueError('Slice must contain a start index')
    if index.stop is None: 
        values = [values]
    
    if index.step is None or index.step == 1:
        pass
    elif index.step == 2:
        values = vm.from_words(values) 
    else:
        raise ValueError('Invalid step: {}'.format(index.step)) 
   
    stop = index.stop if index.stop is not None else index.start + index.step 
    if stop - index.start != len(values): 
        raise ValueError('Slice length mismatch')
     
    return values 

def _is_ascii_printable(value):
    return value >= 0x20 and value < 0x7f

        