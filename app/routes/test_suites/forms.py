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

class DataModelFormV1(FlaskForm):
    vc_text = TextAreaField("Verifiable Credential", validators=[DataRequired()])
    vc_file = FileField('File')
    # proof_type = SelectField("Proof Type", validators=[DataRequired()])
    submit = SubmitField("Submit")

class VcTestSuiteFormV1(FlaskForm):
    endpoint = StringField("VC-API Endpoint")
    implementation = SelectField("VC-API Implementation")
    token = StringField("OAuth Token (Optional)")
    features = MultiCheckboxField("Supported Features", validators=[])
    proof_type = SelectField("Proof Type", validators=[DataRequired()])
    submit = SubmitField("Submit")

class VcPlaygroundTestSuiteForm(FlaskForm):
    implementation = SelectField("VC-API Implementation", validators=[])
    endpoint = StringField("VC-API Endpoint", validators=[])
    # issuer = SelectField("Issuer", validators=[DataRequired()])
    # issuer_endpoint = StringField("Issuer Endpoint", validators=[DataRequired()])
    # verifier = SelectField("Verifier", validators=[DataRequired()])
    # verifier_endpoint = StringField("Verifier Endpoint", validators=[DataRequired()])
    submit = SubmitField("Submit")

class VCFormatValidatorV1(FlaskForm):
    vc_text = TextAreaField("Verifiable Credential", validators=[DataRequired()])
    # features = MultiCheckboxField("Supported features", validators=[])
    proof_type = SelectField("Proof Type", validators=[DataRequired()])
    vc_file = FileField('File')
    submit = SubmitField("Submit")

class VCProfilerV1(FlaskForm):
    vc = TextAreaField("Verifiable Credential", validators=[DataRequired()])
    submit = SubmitField("Submit")
