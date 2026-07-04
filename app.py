from flask import Flask, render_template

app = Flask(__name__)
# app.secret_key = "development-key"  # improve later

@app.route("/")
def index():
    return render_template("base.html")