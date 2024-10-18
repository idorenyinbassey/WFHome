from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# User model representing a registered user in the system
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=True)  # New fields
    middle_name = db.Column(db.String(150), nullable=True)
    last_name = db.Column(db.String(150), nullable=True)
    department = db.Column(db.String(150), nullable=True, default='Unknown')  # Department dropdown
    phone_number = db.Column(db.String(15), nullable=True)  # Optional fields
    address = db.Column(db.String(250), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to set a password and hash it for security
    def set_password(self, password):
        """Hashes the password and stores it in the password_hash field."""
        self.password_hash = generate_password_hash(password)

    # Method to check if the entered password matches the stored hash
    def check_password(self, password):
        """Compares a given password with the stored password hash."""
        return check_password_hash(self.password_hash, password)

    # String representation for debugging purposes
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.first_name}', '{self.last_name}', '{self.department}', '{self.phone_number}', '{self.address}', '{self.date_created}',)"

# Task model representing tasks assigned to users
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(100), nullable=False)
    
    description = db.Column(db.Text, nullable=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    # String representation of the task object for debugging purposes
    def __repr__(self):
        return f"Task('{self.title}', 'Assigned to user_id: {self.user_id}')"