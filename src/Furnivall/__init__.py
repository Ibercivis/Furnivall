__all__=['Core', 'Views', 'Plugins']

import os, sys
encoding = sys.getfilesystemencoding()
if hasattr(sys, 'frozen'):
    data_dir = os.path.abspath(os.path.dirname(unicode(sys.executable, encoding)))
data_dir = os.path.abspath(os.path.dirname(unicode(__file__, encoding)))
