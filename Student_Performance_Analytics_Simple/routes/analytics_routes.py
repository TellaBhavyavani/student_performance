import io
import pandas as pd

from flask import render_template, request, redirect, url_for, send_file
from models import Student, Course, Grade, db
from auth import is_logged_in, is_admin
from analytics import get_analytics


def register_analytics_routes(app):

    @app.route("/analytics")
    def analytics_page():
        if not is_logged_in():
            return redirect(url_for("login"))

        course_code = request.args.get("course")
        student_email = request.args.get("student")

        result = get_analytics(course_code, student_email)

        courses = Course.query.all()
        students = Student.query.all()

        return render_template(
            "analytics.html",
            result=result,
            courses=courses,
            students=students
        )

    @app.route("/analytics/export/csv")
    def export_csv():
        if not is_logged_in():
            return redirect(url_for("login"))

        result = get_analytics()
        df = result["data"]

        output = io.BytesIO()
        output.write(df.to_csv(index=False).encode("utf-8"))
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="student_grades.csv",
            mimetype="text/csv"
        )

    @app.route("/analytics/export/xlsx")
    def export_xlsx():
        if not is_logged_in():
            return redirect(url_for("login"))

        result = get_analytics()
        df = result["data"]

        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Grades")

        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="student_grades.xlsx",
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    @app.route("/analytics/upload", methods=["POST"])
    def upload_csv():
        if not is_admin():
            return redirect(url_for("analytics_page"))

        file = request.files.get("file")

        if not file:
            return redirect(url_for("analytics_page"))

        df = pd.read_csv(file)

        for _, row in df.iterrows():
            student = Student.query.filter_by(
                email=row["student_email"]
            ).first()

            course = Course.query.filter_by(
                code=row["course_code"]
            ).first()

            if student and course:
                grade = Grade(
                    student_id=student.id,
                    course_id=course.id,
                    score=float(row["score"])
                )

                db.session.add(grade)

        db.session.commit()

        return redirect(url_for("analytics_page"))
