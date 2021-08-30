from collections import namedtuple
import uuid
import datetime
import redis

from app.main import db
from app.main.model.chat import Chat
from app.main.model.user import User
from app.main.model.user_chats import UserChats
from app.main.model.message import Message
from typing import Dict, Tuple

r = redis.StrictRedis(host='localhost', port=6379, db=0, charset='utf-8', decode_responses=True)

def save_new_chat(name):
    chat = Chat.query.filter_by(name=name).first()
    if not chat:
        new_chat = Chat(
            name=name,
            created_on=datetime.datetime.utcnow()
        )
        save_changes(new_chat)
        response_object = {
            'status': 'success',
            'message': 'Chat created.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Chat already exists.',
        }
        return response_object, 409

def get_all_chats():
    return Chat.query.all()

def connect_to_chat(chat: Chat, username):
    current_chat = UserChats.query.filter_by(username = username, chat_name = chat.name).first()
    if not current_chat:
        new_user_chat = UserChats(
            username=username,
            chat_name=chat.name
        )
        db.session.add(new_user_chat)
        db.session.commit()

def disconnect_from_chat(chat: Chat, username):
    current_chat = UserChats.query.filter_by(username = username, chat_name = chat.name).first()
    if current_chat:
        db.session.delete(current_chat)
        db.session.commit()

def get_users_in_chat(chat: Chat) -> None:
    return UserChats.query.filter_by(chat_name = chat.name).all()

def get_a_chat(name):
    return Chat.query.filter_by(name=name).first()

def delete_a_chat(data: Chat) -> None:
    db.session.delete(data)
    db.session.commit()

def save_changes(data: Chat) -> None:
    db.session.add(data)
    db.session.commit()

def stream_chat(name):
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe(name)
    for message in pubsub.listen():
        print('['+name+'] RECEIVED MSG: %s\n\n' % message['data'])
        yield 'data: %s\n\n' % message['data']

def message_chat(username, chat_name, message):
    now = datetime.datetime.now()
    r.publish(chat_name, u'[%s] %s: %s' % (now.isoformat(), username, message))
    new_message = Message(
            username=username,
            chat_name=chat_name,
            message_type='MESSAGE',
            created_on=now,
            message=message
        )
    db.session.add(new_message)
    db.session.commit()
    print(u'[%s] SENT MSG: [%s] %s: %s' % (chat_name, now.replace(microsecond=0).time().isoformat(), username, message))

def get_messages(chat_name, size=100):
    """fetch messages limited by size"""
    messages = Message.query.filter_by(chat_name = chat_name).order_by(Message.created_on.desc()).limit(size).all()
    result_list = []
    for row in messages:
            result_list.append({
                'username':row.username,
                'name': row.chat_name,
                'message_type': row.message_type,
                'created_on': row.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                'message': row.message
                })
    return result_list
