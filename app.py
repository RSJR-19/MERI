from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def signup_page():
    return render_template("auth/signup.html")

app.run(debug=False)