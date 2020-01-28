from tinydb import where
from flask_template.model.todo import TodoDoesNotExist

class Todo_service:
    def __init__(self, db):
        self.db = db

    def add_todo(self, todo):   
        todo.generate_id()
        self.db.insert({'id': todo.id,'task': todo.task})

        return todo

    def update_todo(self, todo):
        if self.exist_todo(todo):
            todo.is_found = True
            self.db.update({'task': todo.task}, where('id') == todo.id)
        else:
            self.add_todo(todo)

        return todo

    def delete_todo(self, todo):
        if self.exist_todo(todo):
            todo.is_found = True
            self.db.remove(where('id') == todo.id)
            return todo
        else:
            raise TodoDoesNotExist('Todo ID: '+todo.id+' does not exist')

    def get_todo(self, todo):
        res = self.db.search(where('id') == todo.id)

        if len(res) > 0:
            todo.task = res[0]['task']
            todo.is_found = True
            return todo
        else:
            raise TodoDoesNotExist('Todo ID: '+todo.id+' does not exist')
        

    def exist_todo(self, todo):
        res = self.db.search(where('id') == todo.id)

        if len(res) > 0:
            return True

        return False