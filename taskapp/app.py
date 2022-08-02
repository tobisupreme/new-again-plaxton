from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', data=[{
        'task': 'Strike a pose'
    }, {
        'task': 'Bend the knee'
    }, {
        'task': 'parse the html'
    }])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5501)
