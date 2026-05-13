from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email

class DepartmentForm(FlaskForm):
    title = StringField('Title of department', validators=[DataRequired()])
    chief = SelectField('Chief', coerce=int, validators=[DataRequired()])
    members = StringField('Members', validators=[DataRequired()])
    email = StringField('Department Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')