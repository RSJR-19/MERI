from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import os

load_dotenv()
app = Flask(__name__)

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
    return "<h1>Success</h1>"

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute("SELECT password_hash, username FROM users WHERE email = %s", (email,))

    user = cursor.fetchone()

    if user is None:
        return "<h1>User not found!</h1>"

    else:
        if check_password_hash(user[0], password):
            return f"<h1> Welcome Back, {user[1]}!"
        else:
            return f"Wrong password!"

    

app.run(debug=False)