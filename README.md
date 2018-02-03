# Web servers in python 3
Example code of how to build and run locally a server from scratch using python 3, and how to build a WSGI middleware from scratch and use it to let a server and any python web application talk to each other. Examples of simple applications built with different frameworks (pyramid, flask, django) are present and can be tested.

The code is a porting to python 3 of the examples shown in the article series [Let's Build A Web Server](https://ruslanspivak.com/lsbaws-part1/)

The programs are also thoroughly commented and documented, so that one can use these programs to learn much more in detail about servers and WSGI applications than simply reading the articles and copying the examples.

# Usage

## webserver 1 - simple server
Run the server
```
python webserver1.py
```
While the server is running, use a browser to visit the url
```
localhost:8888/hello
```
or connect to the server using telnet from the command line:
```
$ telnet localhost 8888
```
and make an HTTP request 'manually' by typing:
```
GET /hello HTTP/1.1
```
(this asks the server to retrieve the resource at the url /hello and bring it to you. Same thing you would do by visiting the url ina browser. In this case, the response is just displayed in the terminal)

## webserver 2 - WSGI server
Here we use a WSGI (Python Web Server Gateway Interface) in order to run a web application under our server, without the need of modifying the server in order to accommodate all possible different frameworks.
Create a virual environment with pip, so that you can install the frameworks and use them just for this application, without polluting your global python installation.
If you don't have virtualenv installed already, install it via:
```
[sudo] pip install virtualenv
```
Then make a virtualenv wherever you want (the location is not important, and is not related to the location of your python scripts/application). Also the name of the virtualenv is unimportant. Here we use 'venv', but you could substitute it with 'xyz_fancy_name' or '~/whereverIwant/whateverNameIPrefer':
```
virtualenv -p python3 venv
```
Activate the virtualenv with the command '.' followed by the path to the file bin/activate, which lives inside the virtualenv (depending on where you are, you need to specify the path in a proper manner. In this case, we assume we are in the same directory where the venv directory lives. That's why we access it through ./venv/. Note that the first dot is the command, the second dot is part of the path):
```
. ./venv/
```
You should see your terminal changing to something like:
```
(venv) $
```
Now you *are* in the virtualenv, no matter where you physically are. This means that you can change your directory normally, and (venv) won't go away from your prompt.
Install the frameworks needed to run the web applications:
```
pip install pyramid
pip install flask
pip install django
```
The configuration is completed! Now you can forget everything you have done (you won't need to do this again), and you can just focus on running the applications.
To fire up the server and run one of the simple web applications, type (suppose the code for the application lives in the file nameoftheapplication.py):
```
python webserver2.py nameoftheapplication:app
```
For example, if you want to run the application that uses the Pyramid framework, which is in the file pyramidapp.py, you should type:
```
python webserver2.py pyramidapp:app
```
Now, as in the case of webserver1, you can visit the url
```
localhost:8888/hello
```
or connect and make a request directly via telnet:
```
telnet localhost 8888
GET /hello HTTP/1.1
```
and voilà! The app will respond with wathever it is programmed to do and you will be able to see the response (in this case, it should just print something like "Hello World").
You can try 4 different simple apps:
* pyramidapp.py (pyramid app)
* flaskapp.py	(flask app)
* djangoapp.py	(django app, more complex)
* wsgiapp.py	(hand-made app, without using any framework)

Once you are done with the virtualenv, simply deactivate by typing:
```
deactivate
```
## webserver 3 - handling multiple requests
*(webserver3a.py was not included, since it is just a simple server, like the one in webserver1 or webserver2)*

**webserver3b - sleeping server**
This server sleeps for one minute after it handles one request. Try it with:
```
python webserver3b.py
```
and then make requests to the server. It will sleep!

**webserver3c - concurrent server**
This server is able to handle multiple requests (even if it is forced to sleep after handling one!) by cloning itself ('forking a child') and making the clone actually handle the request in its place.
Try it with:
```
python webserver3c.py
```
and make multiple requests. They will be handled!

**webserver3d - zombies-generating concurrent server**
This is exactly like webserver3c, with the only difference that the original server process doesn't close the connection with the client after each request. This can create a lot of processes which remain open, and it can reach the maximum number of open processes on your machine!
See how many open processes your system can handle by typing:
```
ulimit -a
```
and then look for 'open files'.
Try to set a low cap of 256 on this value with:
```
ulimit -n 256
```
Then fire up your server with
```
python webserver3d.py
```
And make a lot of requests with the script client3.py (you can't do them by hand!)
```
python client3.py --max-clients=300
```
(read the comments in the client3.py file for more command line options)
The server will stop because of the error 'Too many open files', and it will create zombie processes!
To observe the creation of a zombie process, start up the server again:
```
python webserver3d.py
```
make a request, for example with (here we use the program HTTpie, you can use a browser, or any other command line program)
```
http localhost:8888/hello
```
and finally run the `ps` command, and grep (search) for running python processes on your machine:
```
ps auxw | grep -i python | grep -v grep
```
you should be able to see a process named <defunct>, whose status is Z+ (aka: zombie).
This is a child process whose parent process didn't wait for it to correctly terminate, and now it is occupying memory and nobody is handling it!

**webserver3e - server receiving asynchronous SIGCHLD notifications**
To correctly handle a child process, and avoid that that becomes a zombie, the parent process must be instructed to *wait* to get the termination status from the child process that terminates.
But your parent process can't wait indefinitely for its child to send him a termination status (if there is no terminated child process, the *wait* will block your server, waiting for something that will never happen).
The solution is:
* when a child process exits, the kernel sends a SIGCHLD signal.
* the parent process can collect the signal SIGCHLD (it's like a notification that tells it that the child is terminating)
* the parent process *waits* for the child, to collect its termination status
Start up the server:
```
python webserver3e.py
```
make a request with a tool of your choice.
You may get an error! The accept() system call may be interrupted by the SIGCHLD event arriving.

**webserver3f - server that avoids interruptions from SIGCHLD**
This program implements a solution to the previous problem. In the serve_forever loop, the server looks for possible interruptions as the ones described above. If the accept() call is interrupted for the described reason, the program catches the exception, and handles the problem by starting a new accept() call. In this way, possible interruptions are bypassed, and the server doesn't crash.
Try it with:
```
python webserver3f.py
```
and make a request to the server.
You can also verify using `ps` that there are no zombies floating around this time...
...unless you make too many requests!
Try to break the server by simulating 128 clients making a request each:
```
python client3.py --max-clients 128
```
Now run in another terminal:
```
ps auxw | grep -i python | grep -v grep
```
and you will find a lot of zombies!
The problem here is that for 128 clients, 128 childs are forked, each handling one request. They then all terminate at the same time (approximately), and therefore the original server process becomes flooded with 128 signals SIGCHLD. These signals are not enqueued, and the original process can handle only some of them. Therefore only a few children can be correctly terminated. All the others become zombies!

**webserver3g - concurrent server, final version**
A final modification is needed, in that the server's signal handler (the one that listens for signals) needs to be instructed to call waitpid() instead of wait(). This ensures that all terminated child processes are taken care of.
Try it with:
```
python webserver3g.py
```
and stress-test it with:
```
python client3.py --max-clients 128
```
You can verify that there are no zombies this time, using `ps`!
