#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: suite.py 96 2011-12-12 22:29:35Z mcgann $
#------------------------------------------------------------------------------
import logging
import sys

logging.basicConfig(format='%(message)s', stream=sys.stdout)
log = logging.getLogger('mach8.test')

#log.setLevel(logging.CRITICAL) 
log.setLevel(logging.DEBUG)

def banner(item):
    if callable(item): 
        message = item.__module__ + '.' + item.func_name
    else: 
        message = str(item) 
    log.info('\n==================== {}\n'.format(message)) 
