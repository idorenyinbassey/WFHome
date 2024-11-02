from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
import os
from .forms import RegistrationForm, LoginForm, ProfileForm
from . import auth
from models import User, db  # Correct import assuming you're using relative imports

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if the username already exists
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return render_template('register.html', form=form)
        
        # Check if the email already exists
        existing_email = User.query.filter_by(email=form.email.data).first()
        if existing_email:
            flash('An account with this email already exists. Please use a different email or login.', 'danger')
            return render_template('register.html', form=form)
        
        # Create and save the new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Use set_password to hash the password
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('tasks.dashboard'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(
            (User.email == form.login_identifier.data) |
            (User.username == form.login_identifier.data)
        ).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            
            # Check if profile is complete
            if not user.first_name or not user.last_name or not user.department or not user.phone_number:
                return redirect(url_for('auth.edit_profile'))
                
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('tasks.dashboard'))
        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)

    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.middle_name = form.middle_name.data
        current_user.last_name = form.last_name.data
        current_user.department = form.department.data
        current_user.phone_number = form.phone_number.data
        current_user.address = form.address.data

        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                current_user.profile_picture = filename

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('tasks.dashboard'))

    return render_template('profile.html', form=form, user=current_user)

@auth.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@auth.route('/update_notifications', methods=['POST'])
@login_required
def update_notifications():
    # Logic to handle updating notification preferences
    flash('Notification preferences updated!', 'success')
    return redirect(url_for('auth.settings'))

@auth.route('/update_security', methods=['POST'])
@login_required
def update_security():
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')

    if not current_user.check_password(current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('auth.settings'))

    current_user.set_password(new_password)
    db.session.commit()
    flash('Password updated successfully!', 'success')
    return redirect(url_for('auth.settings'))

@auth.route('/update_privacy', methods=['POST'])
@login_required
def update_privacy():
    profile_visibility = request.form.get('profile_visibility')
    current_user.profile_visibility = profile_visibility  # Ensure this field exists in your User model
    db.session.commit()
    flash('Privacy settings updated!', 'success')
    return redirect(url_for('auth.settings'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# New route for viewing admin-only content
@auth.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash("You do not have permission to access this page.", "danger")
        return redirect(url_for('tasks.dashboard'))
    
    return render_template('admin_dashboard.html')  # Ensure this template exists