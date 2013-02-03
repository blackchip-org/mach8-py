#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: demo.py 111 2011-12-18 12:33:04Z mcgann $
#------------------------------------------------------------------------------

TEXT = ("""
This is a demo of the Mach-8 monitor. 

Let's create a simple program that prints out the classic 'Hello world' string. 
First, we will load the zero terminated string into memory at address $3000. 
Type in the following to position the assembler at that address and then load 
the string into memory. 

Type in the following: 

a.position = 0x3000
a.data('Hello world!\\n', 0) 
demo
""", 
"""
Each step of the demo will give you instructions on what to do and then 
return to the mach8 prompt. The last set of instructions can be repeated
again by typing in 'again' and you can go back one step by typing in 'back'. 

Now lets dump the memory at that address to see that the string is actually
there. 

Type in the following: 

m(0x3000)
demo
""",
"""
If the 'm' command only has one argument, a full page of memory is displayed
starting at that address. Let's only display one line of dump instead: 

Type in the following: 

m(0x3000, 0x300f)
demo
""", 
"""
Typing in 'm' with no arguments continues the dump at the previous location
and displays a page of memory. The command below shows memory from 
$3110 (the end of the last 'm' command) all the way to $310f. 

Type in the following: 

m
demo
""", 
"""
We will now use the STROUT routine to print the string. The STROUT routine 
requires the X register to be loaded with the low byte of the string
address and the Y register to be loaded with the high byte of the string
address. Position the assembler at address $2000, load the registers, 
call the STROUT routine, and then return. 

Type in the following: 

a.position = 0x2000 
a(ldx_imm, 0x00) 
a(ldy_imm, 0x30) 
a(jsr, 'STROUT') 
a(rts) 
demo
"""
, 
"""
Now, run the program. Typing in 'r' with no arguments starts execution at 
the default address of $2000. The string 'Hello world!' should be displayed
on the terminal. 

Type in the following: 

r
demo
"""
,
"""
Use the disassembler to see the program that we have entered. 

Type in the following: 
d(0x2000, 0x2007) 
demo
"""
,
"""
We used a memory address, passed to STROUT, to specify the string to print
to the terminal. Using memory addresses is tedious and it is easier to use
symbolic names instead. Let's assign a label to the 'Hello World' string 
which we placed at address $3000. 

Type in the following: 

a.label('hello', 0x3000) 
demo
""", 
"""
The address of a label can be obtained by using 'y' (sYmbol lookup). Lets make
sure that the value of the 'hello' label is correct. 

Type in the following: 

y('hello')
demo
""",
"""
The 'y' command returns a decimal value, so lets use the python 'hex' function
to see if it is equal to $3000. 

Type in the following: 

hex(y('hello'))
demo
"""
,
"""
Now change the program to use the label instead of the actual memory address. 
Since the X register needs the low byte of the address and the Y register
needs the high byte of the address, use the lb (low byte) and hb (high byte) 
functions. 

Type in the following: 

a.position = 0x2000 
a(ldx_imm, lb('hello')) 
a(ldy_imm, hb('hello')) 
a(jsr, 'STROUT') 
a(rts) 
r
demo
"""
,
"""
Disassemble the new version of the program to see how it looks now. The
arguments for the ldx and ldy instructions now have the label name and the
'<' symbol for low byte and the '>' symbol for high byte. 

d(0x2000, 0x2007) 
demo
"""
, 
"""
Macros can be used to simplify common operations. In this case, loading 
the X and Y registers with the address can be done using the ldxy_imm 
(load X and Y, immediate) macro. Lets rewrite the program using this macro. 

Type in the following: 

a.position = 0x2000 
a.macro(ldxy_imm, 'hello')
a(jsr, 'STROUT') 
a(rts) 
r
demo
"""
, 
"""
Disassemble the program again. It looks like the previous program except
the instructions in the macro are now surrounded by remarks. 

Type in the following: 

d(0x2000, 0x2007)
demo
"""
, 
)

END = """
The demo has finished. If you would like to rerun the demo, type in the 
following: 

demo_restart
"""

class Lessons(object):
    
    def __init__(self, lessons): 
        self.lessons = lessons 
        self._position = 0 
        
    @property
    def position(self):
        return self._position 
    
    @position.setter
    def position(self, v):
        if v < 0: 
            self._position = 0 
        else: 
            self._position = v 
        
    def current(self):
        if self._position >= len(self.lessons): 
            return END
        else: 
            return self.lessons[self.position]
       
    def next(self):
        val = self.current()
        self.position += 1
        return val
    
    def again(self):
        self.position -= 1
        return self.next() 
    
    def back(self):
        self.position -= 2 
        return self.next() 


class LessonPrinter(Lessons):
    
    def __init__(self, lessons):
        super(LessonPrinter, self).__init__(lessons) 

    def next(self):
        print super(LessonPrinter, self).next() 
    

    