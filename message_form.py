from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessagesForm(FlaskForm):
    content = TextAreaField('Message text', validators=[
        DataRequired()])
    submit = SubmitField('Send')