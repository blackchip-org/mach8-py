#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: tools.py 146 2012-03-22 02:12:42Z mcgann $
#------------------------------------------------------------------------------
from mach8 import addressing as am, expression, memory, vm, x6502
import collections

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------

REFERENCE_ABSOLUTE = 'abs'
REFERENCE_ZERO_PAGE = 'zp'
REFERENCE_RELATIVE = 'rel'
REFERENCE_VALUE = 'val'

AM_ADDRESS_16  = (am.ABS, am.ABX, am.ABY, am.IND)
AM_ADDRESS_8   = (am.ZP,  am.ZPX, am.ZPY, am.IZX, am.IZY) 
AM_NO_ARGUMENT = (am.IMP, am.ACC) 


#------------------------------------------------------------------------------
# MetaSource
#------------------------------------------------------------------------------

class MetaSource(object):
    """
    Provides symbolic and metadata support for the assembler and disassembler 
    and contains the following:
    
    * **Labels**: Symbolic names for memory locations.
    * **Aliases**: Symbolic names for arbitrary numeric values.
    * **References**: Uses of symbolic names or branch targets.
    * **Arguments**: Text that should be displayed for the instruction's 
      argument instead of the raw value.
    * **Remarks**: Comments to be displayed at a memory location.
    * **Data**: Descriptive text that should be displayed instead of raw memory 
      values.
    
    .. describe:: m[symbol]
    
       Looks up the address or alias value for the given *symbol*. If *symbol* 
       is ``None`` or is numeric, the value of *symbol* is returned. If 
       *symbol* is not defined, a :class:`SymbolUndefinedError` is raised.

    .. describe:: symbol in m

       Returns ``True`` if *symbol* is a defined label or alias.

    .. describe:: symbol not in m

       Returns ``False`` if *symbol* is a defined label or alias.

    .. describe:: del m[symbol]

       Shorthand for :meth:`undefine`.
    """

    def __init__(self):
        self.labels = dict()
        self.addresses = collections.defaultdict(set)
        self.aliases = dict() 
        self.reserved = set() 
        self.reference_counts = collections.defaultdict(int) 
        self.references = collections.defaultdict(set) 
        self.unresolved = collections.defaultdict(list)
        self.arguments = dict()
        self.remarks = collections.defaultdict(list)  
        self.data = dict() 
        self.next_auto_label = 1
    
    def reset(self):
        self.__init__() 
        
    def _check_symbol(self, name, reserved=False):
        """
        Check entry to the against label and symbol dictionaries. Add to 
        reserved set and create a reference count entry if necessary. Determine 
        if this definition resolved an unresolved reference. 
        """
        if name in self.labels or name in self.aliases or name in self.reserved: 
            raise SymbolConflictError('Symbol already defined (' + name + ')')
        if reserved: 
            self.reserved.add(name) 
        resolvable = self.unresolved.pop(name, list()) 
        # If this resolves a reference, counts already exist. 
        if len(resolvable) == 0: 
            self.reference_counts[name] = 0
        return resolvable
    
    def _unresolved_reference(self, name, address, type, expression=None):
        """
        Increase the reference count for this symbol and append an entry
        to the list in the unresolved dict. 
        """
        self.reference_counts[name] += 1
        # For the address, store the actual location to where the reference
        # is located. Since the address passed in is the address of the 
        # instruction, add one to skip over the opcode. 
        self.unresolved[name] += [UnresolvedReference(name, address + 1, type, 
                                                      expression)]
        
    def define_label(self, name, address, reserved=False):
        """
        Defines a label, *name*, for *address*. Raises a 
        :class:`SymbolConflictError` if an alias or label with the same name is 
        already defined. Raises a :class:`OverflowError` if *address* is not a 
        16-bit value. If *reserved* is ``True``, the alias cannot be removed 
        once added. If this definition resolves references, a list of addresses 
        where unresolved references exist is returned, otherwise an empty list 
        is returned.
        """
        address = vm.size16(address) 
        resolvable = self._check_symbol(name, reserved) 
        self.labels[name] = address
        self.addresses[address].add(name)
        return resolvable
    
    def define_alias(self, name, value, reserved=False):
        """
        Defines an alias, *name*, for *value*. Raises a 
        :class:`SymbolConflictError` if an alias or label with the same name is 
        already defined. If *reserved* is ``True``, the alias cannot be removed 
        once added. If this definition resolves references, a list of addresses 
        where unresolved references exist is returned, otherwise an empty list 
        is returned.
        """
        resolvable = self._check_symbol(name, reserved) 
        self.aliases[name] = self.lookup(value)
        return resolvable
        
    def reserve(self, name):
        """
        Reserves the symbol *name* without assigning it to a value. Raises a 
        :class:`SymbolConflictError` if the symbol is already defined. Once 
        reserved, the symbol cannot be undefined.
        """
        self._check_symbol(name, reserved=True)
        
    def auto_label(self):
        """
        Returns a unique label name. See :meth:`Assembler.auto_label() 
        <mach8.tools.Assembler.auto_label>`.
        """
        label = '@' + str(self.next_auto_label)
        self.next_auto_label += 1
        return label
                
    def __contains__(self, name):
        return (name in self.labels or name in self.aliases)
        
    def lookup(self, name, default=Exception):
        """
        Looks up the address or alias value for the given *symbol*. If 
        *symbol* is ``None`` or is numeric, the value of *symbol* is returned. 
        If *symbol* is not defined, *default* is returned if specified, 
        otherwise a :class:`SymbolUndefinedError` is raised.
        """
        if name is None: 
            return None 
        if isinstance(name, int): 
            value = name
            return value
        if name in self.labels: 
            return self.labels[name]
        if name in self.aliases:
            return self.aliases[name]
        if default is Exception: 
            raise SymbolUndefinedError('Symbol undefined (' + name + ')')
        return default 
        
    def __getitem__(self, name):
        return self.lookup(name) 
    
    def get_labels(self, address):
        """
        Returns a set of all labels defined at *address*. If no labels are 
        defined at *address*, an empty set is returned.
        """
        return self.addresses[address]
    
    def _expression_reference(self, expression, address, type):
        """
        Find all symbols referenced in the expression. Create an entry
        in the reference dict for each symbol found. Set the argument text for
        this instruction to the textual representation of this expression. If 
        all symbols exist, evaluate the expression and return the value, 
        otherwise return zero and defer the evaluation until all unresolved 
        references are defined.  
        """
        references = expression.references(self) 
        defer_eval = False 
        try:
            [self[ref] for ref in references]
            defer_eval = False
        except SymbolUndefinedError: 
            defer_eval = True
        # Evaluate before creating references in case an exception is raised
        # during evaluation. 
        value = 0 if defer_eval else expression.eval(self) 
        for ref in references: 
            self.add_reference(ref, address, type, expression)
        self.set_argument(address, str(expression)) 
        return value 
    
    def _symbol_reference(self, name, address, type, function):
        """
        If the symbol exists, increase the reference count and return the
        symbol's value. Otherwise, add an entry to the undefined references
        dict and return zero. Set the argument text for this instruction to 
        the name of the symbol. 
        """
        try:
            value = self[name] 
            self.reference_counts[name] += 1
        except SymbolUndefinedError: 
            self._unresolved_reference(name, address, type, function)
            value = 0
        self.references[address].add(name)
        self.set_argument(address, name)         
        return value 
    
    def add_reference(self, ref, address, type, expr=None):
        """
        Adds a reference to *ref* from *address*. Value for *ref* can be either 
        a symbol or an address. The *type* of reference is one of the 
        following:

        ============================= =========================================
        Constant                      Description
        ============================= =========================================
        ``tools.REFERENCE_ABSOLUTE``  A 16-bit absolute address.
        ``tools.REFERENCE_RELATIVE``  An 8-bit address displacement.
        ``tools.REFERENCE_ZERO_PAGE`` An 8-bit absolute zero page address.
        ``tools.REFERENCE_VALUE``     An 8-bit value from an expression which 
                                      must be deferred.
        ============================= =========================================

        If *ref* is a symbol that does not exist, an unresolved reference entry 
        is created and can be retrieved via :meth:`get_unresolved`. If *expr* 
        is specified, this :ref:`expression <code_expression>` should be 
        reevaluated once all references are resolved.
        
        If resolved, returns the value of the reference, otherwise returns 
        zero.  
        """        
        if isinstance(ref, int): 
            referenced_address = ref
            # The actual address should be displayed, not the displacement
            if type == REFERENCE_RELATIVE: 
                self.set_argument(address, vm.hex16(referenced_address))
            return referenced_address
        elif isinstance(ref, expression.Expression): 
            expr = ref
            return self._expression_reference(expr, address, type)
        else:
            name = ref
            return self._symbol_reference(name, address, type, expr)
        
    def get_references(self, address):
        """
        Returns a set of all references at *address*. References can either be 
        strings (labels) or numerics (addresses). If there are no references at 
        *address*, an empty set is returned.
        """
        return self.references[address]
        
    def get_unresolved(self):
        """
        Returns a dict where the keys are symbols that are undefined and the 
        values are addresses containing unresolved references to the keyed 
        symbol. If there are no outstanding unresolved references, returns an 
        empty dict.
        """
        return self.unresolved
        
    def set_argument(self, address, text):
        """
        Sets the *text* for the argument of the instruction at *address*.
        """
        self.arguments[address] = text
        
    def get_argument(self, address):
        """
        Returns the text for the argument of the instruction at *address*. If 
        no argument text has been set, returns ``None``.
        """
        return self.arguments.get(address, None)
        
    def set_data(self, data):
        """
        Defines a block of memory defined by *data* of type :class:`Data`. This 
        method will invalidate any other data blocks that overlap with this 
        block by setting is ``valid`` attribute to ``False``.
        """
        for address in xrange(data.address, data.address + data.length):
            if address in self.data: 
                self.data[address].valid = False 
            self.data[address] = data
        
    def get_data(self, address):
        """
        Returns the :class:`Data` block this memory *address* belongs to or 
        ``None`` if it does not belong to a data block. If the returned data 
        block has its ``valid`` attribute set to ``False``, it should be 
        treated the same as if this method returned ``None``.
        """
        return self.data.get(address, None) 
        
    def add_remark(self, address, text):
        """
        Adds a descriptive comment, *text*, at *address*. If other remarks 
        already exists at *address*, this remark is append to the end of the 
        others.
        """
        self.remarks[address] += [text]
        
    def get_remarks(self, address):
        """
        Returns a list of all remarks assigned to *address*. If no remarks are 
        found, an empty list is returned.
        """
        return self.remarks[address]
        
    def clear_remarks(self, address):
        """
        Removes any remarks assigned to *address*.
        """
        self.remarks[address] = list() 
        
    def undefine(self, symbol):
        """
        Removes either the label or alias *symbol*. If *symbol* is not defined, 
        a :class:`SymbolUndefinedError` is raised. If *symbol* is reserved, a 
        :class:`SymbolReservedError` is raised. If *symbol* is still in use, 
        a :class:`SymbolReferencedError` is raised.
        """
        try:
            if symbol in self.reserved:
                raise SymbolReservedError('Cannot remove reserved symbol: ' + 
                                          symbol)
        except KeyError:
            raise SymbolUndefinedError('Symbol undefined: ' + symbol)
        if self.reference_counts[symbol] != 0: 
            raise SymbolReferencedError('Symbol in use: ' + symbol)
        
        if symbol in self.labels:
            address = self.labels[symbol]
            del self.labels[symbol]
            self.addresses[address].remove(symbol)
        elif symbol in self.aliases:
            del self.aliases[symbol]
        else:
            assert False             
        del self.reference_counts[symbol]
        
    def __delitem__(self, symbol):
        self.undefine(symbol) 
        
    def clear(self, begin, end=None, exclude=None):
        """
        Removes all labels, arguments, data, references, and remarks found in 
        memory between *begin* (inclusive) and *end* (exclusive). If *end* is 
        not specified, only the *begin* address is cleared. If specified, the 
        collection of labels in *exclude* will not be cleared if found. 
        Reserved labels and labels which are still referenced are not cleared 
        and no exceptions are raised.
        """
        if end is None: 
            end = begin + 1
        if exclude is None: 
            exclude = set() 
        # Remove references first in case there is a reference to a label
        # that will be cleared.  
        for address, references in self.references.items(): 
            if address >= begin and address < end: 
                for reference in references:
                    self.reference_counts[reference] -= 1
                del self.references[address]
                
        for label, address in self.labels.items(): 
            if address >= begin and address < end and label not in exclude: 
                try: 
                    self.undefine(label)
                except SymbolError:
                    # This symbol cannot be undefined because it is either
                    # a reserved symbol or a reference to it is still in use. 
                    pass   
                  
        for address in self.arguments.keys(): 
            if address >= begin and address < end:
                del self.arguments[address] 
        for address in self.remarks.keys():
            if address >= begin and address < end:
                del self.remarks[address]  
        for address in self.data.keys():
            if address >= begin and address < end:
                self.data[address].valid = False
                del self.data[address] 
                
                
