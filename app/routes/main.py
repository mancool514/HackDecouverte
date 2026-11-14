from datetime import date
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort

from app.routes.gestionnaire_utilisateur import GestionnaireUtilisateurs
from app.routes.livre import Livre

main_bp = Blueprint("main", __name__)

# Base de données fixe : 2 utilisateurs de démo chargés depuis app/data/utilisateurs.json
gestionnaire = GestionnaireUtilisateurs()


# --- Utilitaires -------------------------------------------------------------
def login_requis(vue):
    """Redirige vers /login si personne n'est connecté; passe l'utilisateur à la vue."""
    @wraps(vue)
    def wrapper(*args, **kwargs):
        user = gestionnaire.trouver(session.get("username"))
        if user is None:
            session.clear()
            return redirect(url_for("main.login"))
        return vue(user, *args, **kwargs)
    return wrapper


def livre_ou_404(user, livre_id):
    livre = user.trouver_livre(livre_id)
    if livre is None:
        abort(404)
    return livre


def lire_formulaire_livre(form):
    """Valide le formulaire d'ajout/modification. Retourne (données, erreur)."""
    titre = form.get("titre", "").strip()
    auteur = form.get("auteur", "").strip()
    date_limite = form.get("date_limite", "").strip()
    try:
        pages_totales = int(form.get("pages_totales", ""))
        pages_initiales = int(form.get("pages_initiales") or 0)
    except ValueError:
        return None, "Le nombre de pages doit être un nombre entier."
    try:
        date.fromisoformat(date_limite)
    except ValueError:
        return None, "La date limite est invalide."

    if not titre or not auteur:
        return None, "Le titre et l'auteur sont obligatoires."
    if pages_totales <= 0:
        return None, "Le nombre total de pages doit être supérieur à 0."
    if not 0 <= pages_initiales <= pages_totales:
        return None, "La page actuelle doit être entre 0 et le nombre total de pages."

    return {
        "titre": titre,
        "auteur": auteur,
        "pages_totales": pages_totales,
        "pages_initiales": pages_initiales,
        "date_limite": date_limite,
    }, None


# --- Pages publiques ---------------------------------------------------------
@main_bp.route("/")
def home():
    return render_template("home.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("username") and gestionnaire.trouver(session["username"]):
        return redirect(url_for("main.library"))

    if request.method == "POST":
        user = gestionnaire.connexion(request.form.get("username", ""), request.form.get("password", ""))
        if user:
            session["logged_in"] = True
            session["username"] = user.username
            return redirect(url_for("main.library"))
        flash("Pseudo ou mot de passe incorrect.")

    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.home"))


# --- Bibliothèque (dashboard) ------------------------------------------------
@main_bp.route("/library")
@login_requis
def library(user):
    return render_template("index.html", user=user, livres=user.livres, aujourdhui=date.today().isoformat())


@main_bp.route("/livres/ajouter", methods=["POST"])
@login_requis
def ajouter_livre(user):
    donnees, erreur = lire_formulaire_livre(request.form)
    if erreur:
        flash(erreur)
        return redirect(url_for("main.library"))

    user.ajouter_livre(Livre(**donnees))
    gestionnaire.sauvegarde()
    flash(f"« {donnees['titre']} » a été ajouté à ta bibliothèque.")
    return redirect(url_for("main.library"))


@main_bp.route("/livres/<livre_id>")
@login_requis
def detail_livre(user, livre_id):
    livre = livre_ou_404(user, livre_id)
    return render_template("livre.html", user=user, livre=livre, aujourdhui=date.today().isoformat())


@main_bp.route("/livres/<livre_id>/modifier", methods=["POST"])
@login_requis
def modifier_livre(user, livre_id):
    livre = livre_ou_404(user, livre_id)
    donnees, erreur = lire_formulaire_livre(request.form)
    if erreur:
        flash(erreur)
    else:
        for cle, valeur in donnees.items():
            setattr(livre, cle, valeur)
        gestionnaire.sauvegarde()
        flash("Livre modifié.")
    return redirect(url_for("main.detail_livre", livre_id=livre.id))


@main_bp.route("/livres/<livre_id>/supprimer", methods=["POST"])
@login_requis
def supprimer_livre(user, livre_id):
    livre = livre_ou_404(user, livre_id)
    user.retirer_livre(livre)
    gestionnaire.sauvegarde()
    flash(f"« {livre.titre} » a été supprimé.")
    return redirect(url_for("main.library"))


@main_bp.route("/livres/<livre_id>/lecture", methods=["POST"])
@login_requis
def ajouter_lecture(user, livre_id):
    livre = livre_ou_404(user, livre_id)
    jour = request.form.get("date") or date.today().isoformat()
    try:
        pages = int(request.form.get("pages", ""))
        date.fromisoformat(jour)
    except ValueError:
        flash("Nombre de pages ou date invalide.")
        return redirect(url_for("main.detail_livre", livre_id=livre.id))

    if pages <= 0:
        flash("Le nombre de pages lues doit être supérieur à 0.")
    else:
        livre.lire(pages, jour)
        gestionnaire.sauvegarde()
        flash(f"{pages} page(s) ajoutée(s) le {jour}.")
    return redirect(url_for("main.detail_livre", livre_id=livre.id))


@main_bp.route("/livres/<livre_id>/lecture/<int:index>/supprimer", methods=["POST"])
@login_requis
def supprimer_lecture(user, livre_id, index):
    livre = livre_ou_404(user, livre_id)
    if livre.retirer_lecture(index):
        gestionnaire.sauvegarde()
        flash("Séance de lecture supprimée.")
    return redirect(url_for("main.detail_livre", livre_id=livre.id))
