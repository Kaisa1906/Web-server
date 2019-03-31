from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired


class AddAnnouncementsForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Text', validators=[DataRequired()])
    category = SelectField('Category', choices=[("Cars", "Cars"), ("Clothes", "Clothes"), ("Gadgets", "Gadgets"), ("Handmade", "Handmade"), ("Pets", "Pets")], validators=[DataRequired()])
    cost = StringField('Cost', validators=[DataRequired()])
    submit = SubmitField('Add')
