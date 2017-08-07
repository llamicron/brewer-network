from flask import Flask, request, render_template, url_for, redirect, session
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"


@app.route("/")

def index():
    try:
        return render_template("set_wifi.html", errors = session["message"])
    except KeyError as e:
        return render_template("set_wifi.html", errors = "")

@app.route("/set-wifi", methods = ["POST", "GET"])

def handle_form_post():
    for field, value in request.form.iteritems():
        if not value:
            session["message"] = "Please fill out the form below"
            return redirect("/")
    write_wpa_supplicant(request.form['ssid'], request.form["password"], request.form['priority'])
    session["message"] = "Successful. Restart your Pi to connect"
    return redirect("/")

def write_wpa_supplicant(ssid, password, priority):
    # Write to wpa_supplicant
    wpa = open(wpa_supplicant, "a")
    wpa.write("\nnetwork={\n\tssid=\"%s\"\n\tpsk=\"%s\"\n\tpriority=%s\n}" % (ssid, password, priority))

if __name__ == '__main__':
    app.run()
