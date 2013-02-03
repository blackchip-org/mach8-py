#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: mock.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------

class TerminalInput(object):
    
    def __init__(self, message):
        self.message = message
        self.count = 0
        
    def getch(self):
        c = self.message[self.count]
        self.count += 1
        return c
    
    def __call__(self):
        return self.getch() 
    
    
class TerminalInputSlow(object):
    
    def __init__(self, message):
        self.message = message
        self.count = 0
        
    def getch(self):
        import errno 
        
        self.count += 1
        # Alternate between data and a 'would block'
        if self.count % 2 == 0: 
            raise IOError, (errno.EAGAIN, 
                            'Resource temporarily unavailable')
        return self.message[self.count / 2]

    def __call__(self): 
        return self.getch()
    
