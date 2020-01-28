from flask import Flask, request, abort
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask.signals import got_request_exception

#### IMPORT DRIVERS
from flask_template.driver.tinydb import init_db


#### IMPORT SERVICES
from flask_template.service.todo import Todo_service
from flask_template.service.todolist import Todolist_service

#### IMPORT HANDLERS
from flask_template.handler.todolist import Todolist_handler
from flask_template.handler.todo import Todo_handler
from flask_template.handler.userlogin import UserLogin
from flask_template.handler.tokenrefresh import TokenRefresh

from config import Config
from log_setup import LogSetup
import logging

def create_app(config_class=Config):
    app = Flask(__name__)
    
    ############## CONFIG INITIALIZATION
    app.config.from_object(config_class)

    ############## DRIVER INITIALIZATION
    db = init_db(app)

    ############## SERVICE INITIALIZATION
    todo_service = Todo_service(db)
    todolist_service = Todolist_service(db)

    errors = {
        "ExpiredSignatureError": {
            "status": 401
        },
        "TodoDoesNotExist": {
            "status": 404
        }
    }

    ############## HANDLER INITIALIZATION
    rest = Api(app, errors=errors, catch_all_404s=True)
    rest.add_resource(Todolist_handler, '/todos', resource_class_kwargs={ 'todolist_service': todolist_service })
    rest.add_resource(Todo_handler, '/todo', '/todo/<todo_id>',resource_class_kwargs={ 'todo_service': todo_service })
    rest.add_resource(UserLogin, '/login')
    rest.add_resource(TokenRefresh, '/refreshtoken')

    JWTManager(app)
    LogSetup(app)
    
    return app

config = Config()
app = create_app(config)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

if __name__ != '__main__':  
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)