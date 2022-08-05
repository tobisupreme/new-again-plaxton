from flask import Flask, render_template
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


@app.route('/')
def index():
    return render_template('index.html', todos=Todos.query.order_by('id').all())


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=4000)