#------------------------------------------------------------------------------
# Assembler
#------------------------------------------------------------------------------

class Assembler(object):
    """
    Inline assembler. Instructions are assembled to :class:`memory
    <mach8.memory.Memory>`, *mem*, starting at position *origin*. 
    :class:`MetaSource` object, *meta*, is populated and referenced if 
    specified.  
    
    .. describe:: a(*args)
     
       Shorthand for :meth:`assemble`. 
    """
    
    def __init__(self, mem, origin=0, meta=None):
        self.mem = mem
        self._pc = memory.ProgramCounter(mem, origin)
        if meta is None: 
            meta = MetaSource() 
        self.meta = meta
        self._new_position = True
    
    @property
    def position(self):
        """
        Address where the next instruction will be assembled. If position is 
        assigned to a string value, a symbol lookup will be performed and a 
        :class:`SymbolUndefinedError` is raised if it does not exist. 
        """
        return self._pc.position
        
    @position.setter
    def position(self, ref):
        self._new_position = True
        self._pc.position = self.meta.lookup(ref) 

    def _resolve(self, uref):
        """
        Resolve the given unresolved reference. Get the symbol's value or
        re-evaluate an expression and place that value in the reference's
        address. 
        """
        if uref.expr is None: 
            value = self.meta.lookup(uref.ref) 
        else:
            value = uref.expr.eval(self.meta) 
            
        if uref.type == REFERENCE_VALUE: 
            self.mem[uref.address] = vm.size8(value)  
        elif uref.type == REFERENCE_ABSOLUTE: 
            self.mem[uref.address::2] = vm.size16(value)
        elif uref.type == REFERENCE_ZERO_PAGE: 
            self.mem[uref.address] = vm.size8(value) 
        elif uref.type == REFERENCE_RELATIVE: 
            abs_address = vm.size16(value)
            # Branch is relative to PC after opcode and displacement
            # have been consumed. Since abs_address points to where
            # the displacement should go, add one to this value. 
            rel_address = abs_address - (uref.address + 1) 
            assert_branch_displacement(rel_address)
            self.mem[uref.address] = vm.twos_forward(rel_address)
        else:
            assert False 
                    
    def assemble(self, *args):
        """
        To assemble an instruction, call the object with the 
        :class:`instruction <mach8.instruction.Instruction>` and the 
        argument (if necessary). Example:: 
    
           a = Assembler(mem, position=0x4000) 
           _;    a(lda_imm, 0x42) 
        
        Call the object with a string to create a label at the current address. 
        Forward references allowed. Example::
     
           _;    a(jmp_abs, 'skip_brk')
           _;    a(brk)
           _; a('skip_brk')
           _;    a(nop) 
       
        Use :mod:`expressions <mach8.expressions>` for enhanced disassembly 
        display:: 
    
           _;    a(lda_imm, 9 + 2)     # Disassembles to lda #$0B
           _;    a(lda_imm, add(9, 2)) # Disassembles to lda #[9 + 2]
        
        Returns the address where the instruction was assembled. 

        Note: Any reference to a label or alias that does not exist is 
        considered to be an unresolved reference and will be entered in as a 
        zero until resolved. Invoking :meth:`verify` will raise a 
        :class:`SymbolUnresolvedError` if there are any outstanding unresolved 
        references. 
        """
        instruction_address = self.position
        if len(args) == 0: 
            return instruction_address
        
        # Label definition
        if isinstance(args[0], str):
            if len(args) != 1: 
                raise TypeError('Expected 1 argument but received {:d}' 
                                .format(len(args)))
            label = args[0] 
            self.label(label) 
            return 
        
        inst = args[0]
        required_args = 1 if inst.addressing_mode in AM_NO_ARGUMENT else 2 
        if len(args) != required_args: 
            raise TypeError('Expected {:d} arguments but received {:d}' 
                            .format(required_args, len(args)))
        
        self._check_meta() 
        if inst.addressing_mode in AM_ADDRESS_16:
            self.meta.clear(instruction_address + 1, 
                            instruction_address + 3) 
            address = self.meta.add_reference(args[1], instruction_address, 
                                              REFERENCE_ABSOLUTE) 
            address = vm.size16(address) 
            self._pc.store(inst.opcode) 
            self._pc.store2(address) 
        elif inst.addressing_mode in AM_ADDRESS_8: 
            self.meta.clear(instruction_address + 1, 
                            instruction_address + 2) 
            address = self.meta.add_reference(args[1], instruction_address, 
                                              REFERENCE_ZERO_PAGE) 
            address = vm.size8(address) 
            self._pc.store(inst.opcode) 
            self._pc.store(address) 
        elif inst.addressing_mode == am.IMM:
            self.meta.clear(instruction_address + 1, 
                            instruction_address + 2) 
            value = self.meta.add_reference(args[1], instruction_address, 
                                            REFERENCE_VALUE) 
            value = vm.size8s(value) 
            self._pc.store(inst.opcode) 
            self._pc.store(vm.mask8(value)) 
        elif inst.addressing_mode in AM_NO_ARGUMENT:
            self._pc.store(inst.opcode)
        elif inst.addressing_mode == am.REL:
            self.meta.clear(instruction_address + 1, 
                            instruction_address + 2) 
            abs_address = self.meta.add_reference(args[1], instruction_address, 
                                                  REFERENCE_RELATIVE) 
            if self.meta.lookup(args[1], default=None) is not None:  
                # Branch is relative to PC after instruction has been consumed. 
                # Since we have not yet 'consumed' it, the PC has to be 
                # adjusted by two (opcode and offset) 
                rel_address = abs_address - (self.position + 2)
                assert_branch_displacement(rel_address)
                # TODO: Cleanup 
                address = rel_address & vm.BITS8 
            else: 
                address = 0
            self._pc.store(inst.opcode) 
            self._pc.store(address)  
        else: 
            raise ValueError('Invalid instruction: ' + str(inst)) 
        self._new_position = True
        
    def __call__(self, *args):
        return self.assemble(*args) 

    def _check_meta(self):
        """
        This check is performed when a label, remark, data segment, or 
        assembly occurs at this location. If this is the first time since 
        moving to this address, clear out any previous information. 
        """
        if self._new_position:
            self.meta.clear(self.position) 
            self.meta.arguments.pop(self.position, None)
            self._new_position = False 
                
    def label(self, name, address=None):
        """
        Defines a the label, *name*, at *address*. If *address* is not 
        specified, the current position of the assembler is used. Raises an 
        :class:`OverflowError` if the address is out of range. 
        """
        if address is None: 
            address = self.position
            self._check_meta()
        resolved = self.meta.define_label(name, vm.size16(address)) 
        map(self._resolve, resolved)
        
    def auto_label(self):
        """
        Returns a unique label name. Useful for macro definitions as in the 
        following::

            @macro
            def inc_zp_word(a, address): 
                \""" 
                Increments a word value stored at a zero page location. 
                \"""                              
                no_carry = a.auto_label()

                _;    a(inc_zp,  address)
                _;    a(bne,     no_carry)
                _;    a(inc_zp,  add(address, 1))
                _;    a.label    (no_carry)
        """
        return self.meta.auto_label() 

    def alias(self, name, value):
        """
        Assign a symbolic name to an arbitrary value. Example::
        
        _;    a.alias('nine', 9)
        _;    a.alias('two',  2) 
        _;    a(lda_imm, add('nine', 'two')) # Disassembles to lda #[nine + two] 
        
        Raises an :class:`OverflowError` if this definition resolves a 
        reference but the value is out of range. 
        """
        resolved = self.meta.define_alias(name, value) 
        map(self._resolve, resolved) 
        
    def macro(self, function, *args):
        """
        Invokes the macro *function* with arguments, *arg*. The *function* 
        should be a callable decorated with ``@macro``.  
        """
        function(self, *args) 
        
    def _data_str(self, value):
        """
        Insert string data at the current position. 
        """
        for char in value: 
            self.mem[self.position] = ord(char)
            self.position += 1
    
    def _data_int(self, value):
        """
        Insert numeric data at the current position.
        """
        if vm.is8(value) or vm.is8s(value): 
            self.mem[self.position] = vm.mask8(value)
            self.position += 1
        elif vm.is16(value): 
            self.mem[self.position::2] = value
            self.position += 2
        else: 
            raise OverflowError('Value out of range: ${:X} {:d}'
                               .format(value, value))
                    
    def _data_expression(self, expression):
        """
        Insert the results of an expression at the current position.
        """
        value = expression.eval(self.meta) 
        self._data_int(value) 
        
    def data(self, *args):
        """
        Enter data elements starting at the current assembly address. Each 
        argument is a data element to enter and can be either a: 
        
        * String: Each character is entered as an 8-bit ASCII value. 
        * Byte: Value from -128 to 255
        * Word: Value from 0 to 65535, entered in little endian ordering.
    
        Example:: 
        
            _;    a(ldx_imm, lb('hello'))
            _;    a(ldy_imm, hb('hello'))
            _;    a(jsr,     'SPRINT')
            _;    a(rts)
            _; a('hello')
            _;    a.data('Hello world!!', 0, 0xdead, 0xbeef) 
        """
        address = self.position
        data_list = []
        for arg in args: 
            data_list += [arg]
            if isinstance(arg, str):
                self._data_str(arg)
            elif isinstance(arg, int):
                self._data_int(arg) 
            elif isinstance(arg, expression.Expression):
                self._data_expression(arg)                
            else:
                raise TypeError('Invalid type for data entry')
            
        data = Data(address, self.position - address, 
                    ', '.join(map(repr, data_list)))  
        self.meta.set_data(data) 
        
    def remark(self, text):
        """
        Adds a descriptive comment to the code which will show up in the 
        disassembler. Each invocation of this method will add another line 
        of text if the program counter is not moved. Example:: 
    
            _;    a.remark('Preserve parameter')
            _;    a(pha)  
        """
        self._check_meta() 
        self.meta.add_remark(self.position, text) 
        
    def verify(self):
        """
        Verifies that there are no outstanding unresolved references. Raises 
        a :class:`SymbolUnresolvedError` if there are outstanding unresolved 
        references. The error message will contain a list of all unresolved 
        symbols. 
        """
        unresolved = set() 
        map(unresolved.add, self.meta.unresolved.iterkeys()) 
        if len(unresolved) > 0: 
            raise SymbolUnresolvedError('Unresolved references: ' + 
                                        ', '.join(sorted(unresolved)))
     
