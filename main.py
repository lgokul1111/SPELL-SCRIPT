from flask import Flask, request, jsonify, send_from_directory, Response
from flask import redirect, session
import interpreter


app = Flask(__name__)

app.secret_key = "spellscript-secret-key"


@app.route("/")
def home():

    return send_from_directory("ide", "index.html")

@app.route("/style.css")
def style():

    with open("ide/style.css", "r", encoding="utf-8") as f:
        css = f.read()

    return Response(css, mimetype="text/css")


@app.route("/register", methods=["POST"])
def register():

    name = request.form.get("name")
    age_text = request.form.get("age")

    try:
        age = int(age_text)
    except:
        return jsonify({
            "success": False,
            "message": "Age must be a number."
        })

    if age < 18:

        return jsonify({
            "success": False,
            "message": "You are not eligible to register as a wizard."
        })

    with open("wizards.txt", "a") as f:

        f.write(name + "," + str(age) + "\n")

    session["wizard"] = name

    return jsonify({
        "success": True,
        "message": "Wizard registered successfully."
    })
    
@app.route("/editor.js")
def editor_js():

    with open("ide/editor.js", "r", encoding="utf-8") as f:
        javascript = f.read()

    return Response(javascript, mimetype="application/javascript")

@app.route("/login", methods=["POST"])
def login():

    name = request.form.get("name")

    found = False

    with open("wizards.txt", "r") as f:

        for line in f:

            wizard_name, wizard_age = line.strip().split(",")

            if wizard_name.lower() == name.lower():

                found = True
                session["wizard"] = wizard_name
                break

    if found:

        return jsonify({
            "success": True,
            "message": "Access granted."
        })

    else:

        return jsonify({
            "success": False,
            "message": "Wizard not found. Please register first."
        })

@app.route("/portal")
def portal():

    if "wizard" not in session:

        return redirect("/")

    return send_from_directory("ide", "index.html")


@app.route("/run", methods=["POST"])
def run_spellscript():

    if "wizard" not in session:

        return jsonify({
            "output": "Access denied. Please log in first."
        })

    data = request.get_json()

    source = data.get("source", "")

    result = interpreter.interpret(source)

    return jsonify({
        "output": result
    })

@app.route("/logout")
def logout():

    session.pop("wizard", None)

    return redirect("/")


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )