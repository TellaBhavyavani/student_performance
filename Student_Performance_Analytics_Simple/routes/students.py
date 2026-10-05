from flask import render_template, request, redirect, url_for, jsonify, session
from models import db, Student, Grade
from auth import is_logged_in, is_admin


def register_student_routes(app):

    @app.route("/students")
    def students():
        if not is_logged_in():
            return redirect(url_for("login"))

        students = Student.query.all()
        return render_template("students.html", students=students)

    @app.route("/students/new")
    def new_student():
        if not is_admin():
            return redirect(url_for("students"))
        return render_template("student_form.html", student=None)

    @app.route("/students", methods=["POST"])
    def create_student():
        if not is_admin():
            return redirect(url_for("students"))

        name = request.form.get("name")
        email = request.form.get("email")

        if not name or not email:
            return render_template(
                "student_form.html",
                student=None,
                error="Name and email are required"
            )

        if Student.query.filter_by(email=email).first():
            return render_template(
                "student_form.html",
                student=None,
                error="Email already exists"
            )

        student = Student(name=name, email=email)
        db.session.add(student)
        db.session.commit()

        return redirect(url_for("students"))

    @app.route("/students/<int:id>")
    def student_detail(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        student = Student.query.get_or_404(id)

        if session.get("role") == "student":
            if session.get("email") != student.email:
                return "Access denied", 403

        return render_template("student_detail.html", student=student)

    @app.route("/students/<int:id>/edit")
    def edit_student(id):
        if not is_admin():
            return redirect(url_for("students"))

        student = Student.query.get_or_404(id)
        return render_template("student_form.html", student=student)

    @app.route("/students/<int:id>", methods=["PUT", "PATCH", "POST"])
    def update_student(id):
        if not is_admin():
            return redirect(url_for("students"))

        student = Student.query.get_or_404(id)

        if request.method == "POST":
            method = request.form.get("_method", "PUT").upper()
            if method not in ["PUT", "PATCH"]:
                return redirect(url_for("students"))

            student.name = request.form.get("name")
            student.email = request.form.get("email")

        else:
            data = request.get_json() or {}
            student.name = data.get("name", student.name)
            student.email = data.get("email", student.email)

        db.session.commit()

        if request.is_json:
            return jsonify({
                "status": "success",
                "data": {
                    "id": student.id,
                    "name": student.name,
                    "email": student.email
                }
            })

        return redirect(url_for("student_detail", id=id))

    @app.route("/students/<int:id>", methods=["DELETE"])
    def delete_student(id):
        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        student = Student.query.get_or_404(id)
        Grade.query.filter_by(student_id=id).delete()
        db.session.delete(student)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Student deleted"
        })
