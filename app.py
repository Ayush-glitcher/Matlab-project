from flask import Flask, render_template, request, jsonify, session, redirect
from ode_solver import solve_ode

app = Flask(__name__)
app.secret_key = "secret123"

USERNAME = "admin"
PASSWORD = "1234"


@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")



@app.route("/simulation")
def simulation():

    if "user" not in session:
        return redirect("/login")

    return render_template("simulation.html")

@app.route("/get_solution", methods=["POST"])
def get_solution():

    data = request.json

    equation = data["equation"]

    result = solve_ode(equation)

    return jsonify(result)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:
            session["user"] = username
            return redirect("/")

        return "Invalid Login"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/solve", methods=["POST"])
def solve():

    data = request.json
    equation = data["equation"]

    try:
        result = solve_ode(equation)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)