from flask import Flask, render_template, redirect, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

from Forms import LoginForm, SetAvatar, PostMessage

import time
# from DataBases import RegisteredUsers

app = Flask(__name__)
app.config['SECRET_KEY'] = "MySecretKey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)




# databases registration (python / from web_app import db / db.create_all() / exit() )

class RegisteredUsers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registered_username = db.Column(db.String(20), nullable=False, unique=True)
    registered_password = db.Column(db.String(30), nullable=False)
    profile_image = db.Column(db.String(500), default="data:image/jpeg;base64,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")
    profile_background = db.Column(db.String(500), default="https://i.pinimg.com/originals/06/a8/5b/06a85b703ccc50fcc2214bac56214f48.gif")

    def __repr__(self):
        return '<RegisteredUsers %r>' % self.registered_username

class MessageDatabase(db.Model):
    chat_id = db.Column(db.Integer, primary_key=True)
    message_content = db.Column(db.String(500), nullable=False)
    sender = db.Column(db.String(20), nullable=False)
    reciever = db.Column(db.String(20), nullable=False)
    send_time = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return str("| " + self.sender + " : "  + self.reciever + " : " + self.message_content + " : " + str(self.send_time) + " |")


class ProfilePagePosts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    profile_username = db.Column(db.String(20), nullable=False)
    text_content = db.Column(db.String(500), nullable=False)
    link_content = db.Column(db.String(500), nullable=True)
    post_time = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return str("| " + self.profile_username + " : "  + self.text_content + " : " + self.link_content + " : " + str(self.post_time) + " |")



def GetProfilePostsFunc(username):
    all_posts = ProfilePagePosts.query.all()

    posts_list = {'main' : []}
    
    for post in reversed(all_posts):
        if (post.profile_username == username):
            txt = post.text_content
            img_link = post.link_content
            posts_list['main'].append({'text' : txt, 'img' : img_link})

    return posts_list


# routes & methods
@app.route('/', methods=["GET"])
def index_page():
    return redirect(url_for('profile_page'))

@app.route('/login', methods=["GET", "POST"])
def login_page():

    form = LoginForm()

    new_user = RegisteredUsers()

    invalid = "Invalid username or password."

    if form.validate_on_submit():

        if form.enter.data:

            try:
                users_base = RegisteredUsers.query.all()

                entered_login = form.username.data
                entered_password = form.password.data

                user_id = 1
                for user_info in users_base:
                    if (entered_login == user_info.registered_username):
                        if (entered_password == user_info.registered_password):
                            session['user_info'] = {'user_id' : user_id, 'username' : RegisteredUsers.query.get(user_id).registered_username, 'password' : RegisteredUsers.query.get(user_id).registered_password} 
                            return redirect(url_for('profile_page'))
                    user_id = user_id + 1

                return render_template('login_page.html', form=form, invalid=invalid)

            except:        

                return render_template('login_page.html', form=form, invalid=invalid)


            # print(len(users_base))
            # print(RegisteredUsers.query.get(1).registered_username)


        elif form.register.data:

            users_base = RegisteredUsers.query.all()


            entered_login = form.username.data
            entered_password = form.password.data
            
            # restricted_elements = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "&", "#", ";", " ", ".", "*", "+", "?", "^", "$", "{", "}", ]
            restricted_elements = "1234567890&#; .*+?^${}()|[\]"
            for symbol in entered_login:
                if (symbol in restricted_elements):
                    if (symbol == " "):
                        return render_template('login_page.html', form=form, invalid="Can't use this character in login: space")

                    return render_template('login_page.html', form=form, invalid="Can't use this character in login: " + str(symbol))


            user_id = 1
            for user_info in users_base:
                if (entered_login == user_info.registered_username):
                    return render_template('login_page.html', form=form, invalid="Username already exists.")
                user_id = user_id + 1


            new_user.registered_username = form.username.data
            new_user.registered_password = form.password.data


            try:

                db.session.add(new_user)
                db.session.commit()

                session['user_info'] = {'user_id' : user_id, 'username' : RegisteredUsers.query.get(user_id).registered_username, 'password' : RegisteredUsers.query.get(user_id).registered_password}

                return redirect(url_for('profile_page'))

            except:

                db.session.rollback() #откат бд

                return render_template('login_page.html', form=form, invalid="Database error. Try again.")

    return render_template('login_page.html', form=form, invalid="")



