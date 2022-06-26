from flask_wtf import FlaskForm
from wtforms import BooleanField, FieldList, SubmitField,  StringField
from wtforms.validators import DataRequired, ValidationError


class AtLeast:
    def __init__(self, min_=2, message=None):
        if not message:
            message = 'There should be at least 2 valid options'
        self.message = message
        self.min = min_

    def __call__(self, form, field):
        options = map(lambda x: x.data, field.entries)
        options = list(filter(lambda x: x.strip(), options))

        if len(options) < self.min:
            raise ValidationError(self.message)


class CreatePollForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    answer_options = FieldList(StringField(''), min_entries=2, label='Answer options', validators=[AtLeast()])
    multiple_choices = BooleanField('Multiple choices')
    submit = SubmitField('Create poll')
