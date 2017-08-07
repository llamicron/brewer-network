from flask import Flask, request, render_template, url_for
app = Flask(__name__)

@app.route("/")

def index():
    return render_template("set_wifi.html")

@app.route("/set-wifi", methods = ["POST", "GET"])

def handle_form_post():
    if request.method == "POST":
        return write_wpa_supplicant(request.form['ssid'], request.form["password"])
    else:
        return "Bad request"

def write_wpa_supplicant(ssid, password):
    return ssid