@app.route('/me')
def profile_page():
    if 'user_info' in session:
        user = session['user_info']

        posts = GetProfilePostsFunc(session['user_info']['username'])

        return render_template('profile_page.html', user=user, avatar=RegisteredUsers.query.get(session['user_info']['user_id']).profile_image, ismypage=True, bottom_avatar=RegisteredUsers.query.get(session['user_info']['user_id']).profile_image, my_user=user, background_data=RegisteredUsers.query.get(session['user_info']['user_id']).profile_background, posts=posts)
    else:
        return redirect(url_for('login_page'))





@app.route('/community')
def community():
    if 'user_info' not in session:
        return redirect(url_for('login_page'))

    user = session['user_info']
    all_users = RegisteredUsers.query.all()
    users_js = []
    users_img = []
    for usr in all_users:
        users_js.append(usr.registered_username)
    return render_template('community.html', background_data=RegisteredUsers.query.get(session['user_info']['user_id']).profile_background, all_users=all_users, users_js=users_js)






@app.route('/settings', methods=["POST", "GET"])
def settings():

    form = SetAvatar()

    invalid = ""

    if 'user_info' in session:
        user = session['user_info']

        if form.validate_on_submit():

            users_base = RegisteredUsers.query.all()

            for cur_user in users_base:
                print(cur_user.id)
                if (user['user_id'] == cur_user.id):
                    if (form.avatar_link.data != ""):
                        cur_user.profile_image = form.avatar_link.data
                    if (form.background_link.data != ""):
                        cur_user.profile_background = form.background_link.data

                    print(form.avatar_link.data)

                    db.session.commit()


                    return redirect(url_for('profile_page'))
            
            invalid = "Something went wrong..."
            return render_template('url_avatar_page.html', user=user, form=form, invalid=invalid)


        return render_template('url_avatar_page.html', user=user, form=form, background_data=RegisteredUsers.query.get(session['user_info']['user_id']).profile_background)
    else:
        return redirect(url_for('login_page'))


@app.route('/user/<username_param>')
def user_profile(username_param):
    
    users_base = RegisteredUsers.query.all()
    print(users_base)

    for user_info in users_base:
        if (username_param == user_info.registered_username):

            if 'user_info' in session:
                if (session['user_info']['username'] == username_param):
                    return redirect(url_for('profile_page'))

                me_user_obj = session['user_info']
                me_avatar = RegisteredUsers.query.get(session['user_info']['user_id']).profile_image

            else:

                me_user_obj = {'username' : 'Log In'}
                me_avatar = '/static/css/img/user.png'          

            user_obj = {'username' : user_info.registered_username}


            posts = GetProfilePostsFunc(username_param)

            return render_template('profile_page.html', user=user_obj, avatar=user_info.profile_image, ismypage=False, bottom_avatar=me_avatar, my_user=me_user_obj, background_data=user_info.profile_background, posts=posts) 
    
    return "404 USER NOT FOUND FOR URL /user/"
    


@app.route('/messages')
def messages():
    # max 48 symbols
    # messages_list
    if 'user_info' not in session:
        return redirect(url_for('login_page'))

    me_user = session['user_info']

    messages_info = []

    msg_db = MessageDatabase.query.all()

    users_base = RegisteredUsers.query.all()

    showed_users = []

    for message in reversed(msg_db):
        if (message.sender == session['user_info']['username'] and message.reciever not in showed_users):

            showed_users.append(message.reciever)

            for user in users_base:
                if (message.reciever == user.registered_username):

                    messages_info.append({'username' : user.registered_username, 'user_avatar' : user.profile_image, 'msg_content' : message.message_content, 'reciever' : 'not_me', 'dialogue_url' : '/user/' + message.reciever + '/dialogue'})
            

        elif (message.reciever == session['user_info']['username'] and message.sender not in showed_users):

            showed_users.append(message.sender)

            for user in users_base:
                if (message.sender == user.registered_username):

                    messages_info.append({'username' : user.registered_username, 'user_avatar' : user.profile_image, 'msg_content' : message.message_content, 'reciever' : 'me', 'dialogue_url' : '/user/' + message.sender + '/dialogue'})
        


        
    return render_template('messages.html', messages_list=messages_info, background_data=RegisteredUsers.query.get(session['user_info']['user_id']).profile_background)








