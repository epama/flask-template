from flask_restful import reqparse, abort, Resource, fields, marshal
from flask_jwt_extended import (create_access_token, create_refresh_token)
from flask import current_app as app

class UserLogin(Resource):
    def __init__(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        self.parser = parser

    def post(self):
        args = self.parser.parse_args()
        username = args['username']

        access_token = create_access_token(identity = username)
        refresh_token = create_refresh_token(identity = username)
        
        return {
            'message': 'Logged in as {}'.format(username),
            'access_token': access_token,
            'refresh_token': refresh_token
        }