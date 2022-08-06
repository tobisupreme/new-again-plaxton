from os import abort
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Define App and set configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tobisupreme:tobi@localhost:5432/practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Instantiate SQL Alchemy for DB interaction
db = SQLAlchemy(app)

# Instantiate Migrate for schema modifications
migrate = Migrate(app, db)


# define Table schema
class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return f'[Todo ID: {self.id} | Todo description: {self.description} | Todo_complete_status: {self.completed}]\n'


# define create update todo completed status endpoint
@app.route('/todo/<todo_id>/update', methods=['POST'])
def set_todo_complete(todo_id):
    error = False
    try:
        # get data from client request
        todo_id = todo_id
        todo_status = request.get_json()['completed']
        # attach client request to database instance
        todo = Todos.query.get(todo_id)
        # add request to data base
        todo.completed = todo_status
        db.session.add(todo)
        # for debugging, print to the console
        print(todo)
        # commit transaction to database
        db.session.commit()
    except:
        # in case of error, rollback transaction
        error = True
        db.session.rollback()
    finally:
        # close database session
        db.session.close()
        if error:
            abort()
        else:
            return redirect(url_for('index'))


# define create todo endpoint
@app.route('/todo/add', methods=['POST'])
def add_todo():
    error = False
    body = {}
    try:
        # get data from client request
        add_todo = request.get_json()['description']
        # attach client request to database instance
        todo = Todos(description=add_todo)
        # add request to data base
        db.session.add(todo)
        # read from database and attach to a response object
        body['description'] = todo.description
        # for debugging, print to the console
        print(body)
        # commit transaction to database
        db.session.commit()
    except:
        # in case of error, rollback transaction
        error = True
        db.session.rollback()
    finally:
        # close database session
        db.session.close()
        if error:
            abort()
        else:
            return jsonify(body)


# define homepage route
@app.route('/')
def index():
    return render_template('index.html', todos=Todos.query.order_by('id').all())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
