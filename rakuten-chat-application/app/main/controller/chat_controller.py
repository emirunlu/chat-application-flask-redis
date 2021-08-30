import json

from flask import request, Response
from flask_restx import Resource

from app.main.util.decorator import admin_token_required
from app.main.service.auth_helper import Auth
from ..util.dto import ChatDto, MessageDto
from ..service.chat_service import connect_to_chat, disconnect_from_chat, save_new_chat, get_all_chats, get_a_chat, get_users_in_chat, delete_a_chat, stream_chat, message_chat, get_messages
from typing import Dict, Tuple

api = ChatDto.api
_chat = ChatDto.chat
_message = MessageDto.message

@api.route('/')
class ChatList(Resource):
    @api.doc('list_of_chats')
    @api.marshal_list_with(_chat, envelope='data')
    def get(self):
        """List all chats"""
        return get_all_chats()

@api.route('/<name>')
@api.param('name', 'The Chat identifier')
@api.response(404, 'Chat not found.')
class Chat(Resource):
    @api.doc('get a chat')
    @api.marshal_with(_chat)
    def get(self, name):
        """Get a chat given its identifier"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            return chat

    @api.response(201, 'Chat successfully created.')
    @api.doc('create a new chat')
    def post(self, name):
        """Creates a new Chat """
        return save_new_chat(name)

    @api.response(204, 'Chat successfully deleted.')
    @api.doc('deletes a chat')
    def delete(self, name):
        """Deletes a Chat"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            delete_a_chat(data=chat)
            return Response(status=204)

@api.route('/<name>/message')
@api.param('name', 'The Chat identifier')
@api.response(404, 'Chat not found.')
class ChatMessage(Resource):
    @api.doc('stream messages from a chat')
    def get(self, name):
        """Stream a chat given its identifier"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            user = Auth.get_logged_in_user(request)
            connect_to_chat(chat, user.username)
            return Response(stream_chat(name), mimetype="text/event-stream")

    @api.response(204, 'Disconnected successfully.')
    @api.doc('disconnect from chat')
    def delete(self, name):
        """Disconnect from chat given its identifier"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            user = Auth.get_logged_in_user(request)
            disconnect_from_chat(chat, user.username)
            return Response(status=204)

    @api.expect(_message, validate=True)
    @api.response(204, 'Message sent.')
    @api.doc('send message to chat')
    def post(self, name):
        """Messages a chat"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            user = Auth.get_logged_in_user(request)
            message_chat(user.username, name, request.json['message'])
            return Response(status=204)

@api.route('/<name>/messagehistory')
@api.param('name', 'The Chat identifier')
@api.response(404, 'Chat not found.')
class ChatMessageHistory(Resource):
    @api.doc('get message history from a chat')
    def get(self, name):
        """Get message history from chat given its identifier"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            messages = get_messages(name)
            return messages

@api.route('/<name>/users')
@api.param('name', 'The Chat identifier')
@api.response(404, 'Chat not found.')
class ChatUserList(Resource):
    @api.doc('get connected users within a chat')
    def get(self, name):
        """Get connected users within a chat"""
        chat = get_a_chat(name)
        if not chat:
            api.abort(404)
        else:
            chats = get_users_in_chat(chat)
            return [o.username for o in chats]