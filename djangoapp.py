import sys
# enter into ./helloworld directory
sys.path.insert(0, './helloworld')
# from helloworld/helloworld directory, import the module wsgi.py
# it contains all that is needed to build a simple django app
from helloworld import wsgi

# app object, taken by WSGIServer as the application
app = wsgi.application