class BranchRangeError(Exception):
    """
    Branch target is outside the range of a valid displacement (greater than 
    127 or less than -128) 
    """
    
#------------------------------------------------------------------------------
# Disassembled
#------------------------------------------------------------------------------

FORMAT_TABLE = { 
    am.ABS: ('{} {}',     True),
    am.ABX: ('{} {},x',   True),
    am.ABY: ('{} {},y',   True), 
    am.ACC: ('{} a',      False),
    am.IMM: ('{} #{}',    True),
    am.IMP: ('{}',        False), 
    am.IND: ('{} ({})',   True),
    am.IZX: ('{} ({},x)', True), 
    am.IZY: ('{} ({}),y', True), 
    am.REL: ('{} {}',     True), 
    am.ZP:  ('{} {}',     True), 
    am.ZPX: ('{} {},x',   True), 
    am.ZPY: ('{} {},y',   True),
}

class Disassembled(object):
    """
    Description
    
    .. describe:: str(d)

       Description
    """
       
    address = 0 
    """
    Address where the instruction is located. 
    """
    
    labels = None 
    """
    List of labels that are defined at this address or an empty list. 
    """
    
    instruction = None 
    """
    :class:`~mach8.x6502.Instruction` object. 
    """
    
    argument = None 
    """
    Textual representation that should be used for the argument, or ``None`` 
    if the raw bytes should be displayed. 
    """
    
    bytes = None 
    """
    The opcode and argument bytes. 
    """
    
    remarks = None 
    """
    List of descriptive text that should be displayed for this instruction, 
    one line per element, or an empty list if there are no remarks. 
    """
    
    data = None 
    """
    If not ``None``, this address is part of a :class:`Data` block and its
    textual representation should be shown instead. 
    """
     
    def __init__(self): 
        self.labels = []
        self.instruction = x6502.NUL
        self.bytes = [x6502.NUL.opcode]
        self.remarks = [] 

    def _format_bytes(self):
        """
        Formats the bytes of the instruction. Always uses up space for three
        bytes (opcode + 16-bit argument) using black space as needed. 
        """
        str_bytes = []
        for i in xrange(0, 3): 
            if i >= len(self.bytes): 
                str_bytes += ["  "]
            else: 
                str_bytes += ["{:02x}".format(self.bytes[i])]
        return ' '.join(str_bytes) 
            
    def _format_instruction(self):
        """
        Formats the instruction name and arguments. 
        """
        i = self.instruction
        try:
            formatter, has_argument = FORMAT_TABLE[i.addressing_mode]
        except KeyError:
            raise ValueError('Invalid addressing mode: ' + 
                             str(i.addressing_mode)) 
        
        if not has_argument: 
            return formatter.format(i.operation) 
        
        if self.argument is None:
            # Format the raw bytes 
            if len(self.bytes) == 2: 
                arg = vm.hex8(self.bytes[1])
            else: 
                arg = vm.hex16(vm.to_words(self.bytes[1:3])[0]) 
        else: 
            arg = self.argument 
        return formatter.format(i.operation, arg) 
    
    def __str__(self):
        b = self._format_bytes()
        i = self._format_instruction()
        lines = [] 
        for label in self.labels: 
            lines += [label + ':'] 
        for remark in self.remarks: 
            lines += ['    ; ' + remark]
        if self.data is not None and self.data.valid: 
            lines += ['    {}: data      {}'.format(vm.hex16(self.data.address), 
                                             self.data.text)]
        else:
            lines += ["    {}: {}  {}".format(vm.hex16(self.address), 
                                              b, i)]
        return '\n'.join(lines) 
    
