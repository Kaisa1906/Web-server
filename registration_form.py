from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"id": "login",
                                      "class": "form-control"})  # if there is no data it wouldn't be sent
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"id": "password",
                                        "class": "form-control"})  # if there is no data it wouldn't be sent
    submit = SubmitField('Register')
