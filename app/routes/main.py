from flask import Blueprint, render_template, request, redirect, url_for, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/library")
def library():
    # Si l'utilisateur n'est pas connecté, on le renvoie vers login
    if not session.get("logged_in"):
        return redirect(url_for("main.login"))
    return render_template("index.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Simulation de connexion réussie
        session["logged_in"] = True
        return redirect(url_for("main.library"))
    return render_template("login.html")

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
@main_bp.route("/register", methods=["POST"])
def register():
    # Simulation d'inscription réussie en attendant le code de ton coéquipier
    session["logged_in"] = True
    return redirect(url_for("main.library"))

