import random
import string

class TodoDoesNotExist(Exception):
    pass

class Todo:
    def __init__(self, task, id):
        if task is not None:
            self.task = task

        if id is not None:
            self.id = id  

        self.is_found = False

    def generate_id(self, size=6, chars=string.ascii_uppercase + string.digits):  
        self.id = ''.join(random.choice(chars) for _ in range(size))
        return 1