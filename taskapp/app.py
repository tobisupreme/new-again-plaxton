from crypt import methods
from flask import Flask, redirect, render_template, request, url_for
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


@app.route('/tasks/create', methods=['POST'])
def create_task():
    task_desc = request.form.get('task', '')
    task = Tasks(task=task_desc)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/')
def index():
    return render_template('index.html', data=Tasks.query.all())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5501)
