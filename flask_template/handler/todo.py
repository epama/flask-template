from flask_restful import reqparse, abort, Resource, fields, marshal
from flask_template.model.todo import Todo
from flask_jwt_extended import (jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

todo_fields = {
    "task": fields.String,
    "id": fields.String
}

# Todo
# shows a single todo item and lets you delete a todo item
class Todo_handler(Resource):
    def __init__(self, todo_service):
        parser = reqparse.RequestParser()
        parser.add_argument('task')
        self.parser = parser
        self.todo_service = todo_service
    
    @jwt_required
    def get(self, todo_id):
        todo = Todo(task=None, id=todo_id)
        
        todo = self.todo_service.get_todo(todo)

        return marshal(todo, todo_fields), 200
    
    @jwt_required
    def post(self):
        args = self.parser.parse_args()
        todo = Todo(task=args['task'], id=None)

        todo = self.todo_service.add_todo(todo)

        return marshal(todo, todo_fields), 200
    
    @jwt_required
    def delete(self, todo_id):
        todo = Todo(task=None, id=todo_id)

        todo = self.todo_service.delete_todo(todo)

        return '', 204

    @jwt_required
    def put(self, todo_id):
        args = self.parser.parse_args()
        todo = Todo(task=args['task'], id=todo_id)

        todo = self.todo_service.update_todo(todo)

        if todo.is_found:
            return marshal(todo, todo_fields), 200
    
        return marshal(todo, todo_fields), 201