#------------------------------------------------------------------------------
# Disassembler
#------------------------------------------------------------------------------

class Disassembler(object):
    """
    Description
    """
    
    def __init__(self, mem, origin=0, meta=None):
        self.mem = mem
        self.pc = memory.ProgramCounter(mem, origin) 
        self._opcodes = x6502.get_instruction_set()
        if meta is None: 
            meta = MetaSource() 
        self.meta = meta
        
    @property
    def position(self):
        """
        Address where the next instruction will be disassembled. If position is 
        assigned to a string value, a symbol lookup will be performed and a 
        :class:`SymbolUndefinedError` is raised if it does not exist. 
        """
        return self.pc.position

    @position.setter
    def position(self, value):
        self.pc.position = self.meta.lookup(value)
        
    def next(self):
        """
        Description
        """
        d = Disassembled()
        d.address = vm.size16(self.position)
        d.labels = self.meta.get_labels(d.address) 
        d.remarks = self.meta.get_remarks(d.address)
        d.argument = self.meta.get_argument(d.address) 
        d.data = self.meta.get_data(d.address) 
        if d.data is not None: 
            self.position = d.data.address + d.data.length 
            return d 
        
        opcode = self.pc.load()
        if opcode in self._opcodes: 
            i = self._opcodes[opcode]
        else:
            op = '?{:02X}'.format(opcode)
            i = x6502.Instruction(opcode, op, am.IMP, None)
        d.instruction = i
        if i.addressing_mode in AM_ADDRESS_16:
            arg = self.pc.load2()
            d.bytes = [opcode, vm.lb(arg), vm.hb(arg)] 
        elif (i.addressing_mode in AM_ADDRESS_8 or 
              i.addressing_mode in (am.REL, am.IMM)):
            arg = self.pc.load()
            if i.addressing_mode == am.REL and d.argument is None: 
                # Branch is displacement after consuming bytes, therefore
                # add two. 
                d.argument = vm.hex16(d.address + vm.twos_inverse(arg) + 2) 
            d.bytes = [opcode, arg]                 
        elif i.addressing_mode in AM_NO_ARGUMENT:
            d.bytes = [opcode]
        else: 
            assert False 
        return d
        
    def peek(self):
        """
        Description
        """
        start = self.position
        d = self.next() 
        self.position = start
        return d
        
    def disassemble(self, begin=None, end=None):
        if begin is not None: 
            self.position = begin
        if end is None: 
            end = self.position
        while self.position <= end: 
            yield self.next()
        
    def dump(self, begin=None, end=None):
        return '\n'.join(map(str, self.disassemble(begin, end)))
    
    def __call__(self, begin=None, end=None):
        return self.disassemble(begin, end)

