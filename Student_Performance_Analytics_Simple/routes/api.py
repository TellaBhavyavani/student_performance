from flask import jsonify, request
from models import db, Student, Course, Grade
from auth import is_admin
from flask_jwt_extended import jwt_required


def register_api_routes(app):

    @app.route("/api/students", methods=["GET"])
    @jwt_required()
    def api_students():
        students = Student.query.all()

        data = []
        for student in students:
            data.append({
                "id": student.id,
                "name": student.name,
                "email": student.email
            })

        return jsonify({"status": "success", "data": data})

    @app.route("/api/students", methods=["POST"])
    @jwt_required()
    def api_create_student():
        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        data = request.get_json() or {}

        if not data.get("name") or not data.get("email"):
            return jsonify({
                "status": "error",
                "message": "Name and email are required"
            }), 400

        student = Student(
            name=data["name"],
            email=data["email"]
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email
            }
        }), 201

    @app.route("/api/students/<int:id>", methods=["GET"])
    @jwt_required()
    def api_get_student(id):
        student = Student.query.get_or_404(id)

        return jsonify({
            "status": "success",
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email
            }
        })

    @app.route("/api/students/<int:id>", methods=["PUT", "PATCH"])
    @jwt_required()
    def api_update_student(id):
        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        student = Student.query.get_or_404(id)
        data = request.get_json() or {}

        student.name = data.get("name", student.name)
        student.email = data.get("email", student.email)

        db.session.commit()

        return jsonify({
            "status": "success",
            "data": {
                "id": student.id,
                "name": student.name,
                "email": student.email
            }
        })

    @app.route("/api/students/<int:id>", methods=["DELETE"])
    @jwt_required()
    def api_delete_student(id):
        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        student = Student.query.get_or_404(id)
        db.session.delete(student)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Student deleted"
        })

    @app.route("/api/courses", methods=["GET", "POST"])
    @jwt_required()
    def api_courses():
        if request.method == "GET":
            courses = Course.query.all()

            data = []
            for course in courses:
                data.append({
                    "id": course.id,
                    "name": course.name,
                    "code": course.code
                })

            return jsonify({"status": "success", "data": data})

        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        data = request.get_json() or {}

        course = Course(
            name=data.get("name"),
            code=data.get("code")
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": {
                "id": course.id,
                "name": course.name,
                "code": course.code
            }
        }), 201

    @app.route("/api/grades", methods=["GET", "POST"])
    @jwt_required()
    def api_grades():
        if request.method == "GET":
            grades = Grade.query.all()

            data = []
            for grade in grades:
                data.append({
                    "id": grade.id,
                    "student_id": grade.student_id,
                    "course_id": grade.course_id,
                    "score": grade.score,
                    "date": str(grade.date)
                })

            return jsonify({"status": "success", "data": data})

        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        data = request.get_json() or {}

        grade = Grade(
            student_id=data.get("student_id"),
            course_id=data.get("course_id"),
            score=data.get("score")
        )

        db.session.add(grade)
        db.session.commit()

        return jsonify({
            "status": "success",
            "data": {
                "id": grade.id,
                "student_id": grade.student_id,
                "course_id": grade.course_id,
                "score": grade.score
            }
        }), 201

    @app.route("/api/grades/<int:id>", methods=["GET", "PUT", "PATCH", "DELETE"])
    @jwt_required()
    def api_grade_detail(id):
        grade = Grade.query.get_or_404(id)

        if request.method == "GET":
            return jsonify({
                "status": "success",
                "data": {
                    "id": grade.id,
                    "student_id": grade.student_id,
                    "course_id": grade.course_id,
                    "score": grade.score,
                    "date": str(grade.date)
                }
            })

        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        if request.method in ["PUT", "PATCH"]:
            data = request.get_json() or {}

            grade.student_id = data.get("student_id", grade.student_id)
            grade.course_id = data.get("course_id", grade.course_id)
            grade.score = data.get("score", grade.score)

            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "Grade updated"
            })

        db.session.delete(grade)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Grade deleted"
        })
