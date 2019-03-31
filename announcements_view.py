from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired


class ChooseCategory(FlaskForm):
    category = SelectField('Category', choices=[(None, 'All'),("Cars", "Cars"), ("Clothes", "Clothes"), ("Gadgets", "Gadgets"), ("Handmade", "Handmade"), ("Pets", "Pets")], validators=[DataRequired()])
    submit = SubmitField('Choose')