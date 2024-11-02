import pytest
from app import create_app, db
from config import TestingConfig  # Import the actual class, not a string
from models import Task, User

@pytest.fixture
def app():
    app = create_app(TestingConfig)  # Pass the class directly
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_task_creation_and_notification(client):
    # Create a test user and log in
    test_user = User(username='testuser', email='test@example.com')
    test_user.set_password('password123')
    db.session.add(test_user)
    db.session.commit()

    client.post('/login', data={
        'username': 'testuser',
        'password': 'password123'
    })

    # Test task creation
    response = client.post('/dashboard', data={
        'task_title': 'Test Task',
        'task_description': 'This is a test task.',
        'task_type': 'individual',
        'priority': 'high',
        'due_date': '2024-11-10'
    })

    # Check if the response indicates a successful redirect
    assert response.status_code == 302  # Redirect after task creation

    # Follow the redirect to get the final response
    response = client.get(response.location)

    # Print out the response data for debugging
    print(response.data.decode('utf-8'))  # Decode bytes to string for better readability

    # Assert that the task creation success message is in the final response
    assert b'Task created successfully!' in response.data  # Check if success message appears