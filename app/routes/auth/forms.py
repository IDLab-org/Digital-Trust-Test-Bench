from flask_wtf import FlaskForm
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms import validators
from wtforms import (
    StringField,
    HiddenField,
    SubmitField,
    TextAreaField,
    FileField,
    SelectMultipleField,
    BooleanField,
    SelectField,
    RadioField,
    PasswordField,
    EmailField,
    )
from wtforms.validators import DataRequired, Length, InputRequired
from email_validator import validate_email, EmailNotValidError


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

# Keeping this code even if unused - in case we need basic authtntication in the future

class BasicLoginForm(FlaskForm):
    email = EmailField("Email Address", [validators.DataRequired(), validators.Email("Enter a valid email address")])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class GithubLoginForm(FlaskForm):
    submit = SubmitField("Submit")

class VCLoginForm(FlaskForm):
    submit = SubmitField("Submit")