@app.route('/get_msg_db')
def get_msg_db():
    if 'user_info' not in session:
        return redirect(url_for('login_page'))

    me_user = session['user_info']

    messages_info = {"main" : []}

    msg_db = MessageDatabase.query.all()

    users_base = RegisteredUsers.query.all()

    showed_users = []

    for message in reversed(msg_db):
        if (message.sender == session['user_info']['username'] and message.reciever not in showed_users):

            showed_users.append(message.reciever)

            for user in users_base:
                if (message.reciever == user.registered_username):

                    messages_info["main"].append({'username' : user.registered_username, 'msg_content' : message.message_content, 'reciever' : 'not_me', 'dialogue_url' : '/user/' + message.reciever + '/dialogue', 'user_avatar' : user.profile_image,})
            
    # 'user_avatar' : user.profile_image,
        elif (message.reciever == session['user_info']['username'] and message.sender not in showed_users):

            showed_users.append(message.sender)

            for user in users_base:
                if (message.sender == user.registered_username):

                    messages_info["main"].append({'username' : user.registered_username, 'msg_content' : message.message_content, 'reciever' : 'me', 'dialogue_url' : '/user/' + message.sender + '/dialogue', 'user_avatar' : user.profile_image,})
        
    return messages_info





@app.route('/user/<username_param>/dialogue/msg_db_info', methods=["POST", "GET"])
def dialogue_db(username_param):
    if 'user_info' not in session:

        return redirect(url_for('login_page'))

    me_user = session['user_info']

    users_base = RegisteredUsers.query.all()

    for user_info in users_base:
        if (username_param == user_info.registered_username):

            print("Session exist, starting /dialogue;")
            
            messages_for_this_dialogue = {"main" : []}

            msg_db = MessageDatabase.query.all()

            # print(msg_db)

            for message in msg_db:
                if (message.sender == session['user_info']['username']):
                    if (message.reciever == username_param):

                        messages_for_this_dialogue["main"].append({'msg_reciever' : "not_me", 'content' : message.message_content, 'time' : message.send_time})
                
                elif (message.sender == username_param):
                    if (message.reciever == session['user_info']['username']):

                        messages_for_this_dialogue["main"].append({'msg_reciever' : "me", 'content' : message.message_content, 'time' : message.send_time})

            users_base = RegisteredUsers.query.all()

            for user in users_base:
                if (username_param == user.registered_username):
                    return messages_for_this_dialogue

            return "Dialogue error."






@app.route('/msg_db_info_post', methods=["POST"])
def get_sended_info():
    if 'user_info' not in session:

        return redirect(url_for('login_page'))

    jsdata = request.get_json()

    print("New message sended: " + str(jsdata))

    
    msg_db_new_entry = MessageDatabase()

    msg_db_new_entry.message_content = jsdata['message_content']
    msg_db_new_entry.reciever = jsdata['reciever']
    msg_db_new_entry.sender = jsdata['sender']
    msg_db_new_entry.send_time = jsdata['send_time']

    db.session.add(msg_db_new_entry)
    db.session.commit()
    print("Message added to database.")

    return jsdata






@app.route("/post_new", methods=["POST"])
def post_new():
    if 'user_info' not in session:

        return redirect(url_for('login_page'))

    jsdata = request.get_json()

    print("New post added: " + str(jsdata))

    
    post_base_ref = ProfilePagePosts()

    post_base_ref.profile_username = jsdata['username']
    post_base_ref.text_content = jsdata['post_text']
    post_base_ref.link_content = jsdata['post_img_link']
    post_base_ref.post_time = jsdata['time']

    db.session.add(post_base_ref)
    db.session.commit()
    print("Message added to database.")

    return jsdata


@app.route('/user/<username_param>/dialogue', methods=["POST", "GET"])
def dialogue(username_param):
    if 'user_info' not in session:

        return redirect(url_for('login_page'))


    me_user = session['user_info']

    users_base = RegisteredUsers.query.all()

    for user_info in users_base:
        if (username_param == user_info.registered_username):
            
            messages_for_this_dialogue = []

            msg_db = MessageDatabase.query.all()

            # print(msg_db)

            for message in msg_db:
                if (message.sender == session['user_info']['username']):
                    if (message.reciever == username_param):

                        messages_for_this_dialogue.append({'msg_sender' : message.sender, 'msg_reciever' : message.reciever, 'content' : message.message_content, 'time' : message.send_time})
                
                elif (message.sender == username_param):
                    if (message.reciever == session['user_info']['username']):

                        messages_for_this_dialogue.append({'msg_sender' : message.sender, 'msg_reciever' : message.reciever, 'content' : message.message_content, 'time' : message.send_time})

            print(messages_for_this_dialogue)
            print(len(messages_for_this_dialogue))


            users_base = RegisteredUsers.query.all()

            for user in users_base:
                if (username_param == user.registered_username):
                    return render_template('dialogue.html', enemy=user, messages=messages_for_this_dialogue, background_data=RegisteredUsers.query.get(session['user_info']['user_id']).profile_background, user=me_user)

            return "Dialogue error."


            




    return "404 USER NOT FOUND FOR URL /user/"


# run app

if (__name__ == "__main__"):
    app.run(debug=True)