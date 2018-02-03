"""
Simple WSGI web application. Built from scratch, without using
any python web framework (e.g. flask, pyramid, django).
You can use this app in combination with a server and an WSGI
interface which let this app and the server talk
"""

"""
A barebones WSGI application. Note that we need a method which
takes the environ dictionary (dictionary with environment variables)
and a function start_response with signature
start_response(status, response_headers).
"""
def app(environ, start_response):
    status = '200 OK'
    # The headers are a list of 2-tuples like (name, type)
    response_headers = [('Content-Type','text/plain')]
    # use the start_response function to start a response
    # which will send the headers above as answer to a client's request
    start_response(status, response_headers)
    # return some content along with the headers
    # the 'b' before the string is just for sending a bytes object
    # (remember, the WSGIServer expects bytes strings as a response!)
    return [b'Hello world from a simple WSGI application!\n']
