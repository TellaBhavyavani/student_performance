from flask import render_template, request, redirect, url_for, jsonify
from models import db, Grade, Student, Course
from auth import is_logged_in, is_admin


def register_grade_routes(app):

    @app.route("/grades")
    def grades():
        if not is_logged_in():
            return redirect(url_for("login"))

        grades = Grade.query.all()
        return render_template("grades.html", grades=grades)

    @app.route("/grades/new")
    def new_grade():
        if not is_admin():
            return redirect(url_for("grades"))

        students = Student.query.all()
        courses = Course.query.all()

        return render_template(
            "grade_form.html",
            grade=None,
            students=students,
            courses=courses
        )

    @app.route("/grades", methods=["POST"])
    def create_grade():
        if not is_admin():
            return redirect(url_for("grades"))

        student_id = request.form.get("student_id")
        course_id = request.form.get("course_id")
        score = request.form.get("score")

        if not student_id or not course_id or not score:
            return redirect(url_for("new_grade"))

        grade = Grade(
            student_id=int(student_id),
            course_id=int(course_id),
            score=float(score)
        )

        db.session.add(grade)
        db.session.commit()

        return redirect(url_for("grades"))

    @app.route("/grades/<int:id>")
    def grade_detail(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        grade = Grade.query.get_or_404(id)
        return render_template("grade_detail.html", grade=grade)

    @app.route("/grades/<int:id>/edit")
    def edit_grade(id):
        if not is_admin():
            return redirect(url_for("grades"))

        grade = Grade.query.get_or_404(id)
        students = Student.query.all()
        courses = Course.query.all()

        return render_template(
            "grade_form.html",
            grade=grade,
            students=students,
            courses=courses
        )

    @app.route("/grades/<int:id>", methods=["PUT", "PATCH", "POST"])
    def update_grade(id):
        if not is_admin():
            return redirect(url_for("grades"))

        grade = Grade.query.get_or_404(id)

        if request.method == "POST":
            grade.student_id = int(request.form.get("student_id"))
            grade.course_id = int(request.form.get("course_id"))
            grade.score = float(request.form.get("score"))
        else:
            data = request.get_json() or {}
            grade.student_id = data.get("student_id", grade.student_id)
            grade.course_id = data.get("course_id", grade.course_id)
            grade.score = data.get("score", grade.score)

        db.session.commit()

        if request.is_json:
            return jsonify({
                "status": "success",
                "data": {
                    "id": grade.id,
                    "student_id": grade.student_id,
                    "course_id": grade.course_id,
                    "score": grade.score
                }
            })

        return redirect(url_for("grade_detail", id=id))

    @app.route("/grades/<int:id>", methods=["DELETE"])
    def delete_grade(id):
        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        grade = Grade.query.get_or_404(id)
        db.session.delete(grade)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Grade deleted"
        })
