#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_x6502.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
from mach8 import memory, x6502
import unittest
from mach8_test import suite

class TestX6502(unittest.TestCase):

    def setUp(self):
        self.mem = memory.Block(pages=256)
        self.cpu = x6502.CPU(self.mem) 
        
    def test_instruction_set(self):
        # NOP instruction
        self.assertTrue(0xea in x6502.get_instruction_set())
        
    def test_pc(self):
        self.cpu.pc = 0x1234
        self.assertEquals(0x1234, self.cpu.pc) 
            
    def test_a(self):
        self.cpu.a = 0xab
        self.assertEquals(0xab, self.cpu.a) 
        
    def test_x(self):
        self.cpu.x = 0xab
        self.assertEquals(0xab, self.cpu.x) 
        
    def test_y(self):
        self.cpu.y = 0xab
        self.assertEquals(0xab, self.cpu.y) 
        
    def test_sp(self):
        self.cpu.sp = 0xab
        self.assertEquals(0xab, self.cpu.sp) 
        
    def test_sr(self):
        self.cpu.sr = 0xff
        self.assertEquals(0xff, self.cpu.sr) 
        
    def test_sr_zero(self):
        self.cpu.sr = 0x00 
        # Bit 5 hard wired on
        self.assertEquals(0x20, self.cpu.sr) 
        
    def test_c(self):
        self.cpu.c = True 
        self.assertEquals(0b00100001, self.cpu.sr)
        self.assertTrue(self.cpu.c) 

    def test_z(self):
        self.cpu.z = True 
        self.assertEquals(0b00100010, self.cpu.sr)
        self.assertTrue(self.cpu.z) 
                
    def test_i(self):
        self.cpu.i = True 
        self.assertEquals(0b00100100, self.cpu.sr)
        self.assertTrue(self.cpu.i) 
 
    def test_d(self):
        self.cpu.d = True 
        self.assertEquals(0b00101000, self.cpu.sr)
        self.assertTrue(self.cpu.d) 

    def test_b(self):
        self.cpu.b = True 
        self.assertEquals(0b00110000, self.cpu.sr)
        self.assertTrue(self.cpu.b) 
                       
    def test_v(self):
        self.cpu.v = True 
        self.assertEquals(0b01100000, self.cpu.sr)
        self.assertTrue(self.cpu.v) 

    def test_n(self):
        self.cpu.n = True 
        self.assertEquals(0b10100000, self.cpu.sr)
        self.assertTrue(self.cpu.n) 
                
    def test_register_overflow(self):
        self.assertRaises(OverflowError, setattr, self.cpu, 'a', 0x123)

    def test_register_negative(self):
        self.assertRaises(OverflowError, setattr, self.cpu, 'a', -1)

    def test_flag_listener(self):
        def listener(f, v):
            listener.flag = f
            listener.value = v
        self.cpu.flag_listeners += [listener] 
        self.cpu.z = True
        self.assertEquals(x6502.Z, listener.flag) 
        self.assertEquals(True, listener.value) 
        
    def test_register_listener(self):
        def listener(r, v):
            listener.register = r
            listener.value = v 
        self.cpu.register_listeners += [listener]
        self.cpu.a = 0xaa
        self.assertEquals(x6502.A, listener.register) 
        self.assertEquals(0xaa, listener.value) 
        
    def test_frame_listener(self):
        from mach8.instructions import jsr
        def listener(oper):
            listener.operation = oper
        self.cpu.stack_listeners += [listener]
        self.cpu.pc = 0x1fff
        self.mem[0x2000] = jsr.opcode 
        self.cpu.next() 
        self.assertEquals(jsr.operation, listener.operation) 
                
    def test_stack_listener(self):
        from mach8.instructions import pha
        def listener(oper):
            listener.operation = oper
        self.cpu.stack_listeners += [listener]
        self.cpu.pc = 0x1fff
        self.mem[0x2000] = pha.opcode 
        self.cpu.next() 
        self.assertEquals(pha.operation, listener.operation) 
        
    def test_next(self):
        from mach8.instructions import nop 
        cpu = self.cpu 
        cpu.mem[0x2000] = nop.opcode 
        self.cpu.pc = 0x1fff
        cpu.next() 
        self.assertEquals(0x2000, self.cpu.pc) 
        
    def test_run_listener(self):
        from mach8.instructions import nop 
        def listener(a, i):
            listener.address = a 
        self.cpu.run_listeners += [listener]
        self.cpu.pc = 0x1fff
        self.mem[0x2000] = nop.opcode
        self.cpu.next() 
        self.assertEquals(0x2000, listener.address)
        
    def test_str(self):
        suite.banner(self.test_str)
        cpu = self.cpu
        cpu.pc = 0x1234
        cpu.a  = 0x56
        cpu.x  = 0x78
        cpu.y  = 0x9a 
        cpu.sp = 0xbc
        cpu.sr = 0x00
        suite.log.info(str(cpu)) 
        self.assertEquals("""\
 pc  sr ac xr yr sp  n v - b d i z c
1234 20 56 78 9a bc  . . * . . . . .\
""", str(cpu)) 
        
    def test_str_all_flags(self):
        suite.banner(self.test_str_all_flags) 
        cpu = self.cpu
        cpu.sr = 0xff
        suite.log.info(str(cpu)) 
        self.assertEquals("""\
 pc  sr ac xr yr sp  n v - b d i z c
0000 ff 00 00 00 ff  * * * * * * * *\
""", str(cpu)) 
        
    def test_str_exit_reason(self):
        suite.banner(self.test_str_exit_reason)
        cpu = self.cpu 
        cpu.exit = x6502.EXIT_STOP 
        suite.log.info(str(cpu)) 
        self.assertEquals("""\
[stop]
 pc  sr ac xr yr sp  n v - b d i z c
0000 20 00 00 00 ff  . . * . . . . .\
""", str(cpu)) 
        