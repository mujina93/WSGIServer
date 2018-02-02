"""
minimalistic WSGI: Python Web Server Gateway Interface. An
intermediate application that allows any server and any
framework to talk and work together. E.g. you can use
Waitress, Nginx, Gunicorn as servers, and Pyramid, Flash,
or Django as frameworks.
As long as the web server implements the server portion of
the WSGI interface, and the python web framework implements
the framework side of the WSGI interface, everything can work
fine.
"""

"""
socket is a module that provides access to the BSD socket interface.
[socket object]
socket() returns a socket object, whose methods implement the
various socket system calls.
Socket addresses representations:
* AF_UNIX : single string
* AF_INET : pair (host,port) with host a string like a hostname
            or an IPv4 address, and port an integer
* AF_INET6: (host,port,flowinfo,scopeid) with flowinfo and scopeid
            represent sin6_flowinfo and sin6_scope_id members in
            struct sockaddr_in6 in C. These 2 can be omitted.
* AF_NETLINK: pairs pid, groups.
* AF_TIPC : for TIPC (open non-IP based networked protocol).
            Addresses are represented by a tuple
            (addr_type, v1, v2, v3 [, scope])
[socket protocols]
socket.AF_UNIX, socket.AF_INET, socket.AF_INET6 are constants
representing the address (and protocol) families, used for the
first argument to socket()
[socket types]
socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW,
socket.SOCK_RDM, socket.SOCK_SEQPACKET are constants representing
the socket types, used for the second argument to socket()
"""
import socket
"""
io module provides facilities for dealing with various types of I/O.
Main types: text I/O, binary I/O, raw I/O.
An object belonging to any of these categories is called a file object.
It represents the stream where you can write to/from which you can read.
Streams can be read only, write only, or read-write. Every stream is
careful about the type of data you give them (for example, binary streams
want bytes, text streams want strings).
io.StringIO is a file-like class that implements a string (text) buffer.
StringIO(initial_value='',newline='\n') creates a StringIO object,
optionally initialized with a string.
io.BytesIO([initial_bytes]) is instead a buffer for bytes.
[important methods]
* read(size) read and returns at most size characters from the stream
* read1() In BytestIO, same as read()
* readline(size=-1) reads until newline or EOF and return a string
* write(s) write the string s to the stream and returns the number of
            characters written
* getvalue() return the entire contents of the buffer (as a str/or as bytes)
* close() frees the memory buffer. Attempting to do further
            operations with a closed object will raise a ValueError.
In python 2, StringIO was an independent module.
"""
import io
"""
sys module provides access to some variables used or mantained by
the interpreter and to functions that interact strongly with the
interpreter.
[argv]
sys.argv contains the list of command line arguments passed to a
Python script. argv[0] = script name. argv[n] = n-th argument
"""
import sys

