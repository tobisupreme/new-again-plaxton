from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tobisupreme:tobi@localhost:5432/tasksapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'[Task ID: {self.id}, Task: {self.name}]'


@app.route('/')
def index():
    task = Tasks.query.all()
    return 'hello world! ' + task[0].name + ' is here o!'


if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=5003)
