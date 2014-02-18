import sys, os, unittest

if __name__ == "__main__":
    
    os.environ['FLASK_CONFIG'] = 'settings.test';
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
    
    from test import *

    unittest.main()
