from flask import Flask
from flask_restful import Resource, Api,fields, reqparse, abort, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:admin@localhost/todo_db'
app.config['SQLALCHEMY_TRACK_MODIIFICATIONS'] = False
db = SQLAlchemy(app)

## Database Table
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task = db.Column(db.String(200))
    summary = db.Column(db.String(200))

## Create all
# db.create_all()

"""## Temporary
todos = {
    1 : {"task": "Writing the code.", "summary": "Writing the code of Rest"}
}"""

## Configure Parser
task_post_args = reqparse.RequestParser()
task_post_args.add_argument('task', type=str, help="Task is required.", required=True)
task_post_args.add_argument('summary', type=str, help="Summary is required.", required=True)

task_put_args = reqparse.RequestParser()
task_put_args.add_argument('task', type=str)
task_put_args.add_argument('summary', type=str)

resource_fields = {
    'id': fields.Integer,
    'task': fields.String,
    'summary': fields.String
}
class ToDo(Resource):
    @marshal_with(resource_fields)
    def get(self, todo_id):
        task = Todo.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Task not found..")
        return task


    @marshal_with(resource_fields)
    def post(self, todo_id):
        args = task_post_args.parse_args()
        task = Todo.query.filter_by(id=todo_id).first()
        if task:
            abort(409, "Task id is Taken...")
        todo = Todo(task=args['task'], summary=args['summary'])
        db.session.add(todo)
        db.session.commit()
        return todo, 201

    @marshal_with(resource_fields)
    def delete(self, todo_id):
        task = Todo.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Task not found...")
        db.session.delete(task)
        db.session.commit()
        return task

    @marshal_with(resource_fields)
    def put(self, todo_id):
        args = task_put_args.parse_args()
        task = Todo.query.filter_by(id=todo_id).first()
        if not task:
            abort(404, message="Task not found...")
        if args['task']:
            task.task = args['task']
        if args['summary'] :
            task.summary = args['summary']
        return task


class TodoList(Resource):
    def get(self):
        all_tasks = Todo.query.all()
        tasks = {}
        for task in all_tasks:
            tasks[task.id] = {'task': task.task, 'summary': task.summary}
        return tasks

        

api.add_resource(ToDo, '/todo/<int:todo_id>')
api.add_resource(TodoList, '/todos')


if __name__ == ("__main__"):
    app.run(debug=True)