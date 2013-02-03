#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_metasource.py 72 2011-10-21 09:11:44Z mcgann $
#------------------------------------------------------------------------------
from mach8 import tools
import unittest

class TestMetaSource(unittest.TestCase):

    def setUp(self):
        self.meta = tools.MetaSource() 
                
    def test_label(self):
        meta = self.meta
        meta.define_label('test.label', 0x1234) 
        self.assertEquals(0x1234, meta.labels['test.label'])
        self.assertNotIn('test.label', meta.reserved)
        self.assertIn('test.label', meta.addresses[0x1234]) 
        self.assertNotIn('test.label', meta.aliases) 
    
    def test_label_reserved(self):
        meta = self.meta 
        meta.define_label('test.label', 0x1234, reserved=True)
        self.assertEquals(0x1234, meta.labels['test.label'])
        self.assertIn('test.label', meta.reserved)
        self.assertIn('test.label', meta.addresses[0x1234]) 
              
    def test_redefine_label(self):
        meta = self.meta 
        meta.define_label('test.label', 0x1234) 
        self.assertRaises(tools.SymbolConflictError, meta.define_label, 
                          'test.label', 0x8888) 

    def test_label_invalid(self):
        self.assertRaises(OverflowError, self.meta.define_label, 'test.label', 
                          0x12345) 
        
    def test_multi_label(self):
        meta = self.meta 
        meta.define_label('label.one', 0x2222)
        meta.define_label('label.two', 0x2222) 
        self.assertIn('label.one', meta.addresses[0x2222])
        self.assertIn('label.two', meta.addresses[0x2222])

    def test_label_contains(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        self.assertIn('test', meta) 
        
    def test_contains_not(self):
        self.assertNotIn('test', self.meta) 
        
    def test_auto_label(self):
        meta = self.meta
        self.assertEquals('@1', meta.auto_label()) 
        self.assertEquals('@2', meta.auto_label()) 
        
    def test_alias(self):
        meta = self.meta
        meta.define_alias('test.alias', 0x42) 
        self.assertEquals(0x42, meta.aliases['test.alias'])
        self.assertNotIn('test.alias', meta.reserved)
        self.assertNotIn('test.alias', meta.labels)
        
    def test_redefine_alias(self):
        meta = self.meta
        meta.define_alias('test.alias', 0x42)
        self.assertRaises(tools.SymbolConflictError, meta.define_alias, 
                          'test.alias', 0x4242)
        
    def test_alias_contains(self):
        meta = self.meta 
        meta.define_alias('test', 0x2000) 
        self.assertIn('test', meta) 
        
    def test_label_alias_conflict(self):
        meta = self.meta 
        meta.define_label('test', 0x1234) 
        self.assertRaises(tools.SymbolConflictError, meta.define_alias, 
                          'test', 0x12) 
        
    def test_alias_label_conflict(self):
        meta = self.meta 
        meta.define_alias('test', 0x1234) 
        self.assertRaises(tools.SymbolConflictError, meta.define_label, 
                          'test', 0x12) 
        
    def test_label_lookup(self):
        meta = self.meta 
        meta.define_label('test', 0x1234) 
        self.assertEquals(0x1234, meta['test'])

    def test_get_labels(self):
        meta = self.meta 
        meta.define_label('foo', 0x2000) 
        meta.define_label('bar', 0x2000) 
        self.assertSetEqual(set(['foo', 'bar']), meta.get_labels(0x2000)) 
        
    def test_get_labels_empty(self):
        self.assertEquals(0, len(self.meta.get_labels(0x2000))) 
        
    def test_alias_lookup(self):
        meta = self.meta
        meta.define_alias('test', 0x1234) 
        self.assertEquals(0x1234, meta['test'])
                
    def test_alias_alias(self):
        meta = self.meta 
        meta.define_alias('foo', 0x12) 
        meta.define_alias('bar', 'foo') 
        self.assertEquals(0x12, meta['bar'])
        
    def test_lookup_undefined(self):
        self.assertRaises(tools.SymbolUndefinedError, self.meta.lookup, 'test')
    
    def test_lookup_default(self):
        self.assertEquals(0x42, self.meta.lookup('test', default=0x42))
         
    def test_reserve(self):
        meta = self.meta 
        meta.reserve('test')
        self.assertRaises(tools.SymbolConflictError, self.meta.define_label, 
                          'test', 0x1234) 
        
    def test_reference(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        self.assertEquals(0, meta.reference_counts['test'])
        self.assertEquals(0x2000, meta.add_reference('test', 0x3000, 
                                                     tools.REFERENCE_ABSOLUTE))
        self.assertEquals(1, meta.reference_counts['test'])
        self.assertIn('test', meta.references[0x3000])
        
    def test_reference_relative(self):
        meta = self.meta 
        meta.add_reference(0x2000, 0x2002, tools.REFERENCE_RELATIVE) 
        self.assertEquals('$2000', meta.arguments[0x2002])
        
    def test_get_references(self):
        meta = self.meta
        meta.define_label('foo', 0x2000) 
        meta.define_label('bar', 0x3000)
        meta.add_reference('foo', 0x4000, tools.REFERENCE_ABSOLUTE) 
        meta.add_reference('bar', 0x4000, tools.REFERENCE_ABSOLUTE)
        self.assertSetEqual(set(['foo', 'bar']), meta.get_references((0x4000)))
        
    def test_get_references_empty(self):
        self.assertEquals(set(), self.meta.get_references(0x4000)) 
        
    def test_unresolved(self):
        meta = self.meta
        meta.add_reference('test', 0x3000, tools.REFERENCE_ABSOLUTE)
        self.assertIn('test', meta.get_unresolved())
        
    def test_resolved(self):
        meta = self.meta 
        meta.add_reference('test', 0x3000, tools.REFERENCE_ABSOLUTE) 
        meta.define_label('test', 0x2000) 
        self.assertEquals(0, len(meta.get_unresolved())) 
    
    def test_unresolved_empty(self):
        self.assertEquals(0, len(self.meta.get_unresolved()))
        
    def test_argument(self):
        meta = self.meta
        meta.set_argument(0x2000, 'Argument')
        self.assertEquals('Argument', meta.get_argument(0x2000)) 
        
    def test_argument_empty(self):
        self.assertIsNone(self.meta.get_argument(0x2000)) 
        
    def test_data(self):
        meta = self.meta 
        data = tools.Data(0x2000, 3, 'foo')
        meta.set_data(data) 
        self.assertEquals('foo', meta.get_data(0x2000).text) 
        self.assertEquals('foo', meta.get_data(0x2001).text) 
        self.assertEquals('foo', meta.get_data(0x2002).text) 
        self.assertIsNone(meta.get_data(0x2003)) 
        
    def test_data_overlap(self):
        meta = self.meta
        foo = tools.Data(0x2000, 3, 'foo')
        bar = tools.Data(0x2001, 3, 'bar')
        meta.set_data(foo) 
        meta.set_data(bar)
        self.assertFalse(meta.get_data(0x2000).valid) 
        
    def test_data_empty(self):
        self.assertIsNone(self.meta.get_data(0x2000)) 
        
    def test_remarks(self):
        meta = self.meta
        meta.add_remark(0x2000, 'Remark 1')
        meta.add_remark(0x2000, 'Remark 2')        
        self.assertEquals(['Remark 1', 'Remark 2'], meta.get_remarks(0x2000)) 
        
    def test_remarks_empty(self):
        self.assertEquals(0, len(self.meta.get_remarks(0x2000))) 
    
    def test_remarks_clear(self):
        meta = self.meta
        meta.add_remark(0x2000, 'Remark 1')
        meta.add_remark(0x2000, 'Remark 2')
        meta.clear_remarks(0x2000)        
        self.assertEquals([], meta.get_remarks(0x2000))
        
    def test_undefine(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        meta.undefine('test')
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'test')

    def test_delitem(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        del meta['test']
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'test')
                
    def test_undefine_reserved(self):
        meta = self.meta 
        meta.define_label('test', 0x2000, reserved=True) 
        self.assertRaises(tools.SymbolReservedError, meta.undefine, 'test') 
        
    def test_undefine_referenced(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        meta.add_reference('test', 0x3000, tools.REFERENCE_ABSOLUTE)
        self.assertRaises(tools.SymbolReferencedError, meta.undefine, 'test')
        
    def test_clear_label(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        meta.clear(0x2000) 
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'test')
        
    def test_clear_label_range(self):
        meta = self.meta 
        meta.define_label('test', 0x2000) 
        meta.define_label('test2', 0x2fff) 
        meta.clear(0x2000, 0x3000) 
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'test') 
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'test2')

    def test_clear_label_reference(self):
        meta = self.meta 
        meta.add_reference('test', 0x2000, tools.REFERENCE_RELATIVE)
        meta.define_label('test', 0x2003)
        self.assertSetEqual(set(['test']), meta.get_references(0x2000)) 
        meta.clear(0x2000, 0x2004) 
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'test') 
        self.assertEquals(0, len(meta.get_references(0x2000)))
        
    def test_clear_label_reference_in_use(self):
        meta = self.meta 
        meta.add_reference('test', 0x2000, tools.REFERENCE_RELATIVE)
        meta.define_label('test', 0x2003)
        meta.clear(0x2003) 
        self.assertEquals(0x2003, meta['test'])
        self.assertSetEqual(set(['test']), meta.get_references(0x2000)) 

    def test_clear_reserved(self):
        meta = self.meta 
        meta.define_label('test', 0x2000, reserved=True)
        meta.clear(0x2000) 
        self.assertEquals(0x2000, meta['test'])
        
    def test_clear_argument(self):
        meta = self.meta
        meta.set_argument(0x2000, '$8000,X')
        meta.clear(0x2000) 
        self.assertIsNone(meta.get_argument(0x2000)) 
        
    def test_clear_remarks(self):
        meta = self.meta 
        meta.add_remark(0x2000, 'This is a test')
        meta.add_remark(0x2000, 'This is another test')
        meta.clear(0x2000) 
        self.assertListEqual([], meta.get_remarks(0x2000)) 
        
    def test_clear_exclude(self):
        meta = self.meta 
        meta.define_label('foo', 0x2000) 
        meta.define_label('bar', 0x2000) 
        meta.clear(0x2000, exclude=['foo'])
        self.assertEquals(0x2000, meta['foo'])
        self.assertRaises(tools.SymbolUndefinedError, meta.lookup, 'bar')

    def test_clear_data(self):
        meta = self.meta 
        data = tools.Data(0x2000, 3, 'foo')
        meta.set_data(data) 
        meta.clear(0x2000) 
        self.assertIsNone(meta.get_data(0x2000)) 
        self.assertFalse(meta.get_data(0x2001).valid) 
        