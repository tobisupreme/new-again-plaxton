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
    completed = db.Column(db.Boolean(), default=False)
    list_id = db.Column(db.Integer, db.ForeignKey(
        'lists.id'), nullable=False, default=1)

    def __repr__(self):
        return f'[Todo ID: {self.id} | Todo description: {self.description} | Todo_complete_status: {self.completed}]\n'


class Todolist(db.Model):
    __tablename__ = 'lists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todos', backref='list', lazy=True)

    def __repr__(self):
        return f'[list id = {self.id} | list name = {self.name}]\n'


# define delete todo endpoint
@app.route('/todo/<todo_id>/delete', methods=['DELETE'])
def delete_todo(todo_id):
    error = False
    try:
        # get data from client request
        todo_id = todo_id
        # attach client request to database instance
        todo = Todos.query.get(todo_id)
        # delete todo from data base
        db.session.delete(todo)
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
        abort(500)
    else:
        return jsonify({'success': True})


# define delete todolist endpoint
@app.route('/lists/<list_id>/delete', methods=['DELETE'])
def delete_todolist(list_id):
    error = False
    try:
        # get database instance
        todolist = Todolist.query.get(list_id)
        # delete todo from data base
        db.session.delete(todolist)
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
        abort(500)
    else:
        return jsonify({'success': True})


# define update todo completed status endpoint
# @app.route('/lists/<list_id>/update', methods=['POST'])
# def set_todolist_complete(list_id):
#     error = False
#     try:
#         # get data from client request
#         list_id = list_id
#         list_status = request.get_json()['status']
#         # attach client request to database instance
#         todolist = Todolist.query.filter_by(list_id=list_id)
#         # # add request to data base
#         # todo.completed = todo_status
#         db.session.add(todo)
#         # for debugging, print to the console
#         print(todo)
#         # commit transaction to database
#         db.session.commit()
#     except:
#         # in case of error, rollback transaction
#         error = True
#         db.session.rollback()
#     finally:
#         # close database session
#         db.session.close()
#         if error:
#             abort(500)
#     return redirect(url_for('index'))


# define update todo completed status endpoint
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
            abort(500)
    return redirect(url_for('index'))


# define create todolist endpoint
@app.route('/lists/add', methods=['POST'])
def add_todolist():
    error = False
    body = {}
    try:
        # get data from client request
        add_todolist = request.get_json()['name']
        # attach client request to database instance
        todolist = Todolist(name=add_todolist)
        # add request to data base
        db.session.add(todolist)
        # read from database and attach to a response object
        todolist_id = Todolist.query.filter_by(name=add_todolist).all()
        body['listname'] = todolist.name
        print(todolist_id)
        body['list_id'] = todolist_id[0].id
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


# define create todo endpoint
@app.route('/todo/add', methods=['POST'])
def add_todo():
    error = False
    body = {}
    try:
        # get data from client request
        description = request.get_json()['description']
        list_id = request.get_json()['list_id']

        # attach client request to database instance
        todo = Todos(description=description, list_id=list_id)

        # add request, then commit to database
        db.session.add(todo)
        db.session.commit()

        # read from database and attach to a response object
        body['description'] = todo.description
        body['id'] = todo.id
        
        # for debugging, print to the console
        print(body)
    except:
        # in case of error, rollback transaction
        error = True
        db.session.rollback()
    finally:
        # close database session
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify(body)


# define todolist route
@app.route('/lists/<list_id>')
def get_todolist(list_id):
    return render_template('index.html',
                           lists=Todolist.query.all(),
                           active_list=Todolist.query.get(list_id),
                           todos=Todos.query.filter_by(list_id=list_id).order_by('id').all())


# define homepage route
@app.route('/')
def index():
    return redirect(url_for('get_todolist', list_id=1))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
