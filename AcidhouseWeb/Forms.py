from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Login', render_kw={"placeholder": "Username"}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Password"}, validators=[DataRequired()])

    enter = SubmitField('Log In')
    register = SubmitField('Register')

class SetAvatar(FlaskForm):
    avatar_link = StringField('avatar_link', render_kw={"placeholder": "https://..."})
    background_link = StringField('avatar_link', render_kw={"placeholder": "https://..."})

    submit_avatar = SubmitField('SET')

class PostMessage(FlaskForm):
    msg_form_content = StringField('msg_form_content', render_kw={"placeholder": ""}, validators=[DataRequired()])

    send_msg = SubmitField('Send')