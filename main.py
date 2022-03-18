from flask import Flask

app = Flask(__name__)


@app.route('/<param>')
def hello(param):
    return f'<h1>Hello world!</h1><script>alert("{param}")</script>'
