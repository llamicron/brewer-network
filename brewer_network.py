from flask import Flask, request, render_template, url_for, redirect, session, flash
import os
app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yXR~XHh!jmN[LWx/,0RT'
app.wpa_supplicant = "/etc/wpa_supplicant/wpa_supplicant.conf"
app.token_file = os.path.expanduser("~") + "/slack.token"


@app.route("/")
def index():
    return render_template(
        "index.html",
        file=app.wpa_supplicant,
        file_lines=get_file_contents(app.wpa_supplicant),
        token=get_token())


@app.route("/write-supplicant", methods=["POST"])
def handle_supplicant_form_post():
    if not validate_form_submission(request.form):
        session['error'] = True
        flash("Please fill out the form above")
        return redirect("/")

    try:
        write_wpa_supplicant(request.form['ssid'], request.form["password"],
                             request.form['priority'])
        session['error'] = False
        flash("Successful. Restart your Pi to connect.")
        # Switch to env network
        # Ultimate happy path
    except IOError:
        session["error"] = True
        flash(
            "You don't have permission to write to %s. Please run this web server with 'sudo', and if that doesn't work, get Luke."
            % app.wpa_supplicant)
    return redirect("/")


@app.route("/write-token", methods=["POST"])
def handle_token_form_post():
    if not validate_form_submission(request.form):
        session["error"] = True
        flash("Please enter your Slack API Token.")
        return redirect("/")
    try:
        write_token(request.form["token"])
        session["error"] = False
        flash("Slack API Token Set")
    except IOError:
        flash("Failed (IOError): Can't write to file. Get Luke to fix this.")
        session["error"] = True
    return redirect("/")


def write_token(token):
    with open(app.token_file, "w+") as file:
        file.truncate()
        file.write(token)
        session["token_submitted"] = True
        return True
    return False


def get_token():
    if not os.path.isfile(app.token_file):
        open(app.token_file, "w")
    with open(app.token_file, "r") as file:
        return file.read()

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
