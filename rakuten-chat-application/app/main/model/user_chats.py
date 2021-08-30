from .. import db
import datetime

class UserChats(db.Model):
    """ Chat to User Model for storing logged in user related details """
    __tablename__ = "user_chats"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    chat_name = db.Column(db.String(50), unique=False, nullable=False)

    def __repr__(self):
        return "<User Chat '{}'>".format(self.username + ' ' + self.chat_name)