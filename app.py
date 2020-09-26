from flask import Flask, render_template, url_for, redirect, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import collections
import json

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    completed = db.Column(db.Boolean)

    def __init__(self, title, completed):
        self.title = title
        self.completed = completed


class TodoSerializer:
    def __init__(self, todo):
        self.todo = todo


    def to_dict(self):
        return collections.OrderedDict([
            ('id', self.todo.id),
            ('title', self.todo.title),
            ('completed', self.todo.completed)
        ])


@app.route('/api/v1/todos', methods=['GET', 'POST'])
def todos():
    if request.method == 'GET':
        todos = Todo.query.all()
        # for todo in todos:
        serialized = [TodoSerializer(todo).to_dict() for todo in todos]
        return jsonify({
            'todos': serialized,
            'next_id': 3
        })
    elif request.method == 'POST':
        title = request.json['title']
        completed = False
        todo = Todo(title, completed)
        db.session.add(todo)
        db.session.commit()
        serialized = TodoSerializer(todo).to_dict()
        return jsonify(serialized)

@app.route('/api/v1/todos', methods=['DELETE', "GET"])
def delete():
    if request.method == 'DELETE':
        idd = request.json['id']
        print(idd)
        todo = Todo.query.get(idd)
        db.session.delete(todo)
        db.session.commit()
        todos = Todo.query.all()
        serialized = [TodoSerializer(todo).to_dict() for todo in todos]
        return jsonify(serialized)
    elif request.method == "GET":
        todos = Todo.query.filter_by(id=id)
        serialized = [TodoSerializer(todo).to_dict() for todo in todos]
        return jsonify(serialized)

@app.route('/api/v1/todos', methods=['GET', 'PUT'])
def complete():
    if request.method == 'PUT':
        idd = request.json['id']
        todo = Todo.query.get(idd)
        # print(todo.completed)
        if todo.completed == True:
            todo.completed = False
        else:
            todo.completed = True
        print(todo.completed)
        db.session.add(todo)
        db.session.commit()
        serialized = TodoSerializer(todo).to_dict()
        # print(serialized)
        return jsonify(serialized)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        title = request.form['title']
        completed = True
        todo = Todo(title, completed)
        db.session.add(todo)
        db.session.commit()
        return jsonify({"success": "success"})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
