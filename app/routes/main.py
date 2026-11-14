import bcrypt
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.routes.utilisateurs import Utilisateur
from app.routes.books import Livre

main_bp = Blueprint("main", __name__)

# Stockage temporaire en mémoire (dictionnaire {username: objet_Utilisateur})
utilisateurs_db = {}

@main_bp.route("/")
def home():
    return render_template("home.html")

@main_bp.route("/library")
def library():
    username = session.get("username")
    if not username or username not in utilisateurs_db:
        return redirect(url_for("main.login"))
    
    user_actuel = utilisateurs_db[username]
    return render_template("index.html", livres=user_actuel.livres, user=user_actuel)

@main_bp.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")

    if username in utilisateurs_db:
        flash("Ce nom d'utilisateur est déjà pris.")
        return redirect(url_for("main.login"))

    # Hachage du mot de passe pour la méthode verifier_mdp de ton coéquipier
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    nouvel_user = Utilisateur(username, hashed_pw)
    utilisateurs_db[username] = nouvel_user
    
    session["logged_in"] = True
    session["username"] = username
    return redirect(url_for("main.library"))

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = utilisateurs_db.get(username)
        if user and user.verifier_mdp(password):
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("main.library"))
        else:
            flash("Pseudo ou mot de passe incorrect.")
            
    return render_template("login.html")

@main_bp.route("/ajouter_livre", methods=["POST"])
def ajouter_livre():
    username = session.get("username")
    if not username or username not in utilisateurs_db:
        return redirect(url_for("main.login"))

    titre = request.form.get("titre")
    auteur = request.form.get("auteur")
    pages_totales = int(request.form.get("pages_totales", 0))
    pages_lues = int(request.form.get("pagesLu", 0))

    nouveau_livre = Livre(titre, auteur, pages_totales, pages_lues)
    utilisateurs_db[username].ajouter_livre(nouveau_livre)
    
    return redirect(url_for("main.library"))

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))
