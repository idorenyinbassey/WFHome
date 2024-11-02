from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from .forms import TaskForm
from models import Task, User
from . import tasks
from app import db
from datetime import datetime

@tasks.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    """Display the dashboard and handle task creation."""
    # Retrieve tasks for the current user (created by or assigned to)
    user_tasks = Task.query.filter(
        (Task.user_id == current_user.id) | (Task.assignee_id == current_user.id)
    ).all()

    form = TaskForm()  # Task creation form
    # Populate assignee choices with user IDs and usernames
    form.assignee.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        # Validation for date/time fields
        if form.due_date.data and form.due_date.data < datetime.today().date():
            flash('Due date cannot be in the past.', 'danger')
            return render_template('dashboard.html', form=form, tasks=user_tasks, user=current_user)

        if form.start_time.data and form.start_time.data < datetime.now():
            flash('Start time cannot be in the past.', 'danger')
            return render_template('dashboard.html', form=form, tasks=user_tasks, user=current_user)

        if form.end_time.data and form.end_time.data < datetime.now():
            flash('End time cannot be in the past.', 'danger')
            return render_template('dashboard.html', form=form, tasks=user_tasks, user=current_user)

        if form.start_time.data and form.end_time.data and form.end_time.data < form.start_time.data:
            flash('End time cannot be before start time.', 'danger')
            return render_template('dashboard.html', form=form, tasks=user_tasks, user=current_user)

        # Create a new task using form data
        task = Task(
            title=form.task_title.data,
            description=form.task_description.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,  # Use form data directly if available
            task_type=form.task_type.data,
            user_id=current_user.id,  # Set the current user as the creator
            assignee_id=form.assignee.data  # Assign task to the selected user
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('tasks.dashboard'))  # Redirect to the dashboard after creation

    # Render the dashboard with tasks and form
    return render_template('dashboard.html', form=form, tasks=user_tasks, user=current_user)

@tasks.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    """Edit an existing task."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and task.assignee_id != current_user.id:
        abort(403)  # Forbidden if the user is not the creator or assignee

    form = TaskForm(obj=task)
    form.assignee.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        task.title = form.task_title.data
        task.description = form.task_description.data
        task.priority = form.priority.data
        task.due_date = form.due_date.data
        task.start_time = form.start_time.data
        task.end_time = form.end_time.data
        task.task_type = form.task_type.data
        task.assignee_id = form.assignee.data
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('edit_task.html', form=form, task=task)

@tasks.route('/task/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """Delete an existing task."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and task.assignee_id != current_user.id:
        abort(403)  # Forbidden if the user is not the creator or assignee

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('tasks.dashboard'))

@tasks.route('/task/start/<int:task_id>', methods=['POST'])
@login_required
def start_task(task_id):
    """Start a task and record the start time."""
    task = Task.query.get_or_404(task_id)
    # Ensure only the assigned user or creator can start the task
    if task.assignee_id != current_user.id and task.user_id != current_user.id:
        flash('You do not have permission to start this task.', 'danger')
        return redirect(url_for('tasks.dashboard'))

    if not task.start_time:
        task.start_time = datetime.utcnow()  # Set the start time
        db.session.commit()
        flash('Task started.', 'success')
    else:
        flash('Task has already been started.', 'warning')
    return redirect(url_for('tasks.dashboard'))

@tasks.route('/task/complete/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    """Complete a task and record the end time."""
    task = Task.query.get_or_404(task_id)
    # Ensure only the assigned user or creator can complete the task
    if task.assignee_id != current_user.id and task.user_id != current_user.id:
        flash('You do not have permission to complete this task.', 'danger')
        return redirect(url_for('tasks.dashboard'))

    if not task.end_time:
        task.end_time = datetime.utcnow()  # Set the end time
        if hasattr(task, 'calculate_duration'):  # Ensure the method exists
            task.duration = task.calculate_duration()  # Calculate the duration
        db.session.commit()
        flash('Task completed.', 'success')
    else:
        flash('Task has already been completed.', 'warning')
    return redirect(url_for('tasks.dashboard'))

@tasks.route('/end_task/<int:task_id>', methods=['POST'])
@login_required
def end_task(task_id):
    """Mark a task as completed and set the end time."""
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id and task.assignee_id != current_user.id:
        abort(403)  # Forbidden if not the owner or assignee of the task

    if not task.end_time:
        task.end_time = datetime.utcnow()  # Set the end time to the current UTC time
        db.session.commit()
        flash('Task marked as completed!', 'success')
    else:
        flash('Task has already been completed.', 'warning')

    return redirect(url_for('tasks.dashboard'))