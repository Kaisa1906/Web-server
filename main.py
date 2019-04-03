from add_announcement import AddAnnouncementsForm
from db import DB
from flask import Flask, redirect, render_template, session, request
from login_form import LoginForm
from announcements_model import AnnouncementsModel
from users_model import UsersModel
from message_model import MessageModel
from message_form import MessagesForm
from announcements_view import ChooseCategory
from registration_form import RegistrationForm
import os
from hashlib import md5
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yula'
db = DB()
AnnouncementsModel(db.get_connection()).init_table()
UsersModel(db.get_connection()).init_table()
MessageModel(db.get_connection()).init_table()
try:
    count_img = AnnouncementsModel(db.get_connection()).get_all()[-1][0] # catch last img number
except:
    count_img = 0
count_img += 1

@app.route('/login', methods=['GET', 'POST'])
@app.route('/login/<error>', methods=['GET', 'POST'])
def login(error=None): # Now there are User1, User2, User3 with the same passwords
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        exists = user_model.exists(user_name, str(md5(bytes(password,
                                                            encoding='utf-8')).hexdigest()))  # encoding
        if exists[0]:
            session['username'] = user_name
            session['user_id'] = exists[1]
        else:
            return redirect(
                '/login/notexist')
        return redirect("/index")
    return render_template('login.html', title='Login', form=form,
                           error=error)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    return redirect('/login')


@app.route('/registration', methods=["GET", "POST"])
@app.route('/registration/<er>', methods=["GET", "POST"])
def registration(er=None):
    form = RegistrationForm()
    if form.validate_on_submit():
        users = UsersModel(db.get_connection())
        users.insert(form.username.data, str(md5(bytes(form.password.data,
                                                       encoding='utf-8')).hexdigest())) #add new user
        return redirect('/login')
    return render_template('registration.html', form=form, error=er)


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    announcements = AnnouncementsModel(db.get_connection()).get_all() #catch all announcements from db
    announcements.reverse()
    return render_template('index.html', username=session['username'], announcements=announcements)


@app.route('/add_announcements', methods=['GET', 'POST'])
def add_news():
    global count_img
    if 'username' not in session:
        return redirect('/login')
    form = AddAnnouncementsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        category = form.category.data
        cost = form.cost.data
        nm = AnnouncementsModel(db.get_connection())
        request.files["file"].save("static/img/{}.jpg".format(count_img)) # add new img with name (last number + 1)
        nm.insert(title, cost, content, category, session['user_id'], count_img) # add new announcement in db
        count_img += 1
        return redirect("/index")
    return render_template('add_announcement.html', title='Add a listing', form=form, username=session['username'])


@app.route('/delete_announcements/<int:announcements_id>', methods=['GET'])
def delete_news(announcements_id):
    if 'username' not in session:
        return redirect('/login')
    am = AnnouncementsModel(db.get_connection())
    am.delete(announcements_id) #delete announcemen from db
    return redirect("/my_announcements")


@app.route('/my_announcements')
def my_announcements():
    if 'username' not in session:
        return redirect('/login')
    announcements = AnnouncementsModel(db.get_connection()).get_all(session['user_id']) # catch all user_in_session's announcements
    announcements.reverse()
    return render_template('my_announcements.html', username=session['username'], announcements=announcements)


@app.route('/send_message/<int:user_id>', methods=["GET", "POST"])
def send_message(user_id):
    mm = MessageModel(db.get_connection())
    form = MessagesForm()
    if form.validate_on_submit():
        message = form.content.data
        mm.send(session['user_id'], user_id, message)
        return redirect('/messages')
    return render_template('send_message.html', form=form)


@app.route('/messages')
def get_messages():
    mm = MessageModel(db.get_connection())
    um = UsersModel(db.get_connection())
    user_in_session_name = session['user_id']
    messages = mm.get_all(user_in_session_name)
    news_messages_list = []
    dialog_with = []
    for message in messages: # add users, with whom there is a dialog
        if message[1] != user_in_session_name:
            if message[1] not in dialog_with:
                dialog_with.append(message[1])
        else:
            if message[2] not in dialog_with:
                dialog_with.append(message[2])
    dialog_with.reverse() # list of users, who send  a message to user_in_session
    for name in dialog_with:
        last_message = mm.get_all_between_pair(user_in_session_name, name)[-1][-1] # catch last message from dialog
        dialog_name = um.get(name)
        news_messages_list.append((dialog_name, last_message))
    return render_template('messages_page.html', messages=news_messages_list)


@app.route('/dialog/<int:user_id>', methods=["GET", "POST"])
def dialog(user_id):
    mm = MessageModel(db.get_connection())
    um = UsersModel(db.get_connection())
    user_in_session_name = session['user_id']
    all_messages = []
    messages = mm.get_all_between_pair(user_in_session_name, user_id)
    for message in messages:
        all_messages.append((um.get(message[1])[1], message[-1])) # catch message with sender's name
    all_messages.reverse()
    return render_template('dialog_page.html', messages=all_messages, user_id=user_id)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.2', debug=True)
