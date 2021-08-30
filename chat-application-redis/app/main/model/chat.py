from .. import db
import datetime


class Chat(db.Model):
    """ Chat Model for storing chat related details """
    __tablename__ = "chat"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<Chat '{}'>".format(self.name)
