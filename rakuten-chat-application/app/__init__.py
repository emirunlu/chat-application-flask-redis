from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.chat_controller import api as chat_ns

blueprint = Blueprint('api', __name__)
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Api(
    blueprint,
    title='CHAT APPLICATION',
    version='1.0',
    description='a chat application api',
    authorizations=authorizations,
    security='apikey'
)

api.add_namespace(chat_ns, path='/chat')
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
