from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tobisupreme:tobi@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'persons'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'[Person ID: {self.id}, name: {self.name}]'


db.create_all()


@app.route('/')
def index():
    person = Person.query.all()
    return 'hello world! ' + person[0].name + ' is here o!'


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5003)
