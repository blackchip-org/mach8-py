#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_demo.py 98 2011-12-12 23:10:35Z mcgann $
#------------------------------------------------------------------------------
from mach8_test import suite
from mach8_test.harness import console 

class TestDemo(console.TestHarness):
    
    def test(self):
        suite.banner(self.test)
        self.run_test("""
demo
a.position = 0x3000
a.data('Hello world!\\n', 0) 
demo
m(0x3000)
demo
m(0x3000, 0x300f)
demo
m
demo
a.position = 0x2000 
a(ldx_imm, 0x00) 
a(ldy_imm, 0x30) 
a(jsr,     'STROUT') 
a(rts) 
demo
r
demo
d(0x2000, 0x2007) 
demo
a.label('hello', 0x3000)
demo
y('hello')
demo
hex(y('hello'))
demo
a.position = 0x2000 
a(ldx_imm, lb('hello')) 
a(ldy_imm, hb('hello')) 
a(jsr,     'STROUT') 
a(rts) 
r
demo
d(0x2000, 0x2007)
demo
a.position = 0x2000 
a.macro(ldxy_imm, 'hello')
a(jsr, 'STROUT') 
a(rts) 
r
demo
d(0x2000, 0x2007)
demo
""".strip() 
)
        