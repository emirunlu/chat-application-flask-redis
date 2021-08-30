from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class ChatDto:
    api = Namespace('chat', description='chat related operations')
    chat = api.model('chat', {
        'name': fields.String(required=True, description='chat name')
    })


class MessageDto:
    api = Namespace('chat', description='message related operations')
    message = api.model('chat', {
        'message': fields.String(required=True, description='message data')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password')
    })
