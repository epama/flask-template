from flask_template.model.todo import Todo

class Todolist_service:
    def __init__(self, db):
        self.db = db

    def get_todolist(self, query, sort_column, sort_direction, page):

        res = self.db.all()
        todolist = []
        
        if len(res) > 0:
            for row in res:
                todo = Todo(row["task"],row["id"])
                todolist.append(todo)

        return todolist