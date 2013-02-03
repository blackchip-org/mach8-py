#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: vm.py 106 2011-12-15 00:05:50Z mcgann $
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Constants
#------------------------------------------------------------------------------
BIT0 = 1
BIT1 = 2
BIT2 = 4
BIT3 = 8 
BIT4 = 16
BIT5 = 32
BIT6 = 64
BIT7 = 128 

BITS4 = 0xf
BITS8 = 0xff
BITS16 = 0xffff

DIGITS2 = 99

SHIFT_NIBBLE = 4
SHIFT_BYTE = 8 

SBYTE_MIN = -(2**8 / 2) 
SBYTE_MAX = (2**8 / 2) - 1
SWORD_MIN = -(2**16 / 2) 
SWORD_MAX = (2**16 / 2) - 1

PAGE_SIZE = 0x100

#------------------------------------------------------------------------------
# Functions
#------------------------------------------------------------------------------
def bstr(string):
    """
    Return a list of bytes that represents the given *string*.
    """
    return [ord(c) for c in string]
    
def lb(value):
    """
    Returns the low byte from the 16-bit *value*. Example:
    
    >>> hex(vm.lb(0x1234))
    '0x34'
    """
    return value & BITS8 

def hb(value):
    """
    Returns the high byte from the 16-bit *value*. Example:
    
    >>> hex(vm.hb(0x1234))
    '0x12'
    """
    return value >> SHIFT_BYTE & BITS8 

def ln(value):
    """
    Returns the low nibble from the 8-bit *value*. Example:
    
    >>> hex(vm.ln(0xab))
    '0xb'
    """
    return value & BITS4 

def hn(value):
    """
    Returns the high nibble from the 8-bit *value*. Example: 
    
    >>> hex(vm.hn(0xab))
    '0xa'
    """
    return (value >> SHIFT_NIBBLE) & BITS4

def from_words(words):
    """
    Convert a sequence of words into a list of bytes. Example:
    
    >>> vm.from_words([0x1234, 0x5678])
    [0x34, 0x12, 0x78, 0x56]
    """
    bytes = list()
    for w in words: 
        bytes += [lb(w)] 
        bytes += [hb(w)]
    return bytes

def hex8(value):
    """
    Formats the 8-bit *value* in the form of ``$xx``
    """
    return '${:02x}'.format(value)

def hex16(value):
    """
    Formats the 16-bit *value* in the form of ``$xxxx``
    """
    return '${:04x}'.format(value)

def bin8(value):
    """
    Formats the 8-bit *value* in the binary form ``b00000000``
    """ 
    return 'b{:08b}'.format(value) 

def is8(value):
    """
    Returns true if *value* does not overflow an unsigned 8-bit value.
    """
    return abs(value) == value & BITS8

def is8s(value):
    """
    Returns true if *value* does not overflow a signed or unsigned 8-bit value. 
    """
    return value >= SBYTE_MIN and value <= BITS8

def is16(value):
    """
    Returns true if *value* does not overflow an unsigned 16-bit value.
    """
    return abs(value) == value & BITS16
    
def mask8(value):
    """
    Returns *value* as 8 bits unsigned, truncating if necessary.
    """
    return value & BITS8

def mask16(value):
    """
    Returns *value* as 16 bits unsigned, truncating if necessary. 
    """
    return value & BITS16

def size8(value):
    """
    Ensures *value* is 8 bits unsigned, otherwise raises an 
    :class:`OverflowError`. Returns *value*.
    """
    if not is8(value): 
        raise OverflowError('Not a byte: ${:0X} ({:d})'.format(value, value)) 
    return value 

def size8s(value):
    """
    Ensures *value* is 8 bits unsigned or signed, otherwise raises an 
    :class:`OverflowError`. Returns *value*.
    """
    if not is8s(value): 
        raise OverflowError('Not a byte: ${:0X} ({:d})'.format(value, value)) 
    return value 

def size16(value):
    """
    Ensures *value* is 16 bites, otherwise raises an :class:`OverflowError`.
    Returns *value*.
    """
    if not is16(value): 
        raise OverflowError('Not a word: ${:0X} ({:d})'.format(value, value)) 
    return value 

def word(lo, hi):
    """
    Combine the *lo* byte and *hi* byte and return as a word.
    """
    return size8(hi) << SHIFT_BYTE | size8(lo) 

def byte(lo, hi):
    """
    Combine the *lo* nibble and *hi* nibble and return as a byte. 
    """
    return hi << SHIFT_NIBBLE | lo

def to_words(bytes):
    """
    Convert a sequence of bytes into a list of words. Raises a
    :class:`ValueError` if the sequence length is not divisible by two. 
    Example:
    
    >>> vm.to_words([0x34, 0x12, 0x78, 0x56])
    [0x1234, 0x5678]
    """
    try:
        return [word(bytes[i], bytes[i+1]) for i in xrange(0, len(bytes), 2)] 
    except IndexError:
        raise ValueError('Invalid length: ' + str(len(bytes))) 
    
def twos_forward(value):
    """
    Converts a signed integer to a twos' complement byte. Raises a 
    :class:`ValueError` if the value is out of range.
    """
    if size8s(value) < 0:   
        value = BITS8 + 1 - abs(value)
    return value 
        
def twos_inverse(value):
    """
    Converts a twos' complement byte to a signed integer. Raises a 
    :class:`ValueError` if the value is out of range. 
    """
    negative = size8(value) & BIT7 != 0
    if negative: 
        value = value - (BITS8 + 1) 
    return value

def bcd_inverse(a):
    """
    Converts a BCD value to a decimal value. Raises an 
    :class:`InalidBCDNumberError` if the value is not valid. 
    """
    try:
        return int(hex(a)[2:])
    except ValueError: 
        raise InvalidBCDNumberError, 'Invalid BCD value: $%X' % a 
    
def bcd_forward(a):
    """
    Converts a decimal value to a BCD value.  
    """
    sign = '-' if a < 0 else ''
    return int(sign + '0x' + str(abs(a)), 16)

def py2fac(value):
    """
    Convert a floating point value to FAC bytes. 
    """    
    from mach8 import aliases 

    bytes = []
    mantissa, exponent = '{:e}'.format(value).replace('.', '').split('e')
    # Add one more for even-ness
    mantissa = mantissa + '0'
    sign = 0
    if value < 0: 
        sign |= aliases.SIGN_MANTISSA
        # Strip negative sign 
        mantissa = mantissa[1:]
    if exponent.startswith('-'):
        sign |= aliases.SIGN_EXPONENT
    bytes += [sign] 
    for i in xrange(6, -1, -2): 
        hi = ord(mantissa[i]) - ord('0') 
        lo = ord(mantissa[i + 1]) - ord('0')
        bytes += [byte(lo, hi)]  
    hi = ord(exponent[1]) - ord('0')
    lo = ord(exponent[2]) - ord('0')
    bytes += [byte(lo, hi)]
    return bytes 

def fac2py(bytes):
    """
    Convert FAC bytes to a floating point value. 
    """
    from mach8 import aliases 

    chars = []
    sign_byte = bytes[aliases.FAC_SIGN]
    if sign_byte & aliases.SIGN_MANTISSA != 0:
        chars += ['-']
    for i in xrange(0, 4): 
        digits = bytes[aliases.FAC_MANTISSA - i]
        chars += [chr(hn(digits) + ord('0'))]
        if i == 0: 
            chars.append('.')
        chars += [chr(ln(digits) + ord('0'))]
    chars += ['e']
    if sign_byte & aliases.SIGN_EXPONENT != 0: 
        chars += ['-']
    digits = bytes[aliases.FAC_EXPONENT]
    chars += [chr(hn(digits) + ord('0'))]
    chars += [chr(ln(digits) + ord('0'))]
    return float(''.join(chars)) 

#------------------------------------------------------------------------------
# Exceptions
#------------------------------------------------------------------------------

class InvalidBCDNumberError(Exception):
    """
    Attempted to convert a hex value that was not a valid BCD value. 
    """
    

