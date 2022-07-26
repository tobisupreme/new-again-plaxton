from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tobisupreme:tobi@localhost:5432/example'
db = SQLAlchemy(app)


class Person(db.model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)


@app.route('/')
def index():
    return 'hello world! I am here'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003)
