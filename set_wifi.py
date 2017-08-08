from flask import Flask, request, render_template, url_for, redirect, session, flash
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yXR~XHh!jmN[LWx/,0RT'
# wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"
wpa_supplicant = "/Users/llamicron/test"

@app.route("/")

def index():
    return render_template(
        "set_wifi.html",
        file=wpa_supplicant,
        file_lines=get_file_contents(wpa_supplicant)
    )

@app.route("/set-wifi", methods = ["POST", "GET"])

def handle_form_post():
    for field, value in request.form.iteritems():
        if not value:
            flash("Please fill out the form to the right ->")
            return redirect("/")
    write_wpa_supplicant(request.form['ssid'], request.form["password"], request.form['priority'])
    flash("Successful. Restart your Pi to connect")
    return redirect("/")

def write_wpa_supplicant(ssid, password, priority):
    # Write to wpa_supplicant
    wpa = open(wpa_supplicant, "a")
    wpa.write("\nnetwork={\n\tssid=\"%s\"\n\tpsk=\"%s\"\n\tpriority=%s\n}" % (ssid, password, priority))


def get_file_contents(filename):
    with open(filename, 'r') as content_file:
        return list(filter(None, content_file.read().splitlines()))

if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
