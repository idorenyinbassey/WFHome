from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import TaskForm  # Assuming the form is in the forms.py
from models import Task  # Assuming Task is your Task model
from . import tasks
from app import db

@tasks.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # Retrieve tasks for the current user
    user_tasks = Task.query.filter_by(user_id=current_user.id).all()
    form = TaskForm()  # Task creation form

    # Check if the form is submitted and valid
    if form.validate_on_submit():
        # Create a new task using form data
        task = Task(
            title=form.task_title.data,
            description=form.task_description.data,
            user_id=current_user.id  # Assuming Task has a user_id field
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.dashboard'))

    # Render the dashboard with tasks and form
    return render_template('dashboard.html', form=form, tasks=user_tasks, user=current_user)