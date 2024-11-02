from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, DateTimeLocalField, SubmitField
from wtforms.validators import DataRequired, Optional, ValidationError
from datetime import datetime

class TaskForm(FlaskForm):
    task_title = StringField('Task Title', validators=[DataRequired()])
    task_description = TextAreaField('Task Description', validators=[Optional()])
    task_type = SelectField('Task Type', choices=[('individual', 'Individual'), ('group', 'Group')], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], validators=[DataRequired()])
    due_date = DateField('Due Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[Optional()])
    start_time = DateTimeLocalField('Start Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    end_time = DateTimeLocalField('End Time (YYYY-MM-DD HH:MM)', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    assignee = SelectField('Assignee (optional)', coerce=int, validators=[Optional()])
    submit = SubmitField('Create Task')

    def validate_due_date(form, field):
        if field.data and field.data < datetime.today().date():
            raise ValidationError('Due date cannot be in the past.')

    def validate_start_time(form, field):
        if field.data and field.data < datetime.now():
            raise ValidationError('Start time cannot be in the past.')

    def validate_end_time(form, field):
        if field.data and field.data < datetime.now():
            raise ValidationError('End time cannot be in the past.')
        if form.start_time.data and field.data and field.data < form.start_time.data:
            raise ValidationError('End time cannot be before start time.')