# WSGI program class definition
class WSGIServer(object):
    """
    class variables, shared by all instances of WSGIServer class
    they can still be accessed as self.address_family, self.socket_type,...
    """
    # constant representing IPv4, passed as first argument to socket()
    address_family = socket.AF_INET
    # constant representing socket type of type TCP
    socket_type = socket.SOCK_STREAM
    # parameter for socket.listen([backlog]) which specifies the number of
    # unaccepted connections that the system will allow before reusing new connections
    request_queue_size = 1

    """
    constructor, takes the server address as argument
    [server_address]
    the given argument is the address to which the internal socket()
    object will be bound to.
    """
    def __init__(self, server_address):
        """
        Create a listening socket with socket()
        As specified above, the protocol is IPv4 (by address_family)
        and the socket type is TCP (by socket_type).
        The instance socket object is: self.listen_socket.
        A local (inside the method __init__) variable is also created:
        listen_socket, whose name can be used later on in this function
        to access the same socket object (just to avoid to write self.
        every time)
        """
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        """
        setsockopt(level,optname,value:int/buffer) sets the value for
        some socket option (the symbolic constants are the ones like
        socket.SO_*). The value can be an integer, None, or a bytes-like
        object representing a buffer.
        [SOL]
        SOL_ means "socket option level". These symbols are used to set
        socket options through setsockopt.
        [SO_REUSEADDR]
        indicates that the address can be reused. For an AF_INET socket, it
        means that a socket may bind, except when there is an active listening
        socket bound to the address.
        [bind]
        'socket binding' means assigning an address so it can accept connections
        on that address.
        """
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Binds the socket to the address: server_address (argument of
        # the WSGIServer constructor)
        listen_socket.bind(server_address)
        # listen([backlog]) enables the server to accept connections.
        # the backlog argument specifies the number of unaccepted connections
        # that the system will allow before refusing new connections.
        listen_socket.listen(self.request_queue_size)
        """
        getsockname() returns the socket's own address. This can be useful
        to find out the port number of an IP socket. The format of the
        address returned depends on the address family. In this case,
        the address family AF_INET is used, which is expressed as a tuple
        host, port.
        The slicing at the end is probably to ensure that only two arguments
        are extracted from getsockname()
        """
        host, port = self.listen_socket.getsockname()[:2]
        """
        getfqdn() returns a Fully Qualified Domain Name for the argument name
        in this case, a fully qualified domain is returned for the host
        string retrieved by getsockname
        """
        # saves server name as instance attribute
        self.server_name = socket.getfqdn(host)
        # saves port as instance attribute
        self.server_port = port
        # Return headers set by Web framework/Web application
        self.headers_set = []
    """
    WSGI object has an instance object which represents the web application.
    This is a setter that takes an application, and stores it internally.
    """
    def set_app(self, application):
        self.application = application
    """
    starts serving, with an endless loop, doing continuously:
        self.listen_socket.accept() # accepting connection
        self.handle_one_request()   # handling a single request
    """
    def serve_forever(self):
        # just local name for self.listen_socket (internal socket object member)
        listen_socket = self.listen_socket
        # serves until stopped with CTRL+C or similar
        while True:
            """
            accept() accepts a connection. The socket must be:
            * bound to an address (done in __init__ with bind())
            * listening for connections (done with listen())
            The returned value is a pair (conn, addr) where conn is a
            new socket object, usable to send and receive data on the
            connection, and addr is the address bound to the socket on
            the other end of the connection
            """
            # New client connection
            self.client_connection, client_address = listen_socket.accept()
            # Handle one request and close the client connection. Then
            # loop over to wait for another client connection.
            # This method makes use of self.client_connection above
            self.handle_one_request()
    """
    custom method that handles one request. This method is called in
    self.serve_forever endlessly.
    """
    def handle_one_request(self):
        """
        socket.recv(bufsize[,flags]) receives data from the socket.
        It returns a bytes object representing the data received.
        bufsize specifies the maximum amount of data to be received
        at once (in this case, 1024 bytes). flags defaults to 0. See
        Unix man page recv(2) for an explanation.
        [bytes object]
        native python object which is an immutable sequence of integers
        in the range [0,256[
        """
        # Receives data by the client_connection socket object returned
        # by accept() (in self.serve_forever).
        self.request_data = request_data = self.client_connection.recv(1024)
        """
        Print formatted request data a la 'curl -v'.
        The bytearray object request_data is first converted to str
        using .decode('utf-8'), then it is split in lines, and they
        are printed in format (note the '<' for denoting a request):
        < line1
        < line2
        ...
        """
        print(''.join(
            '< {line}\n'.format(line=line)
            for line in request_data.decode('utf-8').splitlines()
        ))
        # call self.parse_request on the data received by the request
        self.parse_request(request_data)

        # Construct environment dictionary using request data
        # this dictionary contains the data required by the application
        # according to the WSGI specification
        env = self.get_environ()

        """
        It's time to call our application callable and get
        back a result that will become HTTP response body
        The application takes a WSGI-stylized dict and a function
        start_response which sets the server headers and should
        return a 'write' callable, according to WSGI specification.
        The 'env' dict contains (well formatted) the data of the
        request. In this way, we are actually making the application
        aware of the exact client's request, and the application is
        able to send a response, which is collected in 'result'.
        When called by the server, the application object must return
        an iterable yielding zero or more strings ('result' here).
        """
        result = self.application(env, self.start_response)

        """
        The server or gateway transmits the yielded strings (by application)
        to the client, in an unbuffered fashion, completing the
        transmission of each string before requesting another one (in
        other words, applications should perform their own buffering).
        Construct a response and send it back to the client.
        Calls self.finish_response() by giving as argument the
        result outputted by the web application after giving it
        the environment dictionary and the start_response function.
        finish_response actually builds the response and prints it in
        a curl-like format.
        """
        self.finish_response(result)
    """
    method called when handling one request (with self.handle_one_request)
    which takes un-parsed text (bytes object) coming from a recv() call
    (when receiving data from a client request). This method parses the
    first line of the request text, and saves various parts into:
    * self.request_method : first part. e.g. GET
    * self.path           : second part, the url. e.g. /hello
    * self.request_version: third part, HTTP version. e.g. HTTP/1.0
    """
    def parse_request(self, text):
        """
        split the line when encountering a newline (e.g. \n, \r
        \r\n, \v, \f, ...). Then, select only the first line
        (the resulting splitted lines are strings which do NOT
        contain newline characters)
        """
        request_line = text.decode('utf-8').splitlines()[0]
        """
        rstrip([chars]) trims the given string by removing all
        instances of the given chars at the end (right) of the
        given string. In this case, we strip the newline '\r\n'.
        This is useful only if there are many '\r\n' left after
        the first one, stripped by splitlines().
        \r is the carriage return character. \n is the newline.
        The pair carriagereturn-newline is needed as a newline
        symbol in a network terminal session (for example when
        using telnet).
        """
        request_line = request_line.rstrip('\r\n')
        """
        Break down the request line into components.
        split() splits when it encounters whitespaces
        therefore a line like:
        GET /hello HTPP/1.1
        is split into:
        'GET', '/hello', 'HTTP/1.1'
        """
        (self.request_method,   # GET
        self.path,              # /hello
        self.request_version    # HTTP/1.1
        ) = request_line.split()
    """
    method that creates the environment dictionary (required according
    to WSGI specifications) and returns it. This is used in
    self.handle_one_request, and is passed to the web application as
    first argument, when asking for a response from the app.
    """
    def get_environ(self):
        """
        environ dictionary, required to contain the environment
        variables as defined by the Common Gateway Interface
        specification.
        """
        env = {}
        """
        The following code snippet does not follow PEP8 conventions
        but it's formatted the way it is for demonstration purposes
        to emphasize the required variables and their values.
        See https://www.python.org/dev/peps/pep-0333/#environ-variables
        for official WSGI documentation.
        """
        # Required WSGI variables
        env['wsgi.version']     = (1,0)
        env['wsgi.url_scheme']  = 'http'
        # as input, we use a BytesIO object (buffer-like class)
        # initialized with the data (bytes object) of the request
        env['wsgi.input']       = io.BytesIO(self.request_data)
        # sys.stderr is the file object corresponding to the standard error
        env['wsgi.errors']      = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess']= False
        env['wsgi.run_once']    = False
        # Required CGI variables
        # (these were extracted by self.parse_request in self.handle_one_request)
        env['REQUEST_METHOD'] = self.request_method     # GET
        env['PATH_INFO'] = self.path                    # /hello
        env['SERVER_NAME'] = self.server_name           # localhost
        # since the request parameters must be strings, we stringify this
        env['SERVER_PORT'] = str(self.server_port)      # 8888
        return env
    """
    start_response function. This is given as second argument to the
    application object, in order to retrieve a response from the request.
    start_response function is needed according to WSGI specifications.
    The start_response(status, response_headers, exc_info=None) callable
    is used to begin the HTTP response, and it must return a write(body_data)
    callable.
    Parameters:
    * status : string of the form "999 Message here" or "404 Not Found"
    * response_headers : list of (header_name, header_value) tuples
                         describing the HTTP response header
    * exc_info : additional parameter used only if the application has caught
                 an error and is trying to display an error message to the browser
    Returns: write(body_data) which is a callable that takes one positional
    parameter: a string to be written as part of the HTTP response body.
    The write callable is provided only to support existing frameworks, and should
    not be used in new applications or frameworks.
    Here it is used in a simplified manner, just to set server headers,
    without returning any write callable.
    Official WSGI documentation: https://www.python.org/dev/peps/pep-0333/#the-start-response-callable
    Purpose of start_response: https://stackoverflow.com/questions/16774952/wsgi-whats-the-purpose-of-start-response-function
    """
    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary server headers
        server_headers = [
            ('Date', 'Tue, 31 Mar 2015 12:54:48 GMT'),
            ('Server', 'WSGIServer 0.2')
        ]
        # Stores headers by taking the status (passed to start_response),
        # the response_headers (passed to start_response by the app) and
        # the server_headers (built here by hand).
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. For simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response
    """
    function that takes the response ouputted by the application, and
    processes the answer and prints that, together with all the headers.
    This method is invoked at the end of handle_one_request, and the
    argument 'result' is of bytes type.
    """
    def finish_response(self, result):
        # if there are problems when sending the response to the
        # client, this block is skipped
        try:
            # takes status string and all headers saved by start_response
            # (start_response is called when it is passed to the application)
            status, response_headers = self.headers_set
            # formatted response. Note that as newline we use \r\n
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)
            # format all the headers, one in each line.
            # response_headers is a list of tuples (2 elements each).
            # to pass the two elements as {0} and {1} arguments in the
            # formatted string, we unzip the tuple with *
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            # newline
            response += '\r\n'
            # format response given by the app, by glueing each
            # string in the list of strings yielded as response
            # (data is originally bytes, and we convert it to
            # string with .decode('utf-8'))
            for data in result:
                response += data.decode('utf-8')
            # Print formatted response data a la 'curl -v'
            print(''.join(
                '> {line}\n'.format(line=line)
                for line in response.splitlines()
            ))
            """
            socket.sendall(bytes[,flags]) sends data to the socket.
            The socket must be connected to a remote socket.
            The flags argument has the same meaning as flags in .recv()
            Unlike send(), this method continues to send data from 'bytes'
            untile either all data has been sent, or an error occurs.
            On error, an exception is raised.
            Note that the argument (response) must be converted from str
            back to bytes again, since these mechanisms work with bytes
            objects. That's why we use encode() on it.
            """
            self.client_connection.sendall(response.encode())
        finally:
            """
            mark the socket closed. The underlying system resource (e.g.
            a file descriptor) is also closed when all file objects from
            makefile() are closed.
            One this happens, all future operations on the socket will fail.
            The remote end will receive no more data.
            """
            # Closes socket, regardless of the success of the response
            self.client_connection.close()

