#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: executors.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
from mach8 import operations as op, addressing as am, vm, x6502 
        
def add(cpu, oper, mode):
    """
    See :data:`~mach8.operations.ADC`.
    """
    operand = _load_am(cpu, mode) 
    carry = 1 if cpu.c else 0 
    if cpu.d: 
        b1 = vm.bcd_inverse(cpu.a) 
        b2 = vm.bcd_inverse(operand) 
        bcd = b1 + b2 + carry 
        cpu.c = bcd > vm.DIGITS2
        if bcd > vm.DIGITS2: 
            bcd -= vm.DIGITS2 + 1
        result = vm.bcd_forward(bcd) & vm.BITS8
    else:
        value = cpu.a + operand + carry 
        cpu.c = value > vm.BITS8 
        result = value & vm.BITS8 
    signed = vm.twos_inverse(cpu.a) + vm.twos_inverse(operand)
    cpu.v = signed > vm.SBYTE_MAX or signed < vm.SBYTE_MIN
    _flags(cpu, result)
    cpu.a = result 
    
def bit(cpu, oper, mode):
    """
    See :data:`~mach8.operations.BIT`.
    """
    operand = _load_am(cpu, mode) 
    value = cpu.a & operand
    cpu.v = (operand & vm.BIT6) != 0
    cpu.z = value == 0 
    cpu.n = operand & vm.BIT7 != 0 
    cpu.v = operand & vm.BIT6 != 0 
    
