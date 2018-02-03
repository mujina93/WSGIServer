###########################################################################
# Concurrent server - webserver3d.py                                      #
#                                                                         #
###########################################################################
"""
The only difference with webserver3d is that this server doesn't close the
connection with the client after a request is accepted. This causes an
unwanted behavior: a lot of connections with the client remain open,
and the original process could even run out of file descriptors (i.e.
it could reach the maximum number of cloned/children processes imposed
by the system.)
To see what is the maximum number of file descriptors that your system
can handle, look at: 'open files' after you type:
ulimit -a
To set this value (say, to 256), type:
ulimit -n 256
After this, if you fire up this server, you won't be able to make more than
256 requests without making the server crash.
To test this behavior, run the script client3.py, which simulates the clients
(you can't do that manually!). After the server is up, type:
python client3.py --max-clients=300
and observe.
"""
import os
import socket

SERVER_ADDRESS = (HOST, PORT) = '', 8888
REQUEST_QUEUE_SIZE = 5


def handle_request(client_connection):
    request = client_connection.recv(1024)
    http_response = b"""\
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)


def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ...'.format(port=PORT))

    clients = []
    while True:
        client_connection, client_address = listen_socket.accept()
        # store the reference otherwise it's garbage collected
        # on the next loop run
        clients.append(client_connection)
        pid = os.fork()
        if pid == 0:  # child
            listen_socket.close()  # close child copy
            handle_request(client_connection)
            client_connection.close()
            os._exit(0)  # child exits here
        else:  # parent
            # client_connection.close()
            print(len(clients))

if __name__ == '__main__':
    serve_forever()
