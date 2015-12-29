#!/usr/bin/env python
import os
from webapp import app




# Below for testing only
#
if __name__ == '__main__':
    virtenv = os.path.join(os.environ.get('OPENSHIFT_PYTHON_DIR','.'), 'virtenv')
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, app)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()
