from flask import Flask
from flask import Response
flask_app = Flask('flaskapp')

@flask_app.route('/hello')
def hello_world():
    return Response(
        'Hello world from Flask!\n',
        mimetype='text/plain'
    )

# app object, this is detected from the WSGIServer and
# is used as the application
app = flask_app.wsgi_app
