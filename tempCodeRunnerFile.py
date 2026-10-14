@app.route('/signup')
def signup_page():
    return render_template("auth/signup.html")

app.run(debug=False)