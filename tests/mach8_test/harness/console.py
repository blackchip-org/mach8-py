#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: console.py 139 2012-02-05 05:28:51Z mcgann $
#------------------------------------------------------------------------------
import StringIO
import unittest
from mach8 import monitor
import sys 
import logging
from mach8_test import suite 
from mach8_test import noseutil

class TestHarness(unittest.TestCase):

    def setUp(self):
        from mach8 import mach

        self.output = StringIO.StringIO() 
        self.previous_stdout, sys.stdout = sys.stdout, self.output 
        self.comp = mach.Computer()
        self.shell = monitor.Shell(self.comp)
        self.meta = self.comp.meta
        # Turn off loading/saving of history and echo input lines. 
        self.shell.interactive = False 
        
    @noseutil.nottest
    def run_test(self, text):
        # Weak sauce. Is there a StringIO pipe?
        self.input = StringIO.StringIO(text + '\n') 
        self.previous_stdin, sys.stdin = sys.stdin, self.input 
        self.comp.reset() 
        self.shell.run() 
        # List of each output line with whitespace cleaned out. 
        self.results = map(str.strip, self.output.getvalue().splitlines())
        
    def tearDown(self):
        sys.stdout = self.previous_stdout
        try:
            sys.stdin = self.previous_stdin
        except AttributeError: 
            # Failure before stdin was reassigned
            pass
        
        if suite.log.isEnabledFor(logging.DEBUG):
            text = self.output.getvalue() 
            lines = text.splitlines() 
            # Line number ascending, descending, line text
            for line_number in xrange(1, len(lines)): 
                suite.log.debug('[{:3d} {:3d}] {}'
                                .format(line_number, len(lines) - line_number,
                                        lines[line_number])) 
