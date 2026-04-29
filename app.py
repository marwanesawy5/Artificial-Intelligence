# app.py

from flask import Flask, request, jsonify, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import db, User, Watchlist
from llm import ask_llm
import webbrowser
import threading
from planner import planner_bp
app = Flask(__name__)
app.register_blueprint(planner_bp)
# -------------------
# CONFIG
# -------------------
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# -------------------
# EXTRA TABLE
# -------------------
class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    message = db.Column(db.Text)
    reply = db.Column(db.Text)

# -------------------
# CREATE DATABASE
# -------------------
with app.app_context():
    db.create_all()

# -------------------
# AUTH ROUTES
# -------------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("Username or Email already exists.")
            return redirect(url_for("signup"))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully.")
        return redirect(url_for("login"))

    return send_from_directory(".", "signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.")
        return redirect(url_for("login"))

    return send_from_directory(".", "login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


# -------------------
# MAIN PAGES
# -------------------

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return send_from_directory(".", "dashboard.html")


@app.route("/markets")
def markets():
    return send_from_directory(".", "markets.html")


@app.route("/nearby")
def nearby():
    return send_from_directory(".", "nearby.html")


@app.route("/inputs")
def inputs():
    return send_from_directory(".", "inputs.html")


@app.route("/chatbot")
def chatbot():
    return send_from_directory(".", "chatbot.html")


# -------------------
# STATIC FILES
# CSS / JS / Images
# -------------------

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)


# -------------------
# CHAT API
# -------------------

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data["message"]

    reply = ask_llm(message)

    username = session.get("username", "guest")

    new_chat = ChatHistory(
        username=username,
        message=message,
        reply=reply
    )

    db.session.add(new_chat)
    db.session.commit()

    return jsonify({"reply": reply})


# -------------------
# AUTO OPEN BROWSER
# -------------------

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")


if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, use_reloader=False)