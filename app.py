from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import get_db, login_required, inr

app = Flask(__name__)

app.config["SECRET_KEY"] = "development-key"   # replace later with an environment variable

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.jinja_env.filters["inr"] = inr


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            flash("must provide username","danger")
            return redirect(url_for("register"))

        password = request.form.get("password")
        if not password:
            flash("must provide password","danger")
            return redirect(url_for("register"))
        confPass = request.form.get("confirm_password")
        if not confPass:
            flash("must provide the confirm password","danger")
            return redirect(url_for("register"))
        if confPass != password:
            flash("must match the password","danger")
            return redirect(url_for("register"))


        db = get_db()

        cursor_user = db.execute("SELECT username FROM users WHERE username=?", (username,))
        users = cursor_user.fetchone()
        if users:
            flash("Username already exists", "danger")
            db.close()
            return redirect(url_for("register"))
        
        hashPass = generate_password_hash(password)

        db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)", (username, hashPass))
        db.commit()

        db.close()

        flash("Registration successful! Please log in.", "success")

        return redirect(url_for("login"))
    

    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    
    else:
        return render_template("login.html")