def bit_op(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.AND`, 
    :data:`~mach8.operations.EOR`, 
    :data:`~mach8.operations.ORA`,
    """
    operand = _load_am(cpu, mode) 
    if   oper == op.AND: cpu.a &= operand 
    elif oper == op.ORA: cpu.a |= operand 
    elif oper == op.EOR: cpu.a ^= operand 
    else: assert False 
    _flags(cpu, cpu.a) 
    
def branch(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.BCS`, 
    :data:`~mach8.operations.BCC`, 
    :data:`~mach8.operations.BEQ`,
    :data:`~mach8.operations.BMI`, 
    :data:`~mach8.operations.BNE`, 
    :data:`~mach8.operations.BPL`,
    :data:`~mach8.operations.BRA`, 
    :data:`~mach8.operations.BVC`, 
    :data:`~mach8.operations.BVS`.
    """
    displacement = cpu.fetch() 
    branch = False 
    if   oper == op.BCS: branch = cpu.c
    elif oper == op.BCC: branch = not cpu.c
    elif oper == op.BEQ: branch = cpu.z 
    elif oper == op.BMI: branch = cpu.n 
    elif oper == op.BNE: branch = not cpu.z 
    elif oper == op.BPL: branch = not cpu.n 
    elif oper == op.BRA: branch = True 
    elif oper == op.BVC: branch = not cpu.v 
    elif oper == op.BVS: branch = cpu.v 
    else: assert False 
    if branch: 
        cpu.pc += vm.twos_inverse(displacement)
        
def brk(cpu, oper, mode):
    """
    See :data:`~mach8.operations.BRK`.
    """
    cpu.b = True 
    cpu.exit = x6502.EXIT_BREAK 
    # Gobble up next byte
    cpu.fetch() 
    
def compare(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.CMP`, 
    :data:`~mach8.operations.CPX`, 
    :data:`~mach8.operations.CPY`.
    """
    operand = _load_am(cpu, mode) 
    if   oper == op.CMP: result = cpu.a - operand
    elif oper == op.CPX: result = cpu.x - operand
    elif oper == op.CPY: result = cpu.y - operand
    else: assert False
    
    # C set as if subtraction. Clear if 'borrow', otherwise set
    cpu.c = result >= 0 
    _flags(cpu, result) 
    
def flags(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.CLC`, 
    :data:`~mach8.operations.SEC`, 
    :data:`~mach8.operations.CLI`,
    :data:`~mach8.operations.SEI`, 
    :data:`~mach8.operations.CLV`, 
    :data:`~mach8.operations.CLD`,  
    :data:`~mach8.operations.SED`.    
    """
    if   oper == op.CLC: cpu.c = False 
    elif oper == op.SEC: cpu.c = True
    elif oper == op.CLI: cpu.i = False 
    elif oper == op.SEI: cpu.i = True
    elif oper == op.CLV: cpu.v = False 
    elif oper == op.CLD: cpu.d = False 
    elif oper == op.SED: cpu.d = True
    else: assert False 
    
    
def jump(cpu, oper, mode):
    """
    See :data:`~mach8.operations.JMP`.
    """
    # CPU increments PC before fetching the opcode for the next instruction, 
    # set the target to be one less than actual. 
    if   mode == am.ABS: address = cpu.fetch2() 
    elif mode == am.IND: address = cpu.mem[cpu.fetch2()::2] 
    cpu.pc = address - 1
    
def jump_subroutine(cpu, oper, mode):
    """
    See :data:`~mach8.operations.LDA`.
    """
    [listener(oper) for listener in cpu.stack_listeners]
    address = cpu.fetch2()
    cpu.push2(cpu.pc) 
    # CPU increments PC before fetching the opcode for the next instruction, 
    # set the target to be one less than actual. 
    cpu.pc = address - 1

def load(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.LDA`, 
    :data:`~mach8.operations.LDX`, 
    :data:`~mach8.operations.LDY`.
    """
    value = _load_am(cpu, mode) 
    if   oper == op.LDA: cpu.a = value
    elif oper == op.LDX: cpu.x = value
    elif oper == op.LDY: cpu.y = value 
    else: assert False
    _flags(cpu, value) 

def nop(cpu, oper, mode):
    """
    See :data:`~mach8.operations.NOP`.
    """
    pass

def one_register(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.DEX`, 
    :data:`~mach8.operations.INX`, 
    :data:`~mach8.operations.DEY`,
    :data:`~mach8.operations.INY`,
    """
    if   oper == op.DEX: cpu.x = vm.mask8(cpu.x - 1); result = cpu.x 
    elif oper == op.INX: cpu.x = vm.mask8(cpu.x + 1); result = cpu.x 
    elif oper == op.DEY: cpu.y = vm.mask8(cpu.y - 1); result = cpu.y 
    elif oper == op.INY: cpu.y = vm.mask8(cpu.y + 1); result = cpu.y
    else: assert False
    _flags(cpu, result) 
    
def one_memory(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.DEC`, 
    :data:`~mach8.operations.INC`, 
    """
    address = _fetch_address(cpu, mode) 
    operand = _load_am(cpu, mode, address=address) 
    if   oper == op.DEC: value = vm.mask8(operand - 1)
    elif oper == op.INC: value = vm.mask8(operand + 1)
    _flags(cpu, value) 
    _store_am(cpu, mode, value, address=address) 
    
def return_subroutine(cpu, oper, mode):
    """
    See :data:`~mach8.operations.RTS`.
    """
    [listener(oper) for listener in cpu.stack_listeners] 
    cpu.pc = cpu.pull2()
            
def shift(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.ASL`, 
    :data:`~mach8.operations.ROL`, 
    :data:`~mach8.operations.LSR`, 
    :data:`~mach8.operations.ROR`. 
    """
    if mode == am.ACC: 
        operand = cpu.a 
    else:
        address = _fetch_address(cpu, mode) 
        operand = _load_am(cpu, mode, address)
        
    if oper in (op.ASL, op.ROL): 
        add_by = vm.BIT0 if cpu.c else 0 
        cpu.c = (operand & vm.BIT7) != 0
        result = (operand << 1) & vm.BITS8
        if oper == op.ROL: 
            result += add_by
    elif oper in (op.LSR, op.ROR): 
        add_by = vm.BIT7 if cpu.c else 0
        cpu.c = (operand & vm.BIT0) != 0 
        result = (operand >> 1) & vm.BITS8 
        if oper == op.ROR: 
            result += add_by
    else: 
        assert False
    _flags(cpu, result)
    if mode == am.ACC: 
        cpu.a = result
    else: 
        _store_am(cpu, mode, result, address) 
            
def stack(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.PHA`, 
    :data:`~mach8.operations.PLA`, 
    :data:`~mach8.operations.PHX`,
    :data:`~mach8.operations.PLX`,
    :data:`~mach8.operations.PHY`, 
    :data:`~mach8.operations.PLY`, 
    :data:`~mach8.operations.PHP`,
    :data:`~mach8.operations.PLP`,
    :data:`~mach8.operations.TXS`,
    :data:`~mach8.operations.TSX`.
    """
    [listener(oper) for listener in cpu.stack_listeners] 
    
    if   oper == op.PHA: cpu.push(cpu.a) 
    elif oper == op.PLA: cpu.a = cpu.pull(); _flags(cpu, cpu.a) 
    elif oper == op.PHX: cpu.push(cpu.x) 
    elif oper == op.PLX: cpu.x = cpu.pull(); _flags(cpu, cpu.x) 
    elif oper == op.PHY: cpu.push(cpu.y) 
    elif oper == op.PLY: cpu.y = cpu.pull(); _flags(cpu, cpu.y) 
    elif oper == op.PHP: cpu.push(cpu.sr) 
    elif oper == op.PLP: cpu.sr = cpu.pull()
    elif oper == op.TXS: cpu.sp = cpu.x 
    elif oper == op.TSX: cpu.x = cpu.sp 
    else: assert False
    
def store(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.STA`, 
    :data:`~mach8.operations.STX`, 
    :data:`~mach8.operations.STY`,
    :data:`~mach8.operations.STZ`,
    """
    if   oper == op.STA: _store_am(cpu, mode, cpu.a) 
    elif oper == op.STX: _store_am(cpu, mode, cpu.x)
    elif oper == op.STY: _store_am(cpu, mode, cpu.y)
    elif oper == op.STZ: _store_am(cpu, mode, 0) 
    else: assert False
    
def sub(cpu, oper, mode):
    """
    See :data:`~mach8.operations.SBC`, 
    """
    operand = _load_am(cpu, mode) 
    carry = 0 if cpu.c else 1
    if cpu.d: 
        b1 = vm.bcd_inverse(cpu.a) 
        b2 = vm.bcd_inverse(operand) 
        value = b1 - b2 - carry 
        cpu.c = not value < 0 
        if value < 0: 
            value += 100
        result = vm.bcd_forward(value) & vm.BITS8 
    else: 
        value = cpu.a - operand - carry 
        cpu.c = not value < 0 
        result = value & vm.BITS8 
    signed = vm.twos_inverse(cpu.a) - vm.twos_inverse(operand)
    cpu.v = signed > vm.SBYTE_MAX or signed < vm.SBYTE_MIN
    _flags(cpu, result)
    cpu.a = result 
    
def transfer(cpu, oper, mode):
    """
    See 
    :data:`~mach8.operations.TAX`, 
    :data:`~mach8.operations.TXA`, 
    :data:`~mach8.operations.TAY`,
    :data:`~mach8.operations.TYA`,
    """
    if   oper == op.TAX: cpu.x = cpu.a; result = cpu.x
    elif oper == op.TXA: cpu.a = cpu.x; result = cpu.a 
    elif oper == op.TAY: cpu.y = cpu.a; result = cpu.y 
    elif oper == op.TYA: cpu.a = cpu.y; result = cpu.a 
    else: assert False 
    _flags(cpu, result) 
    
#------------------------------------------------------------------------------
# Supporting functions
#------------------------------------------------------------------------------
def _flags(cpu, value):
    cpu.z = value == 0 
    cpu.n = value & vm.BIT7 != 0 
    
def _load_zp(cpu, address):
    return cpu.mem[vm.size8(address)]

def _load_zp16(cpu, address):
    # TODO: Simplify
    return (_load_zp(cpu, address) + (_load_zp(cpu, address + 1) << 8))

def _fetch_address(cpu, mode):
    if mode == am.ZP: 
        return cpu.fetch()
    elif mode == am.ZPX: 
        return cpu.fetch() + cpu.x 
    elif mode == am.ZPY: 
        return cpu.fetch() + cpu.y 
    elif mode == am.ABS: 
        return cpu.fetch2() 
    elif mode == am.ABX: 
        return cpu.fetch2() + cpu.x 
    elif mode == am.ABY: 
        return cpu.fetch2() + cpu.y 
    elif mode == am.IZX: 
        return _load_zp16(cpu, cpu.fetch() + cpu.x)
    elif mode == am.IZY: 
        return _load_zp16(cpu, cpu.fetch()) + cpu.y
    else: 
        raise ValueError('Invalid addressing mode: {}'.format(mode))
            
def _load_am(cpu, mode, address=None):
    if mode == am.IMM: 
        return cpu.fetch()
    if address is None: 
        address = _fetch_address(cpu, mode)
    if mode in (am.ZP, am.ZPX, am.ZPY): 
        return _load_zp(cpu, address)
    else:
        return cpu.mem[address]
        
def _store_zp(cpu, address, value):
    cpu.mem[vm.size8(address)] = value

def _store_am(cpu, mode, value, address=None):
    if address is None: 
        address = _fetch_address(cpu, mode) 
    if mode in (am.ZP, am.ZPX, am.ZPY): 
        _store_zp(cpu, address, value)
    else: 
        cpu.mem[address] = value

 
    