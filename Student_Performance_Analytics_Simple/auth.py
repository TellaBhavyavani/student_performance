from flask import render_template, request, redirect, url_for, session, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User


def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role, "email": user.email}
        )
        session["token"] = token
        session["user_id"] = user.id
        session["role"] = user.role
        session["email"] = user.email
        return user

    return None


def register_auth_routes(app):

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form.get("email")
            password = request.form.get("password")

            user = login_user(email, password)

            if user:
                return redirect(url_for("dashboard"))

            return render_template("login.html", error="Invalid email or password")

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("home"))

    @app.route("/api/login", methods=["POST"])
    def api_login():
        data = request.get_json() or {}
        user = login_user(data.get("email"), data.get("password"))

        if not user:
            return jsonify({
                "status": "error",
                "message": "Invalid email or password"
            }), 401

        return jsonify({
            "status": "success",
            "data": {
                "token": session["token"],
                "user_id": user.id,
                "name": user.name,
                "role": user.role
            }
        }), 200


def is_logged_in():
    return "user_id" in session


def is_admin():
    return session.get("role") == "admin"


def current_user():
    if not is_logged_in():
        return None
    return User.query.get(session["user_id"])


def create_demo_users():
    if User.query.count() == 0:
        admin = User(
            name="Admin",
            email="admin@example.com",
            password=generate_password_hash("admin123"),
            role="admin"
        )

        student = User(
            name="Alice",
            email="alice@example.com",
            password=generate_password_hash("student123"),
            role="student"
        )

        db.session.add(admin)
        db.session.add(student)
        db.session.commit()
