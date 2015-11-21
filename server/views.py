#! -*- coding: utf-8 -*-

from datetime import datetime

from flask import redirect, abort, jsonify, render_template
from flask import url_for, request, flash

from flask.ext.sqlalchemy import Pagination
from flask.ext.login import login_required, current_user, login_user, logout_user
from flask.ext.mail import Message

from server import app, db
from server import login_manager
from models import User, MessageBoard, Discuss
from models import Book, BookCan, Tag
from forms import LoginForm, CanForm, RegistForm
from forms import MeaageForm, BookForm

ITEM_NUM_PER_PAGE = 30

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    user.latest_login = datetime.now()
    user.latest_ip = request.remote_addr
    db.session.commit()
    return user


@app.route('/')
@app.route('/cans/<page>')
def index(page=1):
    book_can_pagination = BookCan.query.order_by(BookCan.time).paginate(int(page), ITEM_NUM_PER_PAGE, False)
    books = Book.query.order_by(Book.time).limit(10)
    msg_board = MessageBoard.query.order_by(MessageBoard.time).limit(20)
    tag = Tag.query.limit(6)
    return render_template('index.html',
                           book_can = book_can_pagination.items,
                           books = books,
                           msg_board = msg_board,
                           tag = tag,
                           pagination = book_can_pagination,
                           endpoint = index)


@app.route('/can/<id>/<page>', methods=['GET', 'POST'])
def can_info(id, page=1):
    book_can = BookCan.query.get_or_404(id)
    if request.method == 'GET':
        books = book_can.book.all()
        discuss_pagination = book_can.discuss.paginate(int(page), ITEM_NUM_PER_PAGE, False)
        return render_template('candetail.html',
                               book_can = book_can,
                               books = books,
                               discusses = discuss_pagination.items,
                               discuss_pagination = discuss_pagination,
                               endpoint = 'can_info')
    if request.method == 'POST':
        content = request.form.get('content')
        discuss = Discuss(content=content, time=datetime.now())
        current_user.discuss.append(discuss)
        book_can.discuss.append(discuss)
        db.session.add(discuss)
        db.session.commit()
        return redirect(url_for('can_info', id=id, page=1))


@app.route('/new/can', methods=['GET', 'POST'])
@login_required
def create_can():
    form = CanForm()
    if request.method == 'GET':
        return render_template('create_can.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            modify_permission = True if request.form.get('modify_permission') == 'y' else False
            print modify_permission, modify_permission=='y'
            can = BookCan(name=form.name.data, intro=form.intro.data,
                          time=datetime.now(), modify_permission=modify_permission)
            current_user.book_can.append(can)
            db.session.add(can)
            db.session.commit()
            return redirect(url_for('book_info', id=can.id))
        else:
            flash('请检查输入内容并重试')
            return render_template('create_can.html', form=form)


@app.route('/new/book/<id>', methods=['GET', 'POST'])
def book_info(id):
    form = BookForm()
    book_can = BookCan.query.get(id)
    if request.method == 'GET':
        return render_template('add_book.html', form=form,
                                id=id)
    if request.method == 'POST':
        if form.validate_on_submit():
            book = Book(name=form.name.data, link=form.link.data,
                        intro=form.intro.data)
            book_can.book.append(book)
            db.session.add(book)
            db.session.commit()
            btn = request.form.get('btn')
            if btn == u'继续添加':
                return render_template('add_book.html', form=BookForm(), id=id)
            else:
                return redirect(url_for('can_info', id=id, page=1))
        else:
            flash('wrong')
            return render_template('add_book.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.passwd.data):
                remember_me = True if form.remember_me.data == 'on' else False
                login_user(user, remember=remember_me)
                next = request.args.get('next') or url_for('index')
                return redirect(next)
            else:
                flash('请检查账号或密码')
                return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/regist', methods=['GET', 'POST'])
@login_required
def regist():
    form = RegistForm()
    if request.method == 'GET':
        return render_template('regist.html', form=form)
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if form.validate_on_submit() and not user:
            user = User(name=form.name.data, email=form.email.data, authentication=False)
            user.set_passwd(form.passwd.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            next = request.args.get('next') or url_for('index')
            flash('请查收您的注册邮件以激活账号')
            return redirect(next)
        else:
            if user:
                flash('当前邮箱已注册，请直接登录')
                return redirect('login')
            else:
                flash('请检查输入重试')
                return render_template('regist.html', form=form)


@app.route('/user/<id>')
@login_required
def user_info():
    book_can = current_user.book_can.limit(20)
    return render_template('home.html',
                            book_can = book_can)


@app.route('/board/<page>', methods=['GET', 'POST'])
def msg_board(page=1):
    msg_board = MessageBoard.query.paginate(int(page), ITEM_NUM_PER_PAGE, False)
    if request.method == 'GET':
        return render_template('message_board.html',
                                msg_board = msg_board)
    if request.method == 'POST':
        form = MeaageForm()
        if form.validate_on_submit():
            msg = MessageBoard(content=form.content.data, time=datetime.now())
            return jsonify(code=200)
        else:
            return jsonify(code=301)


@app.route('/search', methods=['GET', 'POST'])
def search():
    pass

