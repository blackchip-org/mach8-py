#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: test_demo.py 98 2011-12-12 23:10:35Z mcgann $
#------------------------------------------------------------------------------
from mach8.expressions import * 
from mach8 import demo
import unittest

class TestDemo(unittest.TestCase):

    def setUp(self):
        lessons = ('Lesson 1', 'Lesson 2', 'Lesson 3')
        self.demo = demo.Lessons(lessons)
        
    def test_first(self):
        self.assertEquals('Lesson 1', self.demo.next()) 

    def test_second(self):
        self.demo.next() 
        self.assertEquals('Lesson 2', self.demo.next()) 

    def test_end(self):
        self.demo.next()
        self.demo.next() 
        self.demo.next() 
        self.assertEquals(demo.END, self.demo.next()) 

    def test_again(self):
        self.demo.next() 
        self.demo.next() 
        self.assertEquals('Lesson 2', self.demo.again()) 

    def test_again_start(self):
        self.assertEquals('Lesson 1', self.demo.again()) 
        
    def test_back(self):
        self.demo.next() 
        self.demo.next() 
        self.assertEquals('Lesson 1', self.demo.back()) 
            
    def test_back_start(self):
        self.assertEquals('Lesson 1', self.demo.back()) 

        
