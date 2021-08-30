from .. import db
import datetime

class Message(db.Model):
    """ Message Model for storing message related details """
    __tablename__ = "message"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=False, nullable=False)
    chat_name = db.Column(db.String(50), unique=False, nullable=False)
    message_type = db.Column(db.String(50), unique=False, nullable=False)
    message = db.Column(db.String(255), unique=False, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Message '{}'>".format(self.message)
