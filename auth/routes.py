from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, ProfileForm
from . import auth
from models import User, db  # Correct import assuming you're using relative imports

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Use set_password to hash the password
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Try to find the user by email or username
        user = User.query.filter(
            (User.email == form.login_identifier.data) |
            (User.username == form.login_identifier.data)
        ).first()
        # Check if user exists and password matches (assumes password hashing)
        if user and user.check_password(form.password.data):  # Implement check_password in User model
            login_user(user)
            # Check if profile is complete
            if not user.first_name or not user.last_name or not user.department or not user.phone_number:
                return redirect(url_for('auth.edit_profile'))  # Changed 'setup_profile' to 'auth.edit_profile'
            return redirect(url_for('tasks.dashboard'))
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

        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('tasks.dashboard'))  # Redirect to dashboard view

    return render_template('profile.html', form=form, user=current_user)

@auth.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))