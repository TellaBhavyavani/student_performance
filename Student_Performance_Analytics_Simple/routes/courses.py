from flask import render_template, request, redirect, url_for, jsonify
from models import db, Course, Grade
from auth import is_logged_in, is_admin


def register_course_routes(app):

    @app.route("/courses")
    def courses():
        if not is_logged_in():
            return redirect(url_for("login"))

        courses = Course.query.all()
        return render_template("courses.html", courses=courses)

    @app.route("/courses/new")
    def new_course():
        if not is_admin():
            return redirect(url_for("courses"))
        return render_template("course_form.html", course=None)

    @app.route("/courses", methods=["POST"])
    def create_course():
        if not is_admin():
            return redirect(url_for("courses"))

        name = request.form.get("name")
        code = request.form.get("code")

        if not name or not code:
            return render_template(
                "course_form.html",
                course=None,
                error="Course name and code are required"
            )

        course = Course(name=name, code=code)
        db.session.add(course)
        db.session.commit()

        return redirect(url_for("courses"))

    @app.route("/courses/<int:id>")
    def course_detail(id):
        if not is_logged_in():
            return redirect(url_for("login"))

        course = Course.query.get_or_404(id)
        return render_template("course_detail.html", course=course)

    @app.route("/courses/<int:id>/edit")
    def edit_course(id):
        if not is_admin():
            return redirect(url_for("courses"))

        course = Course.query.get_or_404(id)
        return render_template("course_form.html", course=course)

    @app.route("/courses/<int:id>", methods=["PUT", "PATCH", "POST"])
    def update_course(id):
        if not is_admin():
            return redirect(url_for("courses"))

        course = Course.query.get_or_404(id)

        if request.method == "POST":
            method = request.form.get("_method", "PUT").upper()
            if method not in ["PUT", "PATCH"]:
                return redirect(url_for("courses"))

            course.name = request.form.get("name")
            course.code = request.form.get("code")
        else:
            data = request.get_json() or {}
            course.name = data.get("name", course.name)
            course.code = data.get("code", course.code)

        db.session.commit()

        if request.is_json:
            return jsonify({
                "status": "success",
                "data": {
                    "id": course.id,
                    "name": course.name,
                    "code": course.code
                }
            })

        return redirect(url_for("course_detail", id=id))

    @app.route("/courses/<int:id>", methods=["DELETE"])
    def delete_course(id):
        if not is_admin():
            return jsonify({"status": "error", "message": "Admin only"}), 403

        course = Course.query.get_or_404(id)
        Grade.query.filter_by(course_id=id).delete()
        db.session.delete(course)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Course deleted"
        })
