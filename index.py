# PHOUANGSY SOPHIE PHOS06609507
# BONNAIRE BENJAMIN BONB03049706
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import redirect
from flask import make_response
from flask import url_for
from .database import Database
from .mail import *
import re
# from .objets import *

app = Flask(__name__, static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.deconnexion()


@app.route('/')
def front_page():
    return render_template('index.html')


# Récupère les données de connexion et redirige l'utilisateur a l'index
@app.route('/', methods=["POST"])
def authentification():
    return response

# Route qui permet l'inscription d'un nouvel utilisateur
@app.route('/inscription', methods=["GET", "POST"])
def inscription():
    if request.method == "GET":
        return render_template("inscription.html")
    else: 
        # On recupere toutes les donnees
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        email = request.form["email"]
        mdp = request.form["mdp"]
        num_tel = request.form["tel"]
        adresse = request.form["addr"]
        ville = request.form["ville"]
        cp = request.form["CP"]

        # On se connecte a la base de donnees
        db = get_db()        
        verification_email = db.verification_email_existant(email)


        regex_cp = r'[A-Za-z0-9]{6}'

        # Si des champs sont vides
        if (nom == "" or prenom == "" or email == "" or mdp == ""
            or  num_tel == "" or adresse == "" or ville == "" or cp == ""):
            return render_template("inscription.html",
                                error="Tous les champs sont obligatoires.")
        elif re.match(regex_cp, cp) is None:
            return render_template("inscription.html", wrong="Wrong") 

        if (verification_email == email):
            return render_template("inscription.html", email="mail existe deja") 


        db.create_user(nom, prenom, email, mdp, num_tel, adresse, ville, cp) 

        return redirect("/confirmation")


# Route qui confirme l'inscription d'un utilisateur
@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")


# Fonction pour se deconnecter
@app.route('/offline')
def offline():
    response = make_response(redirect(url_for('front_page')))
    response.set_cookie('user_matricule', expires=0)
    return response


# Modifie et ajoute des projets et des heures
@app.route('/<matricule>/<date_du_jour>', methods=["POST"])
def ajout_modif(matricule, date_du_jour):
    return response


# Supprime un projet existant
@app.route('/supprimer_projet/<matricule>/<date_du_jour>')
def form_projet(matricule, date_du_jour):
    return render_template()


# Redirige l'user lorsque la suppression est faite
@app.route('/supprimer/<matricule>/<date_du_jour>', methods=["POST"])
def suppression(matricule, date_du_jour):
    response = make_response(
            redirect(url_for()))
    return response


# Affiche le jour, les projets et les heures associées
@app.route('/<matricule>/<date_du_jour>')
def calendrier_jour(matricule, date_du_jour):
        return render_template()


# Affiche le calendrier du mois
@app.route('/<matricule>/overview/<mois>')
def calendrier_mois(matricule, mois):
    return render_template()



# La page 404.html en cas d'erreur
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
