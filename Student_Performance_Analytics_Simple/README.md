# Student Performance Analytics System

This project is a beginner-friendly full-stack Flask application for managing student performance. It uses Flask for the web application, MySQL with SQLAlchemy for permanent data storage, Jinja2 for HTML templates, CSS and JavaScript for the frontend, JWT for authentication, and Pandas and NumPy for analytics.

## Features

- User login with admin and student roles
- JWT authentication
- Student CRUD operations
- Course CRUD operations
- Grade CRUD operations
- Student-only data access
- REST API
- Pandas and NumPy analytics
- Mean, median and standard deviation
- Course average and ranking
- Course and student filters
- CSV upload
- CSV and Excel reports
- Jinja2 templates
- Separate static CSS and JavaScript files

## Installation

Open the project folder in VS Code terminal.

Create virtual environment:

python -m venv venv

Activate:

venv\Scripts\activate

Install packages:

pip install -r requirements.txt

## MySQL

Open MySQL Workbench and create:

CREATE DATABASE student_performance_db;

The current database setting is:

mysql+pymysql://root:root@localhost/student_performance_db

If your MySQL password is different, edit config.py.

## Run

python app.py

Open:

http://127.0.0.1:5000

## Login

Admin:

Email: admin@example.com
Password: admin123

Student:

Email: alice@example.com
Password: student123

## Main Routes

/                 Home
/login             Login
/dashboard         Dashboard
/students          Students
/courses           Courses
/grades            Grades
/analytics         Analytics

## API

POST /api/login

GET /api/students
POST /api/students
GET /api/students/<id>
PUT /api/students/<id>
PATCH /api/students/<id>
DELETE /api/students/<id>

GET /api/courses
POST /api/courses

GET /api/grades
POST /api/grades
GET /api/grades/<id>
PUT /api/grades/<id>
PATCH /api/grades/<id>
DELETE /api/grades/<id>

## CSV Format

student_email,course_code,score

alice@example.com,PY101,90
alice@example.com,DB101,85
bob@example.com,PY101,78

## Project Structure

app.py contains the main Flask application.

config.py contains configuration.

models.py contains database models.

auth.py contains login and authentication functions.

analytics.py contains Pandas and NumPy calculations.

routes/ contains student, course, grade, API and analytics routes.

templates/ contains Jinja2 HTML files.

static/ contains CSS and JavaScript files.
