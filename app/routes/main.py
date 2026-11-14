from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.routes.gestionnaire_utilisateur import GestionnaireUtilisateurs
from app.routes.livre import Livre

main_bp = Blueprint("main", __name__)
gestionnaire = GestionnaireUtilisateurs()

def trouver_utilisateur(username):
    for u in gestionnaire.utilisateurs:
        if u.username == username:
            return u
    return None

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/library")
def library():
    username = session.get("username")
    user_actuel = trouver_utilisateur(username)
    if not user_actuel:
        return redirect(url_for("main.login"))
    
    return render_template("index.html", livres=user_actuel.livres, user=user_actuel)

@main_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if not gestionnaire.ajouter_utilisateur(username, password):
        flash("Ce nom d'utilisateur est déjà pris.")
        return redirect(url_for("main.login"))

    session["logged_in"] = True
    session["username"] = username
    return redirect(url_for("main.library"))

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = gestionnaire.connexion(username, password)
        if user:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("main.library"))
        else:
            flash("Pseudo ou mot de passe incorrect.")
            
    return render_template("login.html")

@main_bp.route("/ajouter_livre", methods=["POST"])
def ajouter_livre():
    username = session.get("username")
    user_actuel = trouver_utilisateur(username)
    if not user_actuel:
        return redirect(url_for("main.login"))

    titre = request.form.get("titre")
    auteur = request.form.get("auteur")
    pages_totales = int(request.form.get("pages_totales", 0))
    pages_lues = int(request.form.get("pagesLu", 0))

    nouveau_livre = Livre(titre, auteur, pages_totales, pages_lues)
    user_actuel.ajouter_livre(nouveau_livre)
    
    return redirect(url_for("main.library"))

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
