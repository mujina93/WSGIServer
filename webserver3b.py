"""
Iterative server
- Server sleeps for 60 seconds after sending a response to a client
This means that if you make two request, one after the other, to the
server (for example using telnet, curl, or a browser), the second one
will receive no answer until 60 seconds have passed from the handing of
the first request. Try it! Fire up the server and make the requests (
either using 2 terminals, or using 2 tabs in the browser, or both.
You could also simply make a request by visiting localhost:8888 in the
browser, and then refresh the page. You will wee the page loading...
after one minute, you will see in your terminal the new response.)
"""
import socket
# module that allow us to make this program sleep for some seconds
import time

# server running on localhost (your own computer), port 8888
SERVER_ADDRESS = (HOST, PORT) = '', 8888
# parameter used in the server socket (see below in serve_forever())
# that sets to 5 the possible number of requests that the server
# can receive and handle
REQUEST_QUEUE_SIZE = 5

def handle_request(client_connection):
    # receive up to 1024 bytes from the client
    request = client_connection.recv(1024)
    # prints the request (decode, to pass from bytes to str)
    print(request.decode())
    # Build the response (as a bytes string)
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    # send the response to the client
    client_connection.sendall(http_response)
    # force the server (this program) to sleep for 1 minute
    time.sleep(60)

# same method as in WSGIServer class, in webserver2.py (here it is
# just a function, not a class' method). It builds a socket, able to
# manage internet addresses, and activate an infinite loop that:
# listen for client connections, handle clients' requests, closes the
# connections, repeat.
def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))

    while True:
        client_connection, client_address = listen_socket.accept()
        handle_request(client_connection)
        client_connection.close()

# By running this program, you activate the server and make it serve forever
# (until manually stopped)
if __name__ == '__main__':
    serve_forever()
