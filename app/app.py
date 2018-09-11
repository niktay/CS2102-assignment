from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


def run():
    app.run(debug=True, host='0.0.0.0', port=5000)
