from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Optional


class JobsForm(FlaskForm):
    team_leader = SelectField('Team Leader id', coerce=int, validators=[DataRequired()])
    job = StringField('Job Title', validators=[DataRequired()])
    work_size = IntegerField('Work Size', validators=[DataRequired()])
    collaborators = StringField('Collaborators', validators=[DataRequired()])
    start_date = DateTimeField('Start Date', format="%Y-%m-%dT%H:%M", validators=[Optional()])
    end_date = DateTimeField('End Date', format="%Y-%m-%dT%H:%M", validators=[Optional()])

    is_finished = BooleanField('Is job finished?')
    submit = SubmitField('Submit')
