from flask import Flask, render_template, request, redirect, session
from cs50 import SQL

app = Flask(__name__)
app.config["SECRET_KEY"] = "parole123"

db = SQL("sqlite:///datubaze.db")


@app.route("/", methods=["GET"])
def index():
    if "user_id" not in session:
        return redirect("/login")

    user = db.execute(
        "SELECT lietotajvards, vards, uzvards FROM lietotaji WHERE id=?;",
        session["user_id"]
    )

    if not user:
        session.clear()
        return redirect("/login")

    return render_template("index.html", user=user[0])


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    lietotajvards = (request.form.get("lietotajvards") or "").strip()
    parole = request.form.get("parole") or ""

    if not lietotajvards or not parole:
        return redirect("/login")

    lietotajs = db.execute(
        "SELECT * FROM lietotaji WHERE lietotajvards=? AND parole=?;",
        lietotajvards,
        parole
    )

    if lietotajs:
        session["user_id"] = lietotajs[0]["id"]
        return redirect("/")

    return redirect("/register")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    lietotajvards = (request.form.get("lietotajvards") or "").strip()
    parole = request.form.get("parole") or ""
    apst_parole = request.form.get("apst-parole") or ""
    vards = (request.form.get("vards") or "").strip()
    uzvards = (request.form.get("uzvards") or "").strip()

    if not lietotajvards or not parole:
        return redirect("/register")

    if parole != apst_parole:
        return redirect("/register")

    lietotajs = db.execute(
        "SELECT id FROM lietotaji WHERE lietotajvards=?;",
        lietotajvards
    )

    if lietotajs:
        return redirect("/register")

    result = db.execute(
        "INSERT INTO lietotaji(lietotajvards, parole, vards, uzvards) VALUES(?, ?, ?, ?);",
        lietotajvards,
        parole,
        vards,
        uzvards
    )

    if result:
        session["user_id"] = result

    return redirect("/")


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
