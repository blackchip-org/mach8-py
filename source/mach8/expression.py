#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: expression.py 107 2011-12-17 02:36:33Z mcgann $
#------------------------------------------------------------------------------
"""
Classes used to create simple expressions. 
"""
from mach8 import vm 

#==============================================================================
# Helper Functions
#==============================================================================
do_null     = lambda arg: arg
do_byte2    = lambda arg: arg >> (vm.SHIFT_BYTE * 2) & vm.BITS8 
do_byte3    = lambda arg: arg >> (vm.SHIFT_BYTE * 3) & vm.BITS8

format_asc  = lambda arg: "'{}'".format(arg) 
format_x32  = lambda arg: "${:08x}".format(arg)
 
#==============================================================================
# Base classes
#==============================================================================

class Expression(object):
    
    def __init__(self, *args):
        self.arg_spec = args
        
    def references(self, meta=None):
        from mach8 import tools 
        meta = meta if meta is not None else tools.MetaSource() 
        references = []
        for arg in self.arg_spec: 
            if isinstance(arg, Expression): 
                arg.do_references(meta, references) 
        self.do_references(meta, references) 
        return references 
    
    def eval(self, meta=None):    
        from mach8 import tools  
        meta = meta if meta is not None else tools.MetaSource()  
        args = []
        for arg in self.arg_spec: 
            if isinstance(arg, Expression): 
                args += [arg.eval(meta)]
            else: 
                args += [arg] 
        return self.do_eval(meta, *args) 
        
    def __repr__(self):
        args = [arg for arg in self.arg_spec]
        return self.do_string(*args)  
    
    
class BinaryExpression(Expression):
    """
    Expression that can use the ``reduce`` function. Addition is an
    expression that is suitable for this class. Use the ``function`` and 
    call ``reduce`` using the arguments, ``args``. When printing out a string
    representation of this expression, separate arguments with ``operator``.
    For example, the addition expression can be created with the following: 
        
    >>> add = lambda *args: expr.BinaryExpression(operator.add, ' + ', *args)
    """
    
    def __init__(self, function, operator, *args):
        super(BinaryExpression, self).__init__(*args)  
        self.function = function
        self.operator = operator

    def do_references(self, meta, references):
        for arg in self.arg_spec: 
            if isinstance(arg, str):  
                references += [arg] 
                
    def do_eval(self, meta, *arg_spec):
        args = map(meta.lookup, arg_spec)
        return reduce(self.function, args) 
    
    def do_string(self, *args):
        return '[' + self.operator.join(map(str, args)) + ']'
    

class UnaryExpression(Expression):
    """
    Expression with a single argument. Evaluating the high byte of a 16-byte
    value is suitable for this class. Use the ``function``, and invoke with 
    the specified argument, ``arg``. When printing out a string representation 
    of this expression, use ``format_spec`` to format the string. The 
    ``format_spec`` should contain one ``{}`` that indicates where the argument 
    value should be placed. For example, the high byte expression can be 
    created with the following: 
    
    >>> hb = lambda arg: expr.UnaryExpression(vm.hb, '>{}', arg) 
    """
    
    def __init__(self, function, format_spec, arg):
        super(UnaryExpression, self).__init__(arg) 
        self.function = function 
        self.format_spec = format_spec 
        
    def do_references(self, meta, references):
        for arg in self.arg_spec: 
            if isinstance(arg, str): 
                references += [arg] 
                
    def do_eval(self, meta, ref):
        address = meta[ref] 
        return self.function(address) 
        
    def do_string(self, ref):
        return self.format_spec.format(ref) 
    

class LiteralExpression(Expression):
    
    def __init__(self, function, formatter, arg):
        super(LiteralExpression, self).__init__(arg)  
        self.function = function 
        self.formatter = formatter 
        
    def do_references(self, meta, references):
        pass
    
    def do_eval(self, meta, arg):
        return self.function(arg) 
        
    def do_string(self, arg):
        return self.formatter(arg) 
    