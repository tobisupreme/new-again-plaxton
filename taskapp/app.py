from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tobisupreme:tobi@localhost:5432/dummytasksapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'[Task ID = {self.id} | Task = {self.task}]'


@app.route('/')
def index():
    return render_template('index.html', data=Tasks.query.all())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5501)
