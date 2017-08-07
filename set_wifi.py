from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route("/")

def home(name=None):
    # Return a view
    return render_template("set_wifi.html", name=name)
