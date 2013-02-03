try:
    import nose.tools
    nottest = nose.tools.nottest
except ImportError:
    nottest = lambda func: func
