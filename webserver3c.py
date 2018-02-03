###########################################################################
# Concurrent server - webserver3c.py                                      #
#                                                                         #
# - Child process sleeps for 60 seconds after handling a client's request #
# - Parent and child processes close duplicate descriptors                #
#                                                                         #
###########################################################################
"""
This server is able to handle concurrent client requests
by cloning itself and letting the clones handle the request (even if
the original process is forced to sleep for 60 seconds thereafter.)
To observe the behavior, fire up the server, and try to make several
requests (e.g. by refreshing the browser). Observe the data that is
printed in the terminal, which will tell you what copy (look at the pid)
of the original process is actually handling the request.
"""
import os
import socket
import time

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection):
    # receives request's data
    request = client_connection.recv(1024)
    # gets pid (proess id: unique identifier of the server
    # process, which is running on your machine) and ppid (
    # pid of the parent process. For example, if you run
    # the server from a shell, ppid is the shell's pid
    print(
        'Child PID: {pid}. Parent PID {ppid}'.format(
            pid=os.getpid(),
            ppid=os.getppid(),
        )
    )
    # prints request
    print(request.decode())
    # response from the server
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    # send response
    client_connection.sendall(http_response)
    # SLEEP! this process will be unavailable for the next 60 seconds
    time.sleep(60)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))
    print('Parent PID (PPID): {pid}\n'.format(pid=os.getpid()))

    while True:
        client_connection, client_address = listen_socket.accept()
        """
        This time, the server loop works differently. Indeed, it works like
        this: it listens for a request, then the server process is forked
        using os.fork() on the server's pid.
        What happens is that a new clone of the original process is produced,
        (it's a child of the original process) and that is assigned pid = 0.
        The original process continues with its own pid.
        The code that follows, is then valid for both processes. Each of them
        will read and execute it. The difference is that the forked process
        (the clone, whose pid is 0), will execute the 'if' part, while the
        original process will only see and execute the 'else' part.
        The sole role of the server parent process becomes just to accept a
        new client connection, fork a new child (clone itself) to handle that
        client request (the clone is supposed to give a response), and loop
        over to accept another client connection. Nothing more.
        The clones' duty (forked children processes) is to process client
        requests.
        """
        pid = os.fork() # only on Unix, simplest way to have concurrency
        if pid == 0:  # child
            # closes the child copy
            listen_socket.close()  # close child copy
            # handles the request
            handle_request(client_connection)
            # closes the connection cloned_server-client
            # Both this and the connection original_server-client
            # must be closed in order to terminate the connection
            # with the client! If one is missing, the connection
            # remains open, unhandled.
            client_connection.close()
            # standard way of closing a process after a fork.
            # the 0 as argument is the status of the process.
            # in this case the status is 0.
            os._exit(0)  # child exits here
        else:  # parent
            # the original server process just closes its connection
            # with the client. It is important that we keep this line,
            # otherwise the connection will remain open, even if the
            # cloned process closes its connection with the client!
            # (The real connection is never really closed unless all
            # the copies are closed, that's why we need this.)
            client_connection.close()  # close parent copy and loop over

if __name__ == '__main__':
    serve_forever()
