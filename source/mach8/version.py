#------------------------------------------------------------------------------
# Mach-8: The Virtual Machinery Playpen 
#
# blackchip.org, Inspired by the Vintage Computer Club. 
# All rites reversed (K) 2011, Reprint what you like.
#
# $Id: version.py 146 2012-03-22 02:12:42Z mcgann $
#------------------------------------------------------------------------------ 
"""
Version information.

The full version string is in the format of ``MAJOR.MINOR.REVISION``. Two 
functions are also provided to extract the subversion revision number and date.
Can be invoked with the following to print out the full version string: 

>>> python -m mach8.version 

Increase the 'bump' comment line to update the RCS tags when the version has
not changed.  
"""
import re

# Bump: 7

MAJOR           = '3'
"""
Major version number.
"""

MINOR           = '2'
"""
Minor version number. 
"""

REVISION        = '3'
"""
Revision number.
"""

RCS_REVISION    = '$Revision: 146 $'
"""
Expansion of the ``Revision`` keyword in subversion.
"""

RCS_DATE        = '$Date: 2012-03-21 22:12:42 -0400 (Wed, 21 Mar 2012) $'
"""
Expansion of the ``Date`` keyword in subversion. 
"""

def rcs_revision():
    """
    Extracts the revision number from the ``Revision`` keyword.
    """
    return re.search('\$Revision: (\d+)', RCS_REVISION).group(1)

def rcs_date(): 
    """
    Extracts the 'friendly' date string from the ``Date`` keyword. 
    """
    return re.search('\((.*)\)', RCS_DATE).group(1)

def string():
    """
    Returns ``MAJOR.MINOR.REVISION``
    """
    return MAJOR + '.' + MINOR + '.' + REVISION

def full_string():
    """
    Returns ``Mach 8 Version MAJOR.MINOR.REVISION (RCS_REVISION:RCS_DATE)``
    """
    return 'Mach-8 Version {} ({}: {})'.format(string(), 
                                               rcs_revision(), 
                                               rcs_date())
        
if __name__ == '__main__':
    print string() 
