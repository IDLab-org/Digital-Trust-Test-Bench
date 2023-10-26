from flask_wtf import FlaskForm
from wtforms.widgets import CheckboxInput, ListWidget
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
)
from wtforms.validators import DataRequired, Length

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class VCFormatValidatorV1(FlaskForm):
    vc_text = TextAreaField("Verifiable Credential", validators=[DataRequired()])
    # features = MultiCheckboxField("Supported features", validators=[])
    proof_type = SelectField("Proof Type", validators=[DataRequired()])
    vc_file = FileField('File')
    submit = SubmitField("Submit")

class VCProfilerV1(FlaskForm):
    vc = TextAreaField("Verifiable Credential", validators=[DataRequired()])
    submit = SubmitField("Submit")
