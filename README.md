# Wfhome

**Wfhome** is a web-based work-from-home management system built with Flask. The platform allows users to create and manage tasks, track progress, and maintain personal profiles within an organization. It supports multiple user roles, authentication, and task submission with a focus on managing individual and group workflows.

## Features

- User registration and login system
- Profile management with editable fields such as name, department, etc.
- Task creation and assignment
- Dashboard for tracking tasks and progress
- User authentication and session management with Flask-Login
- Responsive design using HTML and CSS
- Blueprint structure for scalability
- Database management with Flask-SQLAlchemy and Alembic for migrations

## Technologies Used

- **Flask**: A lightweight Python web framework
- **Flask-SQLAlchemy**: ORM for handling database interactions
- **Flask-Login**: For user session management
- **Flask-Migrate**: For handling database migrations
- **SQLite**: Lightweight database for development
- **HTML/CSS**: For frontend structure and styling
- **JavaScript**: For interactive elements
- **Git/GitHub**: Version control and project hosting

## Project Structure

```plaintext
wfhome/
│
├── auth/
│   ├── __init__.py
│   ├── forms.py
│   ├── routes.py
│
├── tasks/
│   ├── __init__.py
│   ├── forms.py
│   ├── routes.py
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── profile.html
│   ├── register.html
│   ├── settings.html
│
├── __pycache__/
├── instance/
├── migrations/
├── venv/
├── app.py
├── config.py
├── models.py
├── run.py
├── requirements.txt
└── README.md
```
Installation

Local Development Installation

To get started with Wfhome locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/wfhome.git
cd wfhome
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
# or
venv\Scripts\activate     # For Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. Run the application:
```bash
flask run
```

6. Open your browser and visit http://127.0.0.1:5000/ to access the application.



Docker Installation

To run Wfhome using Docker, follow these steps:

1. Install Docker if you haven't already.


2. Clone the repository:
```bash
git clone https://github.com/yourusername/wfhome.git
cd wfhome
```

3. Build the Docker image:
```bash
docker build -t wfhome:latest .
```

4. Run the Docker container:
```bash
docker run -d -p 5000:5000 wfhome:latest
```

5. Open your browser and visit http://localhost:5000/ to access the application.



Deployment to Web Hosting Services

Heroku

1. Install the Heroku CLI and log in:

heroku login


2. Create a new Heroku application:

heroku create wfhome-app


3. Add a Procfile in the root directory with the following content:
```bash
web: flask run --host=0.0.0.0 --port=$PORT
```

4. Add your code to the Heroku repository and push to deploy:
```bash
git add .
git commit -m "Initial commit"
git push heroku master
```

5. Open your application in the browser:

heroku open



Render

1. Create a free account on Render.


2. Follow the instructions to create a new Flask web service and connect your GitHub repository.


3. Render will automatically detect your Flask app and deploy it.


4. After deployment, Render will provide a URL where you can access your application.



DigitalOcean

1. Create a DigitalOcean Droplet and install Docker.


2. SSH into your Droplet:

ssh root@your_droplet_ip


3. Install Docker and Docker Compose on the server:

apt update
apt install docker docker-compose


4. Clone your repository to the server:
```bash
git clone https://github.com/yourusername/wfhome.git
cd wfhome
```

5. Build and run the Docker image:
```bash
docker-compose up -d
```

6. Open your browser and navigate to the IP address of your Droplet to access Wfhome.



Usage

1. Registration and Login: Register for a new account, then log in to access your dashboard.


2. Profile Management: Update your profile details like name and department after logging in.


3. Task Management: Create and manage tasks, assign them to yourself or a group, and track their progress on the dashboard.



Contributing

Contributions are welcome! If you'd like to contribute to Wfhome, please follow these steps:

1. Fork the repository


2. Create a new branch (git checkout -b feature-branch)


3. Make your changes


4. Commit the changes (git commit -m 'Add new feature')


5. Push to the branch (git push origin feature-branch)


6. Open a Pull Request



License

This project is licensed under the MIT License.


---

Wfhome © 2024 by Preforio ltd. All rights reserved.

Make sure to add Docker-related files, such as a `Dockerfile` and optionally a `docker-compose.yml`, to your project if you plan on using Docker for deployment. Also, replace `yourusername` and `wfhome-app` with your actual GitHub username and desired application names.
