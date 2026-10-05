from flask import Flask, render_template
from flask_jwt_extended import JWTManager

from config import Config
from models import db, Student, Course, Grade
from auth import register_auth_routes, create_demo_users
from routes.students import register_student_routes
from routes.courses import register_course_routes
from routes.grades import register_grade_routes
from routes.api import register_api_routes
from routes.analytics_routes import register_analytics_routes


app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

register_auth_routes(app)
register_student_routes(app)
register_course_routes(app)
register_grade_routes(app)
register_api_routes(app)
register_analytics_routes(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


def create_sample_data():
    if Student.query.count() == 0:
        students = [
            Student(name="Alice", email="alice@example.com"),
            Student(name="Bob", email="bob@example.com"),
            Student(name="Charlie", email="charlie@example.com")
        ]

        db.session.add_all(students)
        db.session.commit()

    if Course.query.count() == 0:
        courses = [
            Course(name="Python", code="PY101"),
            Course(name="Database", code="DB101"),
            Course(name="Web Development", code="WEB101")
        ]

        db.session.add_all(courses)
        db.session.commit()

    if Grade.query.count() == 0:
        alice = Student.query.filter_by(email="alice@example.com").first()
        bob = Student.query.filter_by(email="bob@example.com").first()
        charlie = Student.query.filter_by(email="charlie@example.com").first()

        python = Course.query.filter_by(code="PY101").first()
        database = Course.query.filter_by(code="DB101").first()
        web = Course.query.filter_by(code="WEB101").first()

        grades = [
            Grade(student_id=alice.id, course_id=python.id, score=90),
            Grade(student_id=alice.id, course_id=database.id, score=85),
            Grade(student_id=bob.id, course_id=python.id, score=78),
            Grade(student_id=bob.id, course_id=web.id, score=88),
            Grade(student_id=charlie.id, course_id=database.id, score=72),
            Grade(student_id=charlie.id, course_id=web.id, score=80)
        ]

        db.session.add_all(grades)
        db.session.commit()


with app.app_context():
    db.create_all()
    create_demo_users()
    create_sample_data()


if __name__ == "__main__":
    app.run(debug=True)
