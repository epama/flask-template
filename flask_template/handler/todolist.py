from flask_restful import reqparse, abort, Resource, fields, marshal
from flask_jwt_extended import (jwt_required)

todo_fields = {
    "task": fields.String,
    "id": fields.String
}

class Todolist_handler(Resource):
    def __init__(self, todolist_service):
        parser = reqparse.RequestParser()
        parser.add_argument('q')
        parser.add_argument('sort_column')
        parser.add_argument('sort_direction')
        parser.add_argument('page')
        self.parser = parser

        self.todolist_service = todolist_service

    @jwt_required
    def get(self):
        args = self.parser.parse_args()
        todolist = self.todolist_service.get_todolist(query=args['q'], sort_column=args['sort_column'], sort_direction=args["sort_direction"], page=args["page"])

        return marshal(todolist, todo_fields), 200