"""
host and port used in this program. host is localhost.
In this way, you can visit the service (when it is running)
in a browser at localhost:8888
Or you can visit it manually for example through
telnet localhost 8888
"""
SERVER_ADDRESS = (HOST, PORT) = '', 8888

"""
Function that builds a WSGIServer object (the gateway),
using the given server_address and the given application.
The WSGI is something in between, which lets server and
application/framework communicate. This is where the
initialization is done.
"""
def make_server(server_address, application):
    # Builds WSGIServer object
    server = WSGIServer(server_address)
    # Sets the application
    server.set_app(application)
    # Return 'server': the WSGIServer object
    return server

"""
Main program. Execute if this module is run as main file.
[__name__ == '__main__']
When the Python interpreter reads a source file,
it executes all of the code found in it.
Before executing the code, it will define a few special variables.
For example, if the python interpreter is running that module
(the source file) as the main program, it sets the special __name__
variable to have a value "__main__".
If this file is being imported from another module, __name__ will be
set to the module's name.
"""
if __name__ == '__main__':
    # check that there is at least a command line argument
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    """
    the first argument (after the executable's name) is the app path
    in the format NAMEOFAPP:app
    * NAMEOFAPP is the name of the app (e.g. if you have an app called
                pyramidapp.py, NAMEOFAPP = pyramidapp)
    * app is just the word 'app'. Inside the application module, there
                must be an object called app which represents the app
    """
    app_path = sys.argv[1]
    # splits nameofthemodule and 'app'
    module, application = app_path.split(':')
    # import the module and returns it
    module = __import__(module)
    # gets the object 'app' from the imported module, and
    # saves a referenece to the app object in 'application'
    application = getattr(module, application)
    # builds the WSGI server at localhost
    httpd = make_server(SERVER_ADDRESS, application)
    # print information about the running server
    print('WSGIServer: Serving HTTP on port {port} ...\n'.format(port=PORT))
    # start serving, until manually interrupted, waiting for requests
    # and serving responses by printing them in the terminal
    httpd.serve_forever()
