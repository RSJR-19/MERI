from flask import Flask, request, render_template, jsonify, session, url_for, redirect
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

@app.route('/')
def index_page():
    return render_template("auth/index.html")

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    password = generate_password_hash(password)

    cursor.execute("INSERT INTO users(username,email,password_hash) VALUES (%s, %s, %s)", (username, email, password))
    connection.commit()

    session["username"] = username
    session["email"] = email

    return jsonify({
        "success": True,
        "message": "Account created successfully!",
        "redirect": url_for("dashboard")
    }), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute("SELECT password_hash, username FROM users WHERE email = %s", (email,))

    user = cursor.fetchone()

    if user is None:
        return jsonify({
            "success": False,
            "message": 'User not found'
        }),401

    if not check_password_hash(user[0], password):
        return jsonify({
            "success": False,
            "message": "Incorrect password"
        }), 401

    session["username"] = user[1]
    session['email'] = email

    return jsonify({
        "success": True,
        "message": f"Welcome, {user[1]}!",
        "redirect": url_for("dashboard")
    }), 200

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index_page"))

    return render_template(
        "dashboard/dashboard.html",
        username=session["username"]
    )




    

app.run(debug=False)