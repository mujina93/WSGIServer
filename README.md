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
(For example, if you want to run the application that uses the Pyramid framework, which is in the file pyramidapp.py, you should type:
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

Once you are done with the virtualenv, simply deactivate by typing:
```
deactivate
```
