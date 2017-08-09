from flask import Flask, request, render_template, url_for, redirect, session, flash
import os
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yXR~XHh!jmN[LWx/,0RT'
# app.wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"
app.webhook_file = os.path.expanduser("~") + "/slack.webhook"
app.wpa_supplicant = os.path.dirname(
    os.path.realpath(__file__)) + "/test_wpa_supplicant"


@app.route("/")
def index():
    return render_template(
        "index.html",
        file=app.wpa_supplicant,
        file_lines=get_file_contents(app.wpa_supplicant))


@app.route("/write-supplicant", methods=["POST"])
def handle_supplicant_form_post():
    if not validate_form_submission(request.form):
        session['error'] = True
        flash("Please fill out the form to the right ->")
        return redirect("/")

    try:
        write_wpa_supplicant(request.form['ssid'], request.form["password"],
                             request.form['priority'])
        session['error'] = False
        flash("Successful. Restart your Pi to connect.")
    except IOError:
        session["error"] = True
        flash(
            "You don't have permission to write to %s. Please run this web server with 'sudo', and if that doesn't work, get Luke."
            % app.wpa_supplicant)
    return redirect("/")

@app.route("/write-webhook", methods = ["POST"])
def handle_webhook_form_post():
    if not validate_form_submission(request.form):
        session["error"] = True
        flash("Please enter your slack webhook.")
        return redirect("/")
    try:
        write_webhook(request.form["webhook"])
        flash("Slack Webhook Set")
    except IOError:
        session["error"] = True
        flash("Failed (IOError): Can't write to file. Get Luke to fix this.")
    return redirect("/")

def write_webhook(webhook):
    with open(app.webhook_file, "w+") as file:
        file.truncate()
        file.write(webhook)
        return True
    return False

def write_wpa_supplicant(ssid, password, priority):
    wpa = open(app.wpa_supplicant, "a")
    wpa.write("\nnetwork={\n\tssid=\"%s\"\n\tpsk=\"%s\"\n\tpriority=%s\n}" %
              (ssid, password, priority))


# Returns true if all fields contain a string
def validate_form_submission(form):
    for field, value in request.form.iteritems():
        if not value:
            return False
    return True


def get_file_contents(filename):
    with open(filename, 'r') as content_file:
        return list(filter(None, content_file.read().splitlines()))


if __name__ == '__main__':
    app.run(debug=True)
