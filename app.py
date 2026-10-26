from flask import Flask, request, render_template, jsonify, session, url_for, redirect
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector
import os
from services import AuthServiceFactory

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
    service = AuthServiceFactory.create("signup", cursor, connection)

    result, status_code = service.execute(request.form)

    if not result["success"]:
        return jsonify(result), status_code
    else:
        session['username'] = result['username']
        session['email'] = result['email']

        result['redirect'] = url_for('dashboard')

        return jsonify(result), status_code


@app.route('/login', methods=['POST'])
def login():
    service = AuthServiceFactory.create("login", cursor)

    result, status_code = service.execute(request.form)

    if not result['success']:
        return jsonify(result), status_code

    session['username'] = result['username']
    session['email'] = result['email']

    result['redirect'] = url_for('dashboard')

    return jsonify(result), status_code

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index_page"))

    return render_template(
        "dashboard/dashboard.html",
        username=session["username"]
    )

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "success": True,
        "redirect": url_for("index_page")
    })

@app.route("/check-username", methods=['POST'])
def checkUsername():
    username = request.form.get("username")
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))

    if cursor.fetchone():
        return {
            'success' : False,
            'message' : 'Username already taken!'
        }, 409

    return {
        'success' : True,
        'message' : 'Username available'
    }, 200

app.run(debug=False)