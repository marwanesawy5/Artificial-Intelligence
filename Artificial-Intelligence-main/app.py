import os
import threading
import webbrowser
import requests
from datetime import timedelta
from dotenv import load_dotenv

# 1. Load environment variables first
load_dotenv()

from flask import Flask, request, jsonify, redirect, url_for, session, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from auth.models import db, User, Watchlist, FinancialData, ChatHistory
from llm import ask_llm
from planner import planner_bp

# 2. Initialize App
app = Flask(__name__)

# -------------------
# CONFIG
# -------------------
app.config["SECRET_KEY"] = "MySuperSecretKey2026"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Bulletproof Session Settings
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_NAME"] = "mawzoon_session"

# 3. Initialize Extensions
db.init_app(app)
app.register_blueprint(planner_bp)

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
        new_user = User(username=username, email=email, password=hashed_password)

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
            session.permanent = True 
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for("dashboard"))
        
        return redirect(url_for("login" , error = "true"))
    
    return send_from_directory(".", "login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# -------------------
# API & PAGES
# -------------------

@app.route("/api/finances")
def get_finances():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    current_user_id = session["user_id"]
    user_finances = FinancialData.query.filter_by(user_id=current_user_id).first()
    
    if not user_finances:
        return jsonify({"monthly_savings": 0, "investments": 0, "emergency_fund": 0, "expenses": 0})
        
    return jsonify({
        "monthly_savings": user_finances.monthly_savings,
        "investments": user_finances.investments,
        "emergency_fund": user_finances.emergency_fund,
        "expenses": user_finances.expenses
    })

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return send_from_directory(".", "dashboard.html")

@app.route("/markets")
def markets(): return send_from_directory(".", "markets.html")

@app.route("/nearby")
def nearby(): return send_from_directory(".", "nearby.html")

@app.route("/inputs")
def inputs(): return send_from_directory(".", "inputs.html")

@app.route("/chatbot")
def chatbot(): return send_from_directory(".", "chatbot.html")

# -------------------
# CHAT API
# -------------------

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data["message"]
        reply = ask_llm(message)
        
        username = session.get("username", "guest")
        user_id = session.get("user_id", None)

        new_chat = ChatHistory(
            user_id=user_id,
            username=username,
            message=message,
            reply=reply
        )
        db.session.add(new_chat)
        db.session.commit()

        # FIXED: You must return the reply so the frontend can display it!
        return jsonify({"reply": reply})
    
    except Exception as e:
        return jsonify({"reply": "I'm having trouble connecting to my brain right now. Try again?"}), 500

@app.route("/api/chat_history", methods=["GET"])
def get_chat_history():
    if "user_id" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    history = ChatHistory.query.filter_by(user_id=session["user_id"]).order_by(ChatHistory.timestamp.asc()).all()
    
    return jsonify([{
        "message": h.message,
        "reply": h.reply,
        "date": h.timestamp.strftime("%b %d, %H:%M")
    } for h in history])

# -------------------
# MARKETS API
# -------------------

@app.route("/api/markets")
def get_markets():
    try:
        crypto = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd").json()
        gold_chart = requests.get("https://api.coingecko.com/api/v3/coins/pax-gold/market_chart?vs_currency=usd&days=7").json()

        gold_prices = [price[1] for price in gold_chart["prices"]] if "prices" in gold_chart else [2300, 2310, 2290, 2320, 2330, 2340, 2350]
        stocks = {"AAPL": 185.2, "MSFT": 410.5, "TSLA": 172.3}

        return jsonify({"crypto": crypto, "gold": gold_prices, "stocks": stocks})
    except Exception as e:
        return jsonify({"error": str(e)})

# -------------------
# STATIC FILES & SERVER
# -------------------

@app.route("/<path:filename>")
def files(filename):
    return send_from_directory(".", filename)

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, use_reloader=False)