#------------------------------------------------------------------------------
# Supporting classes / functions
#------------------------------------------------------------------------------

class UnresolvedReference(object):
    """
    Unresolved references are internally tracked in :class:`MetaSource` with 
    instances of this class. Parameters to the constructor are the same as 
    those in the :meth:`MetaSource.add_reference() 
    <mach8.tools.MetaSource.add_reference>` method.
    """
    
    ref = None 
    """
    Symbol or address being referenced. 
    """
    
    address = None 
    """
    Address of the reference.
    """
    
    type = None 
    """
    Type of reference, see :meth:`MetaSource.add_reference() 
    <mach8.tools.MetaSource.add_reference>`
    """
    
    expr = None 
    """
    Expression that should be reevaulated once all references are resolved.
    """
    
    def __init__(self, ref, address, type, expr=None):
        self.ref = ref
        self.type = type
        self.address = address
        self.expr = expr
        

class Data(object):
    """
    Represents a descriptive data block in memory.
    """

    address = None 
    """
    Memory address where the data block begins.
    """
    
    length = None 
    """
    Size, in bytes, of the data block.
    """
    
    text = None 
    """
    Descriptive text that should be used for this memory block instead of 
    showing the raw memory values.
    """
    
    valid = True 
    """
    Is set to ``False`` if a memory write or another data block overwrites 
    portions of this data block and invalidates the descriptive text.
    """

    def __init__(self, address, length, text):
        self.address = address
        self.length = length
        self.text = text
        
        
def assert_branch_displacement(displacement):
    """
    Check that a branch displacement is valid. Raises a 
    :class:`BranchRangeError` if the displacement is greater than 127 or less
    than -128. 
    """
    if displacement < vm.SBYTE_MIN or displacement > vm.SBYTE_MAX: 
        raise BranchRangeError('Invalid branch displacement: {}'
                               .format(displacement)) 
        
#------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------

class SymbolError(Exception): 
    """
    Base exception for symbol errors.
    """

class SymbolConflictError(SymbolError):
    """
    Symbol cannot be added because it is already defined.
    """
    
class SymbolUndefinedError(SymbolError):
    """
    Symbol does not exist.
    """
    
class SymbolReservedError(SymbolError):
    """
    Symbol cannot be removed because it is reserved.
    """

class SymbolReferencedError(SymbolError):
    """
    Symbol cannot be removed because it is still in use.
    """
    
class SymbolUnresolvedError(SymbolError):
    """
    One or more references do not resolve to a defined symbol.
    """
    