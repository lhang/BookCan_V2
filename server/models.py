#! -*- coding: utf-8 -*-


from server import db
from werkzeug.security import generate_password_hash, check_password_hash

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('can_id', db.Integer, db.ForeignKey('book_can.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    passwd = db.Column(db.Text)
    join_time = db.Column(db.DateTime)
    authentication = db.Column(db.Boolean)
    email = db.Column(db.String(30))
    latest_login = db.Column(db.DateTime)
    latest_ip = db.Column(db.String(15))

    book_can = db.relationship('BookCan', backref='user', lazy='dynamic')
    discuss = db.relationship('Discuss', backref='user', lazy='dynamic')
    message_board = db.relationship('MessageBoard', backref='user', lazy='dynamic')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return unicode(self.id)

    def set_passwd(self, passwd):
        passwd = generate_password_hash(passwd)
        self.passwd = passwd
        return True

    def check_password(self, passwd):
        return check_password_hash(self.passwd, passwd)


class BookCan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    intro = db.Column(db.Text)
    time = db.Column(db.DateTime)
    modify_permission = db.Column(db.Boolean)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book = db.relationship('Book', backref='can', lazy='dynamic')
    discuss = db.relationship('Discuss', backref='can', lazy='dynamic')


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    time = db.Column(db.DateTime)

    can = db.relationship('Tag', secondary='tags',
                          backref=db.backref('tag', lazy='dynamic'),
                          lazy='dynamic')


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    intro = db.Column(db.Text)
    link = db.Column(db.Text)
    time = db.Column(db.DateTime)

    can_id = db.Column(db.Integer, db.ForeignKey('book_can.id'))


class Discuss(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    can_id = db.Column(db.Integer, db.ForeignKey('book_can.id'))


class MessageBoard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    time = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

