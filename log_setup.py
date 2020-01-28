import logging
import sys
from flask.logging import default_handler
from flask import request, got_request_exception, current_app
import json

class LogSetup():
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        werkzeug = logging.getLogger("werkzeug")
        werkzeug.disabled = True

        formatter = logging.Formatter("[%(asctime)s.%(msecs)03d] (%(levelname)s) %(message)s","%m-%d-%Y %H:%M:%S")
        default_handler.setFormatter(formatter)
        app.logger.setLevel(app.config['LOG_LEVEL'])

        app.after_request(self.cleanup)
        got_request_exception.connect(self.bailout, app)
    
    def bailout(self, app, exception):
        app.logger.error('%s %s %s %s %s', request.remote_addr, request.method, request.url, type(exception).__name__, exception)
  
    def cleanup(self, response):
        if response.status_code >= 200 and response.status_code <= 299:
            resp_json = response.get_json()
            current_app.logger.info('%s %s %s %s', request.remote_addr, request.method, request.url, resp_json)
        return response        