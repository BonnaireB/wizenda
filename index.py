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
from .objets import *

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
    return render_template('form-index.html')


# Récupère les données du formulaire et redirige l'utilisateur a aujourd'hui
@app.route('/', methods=["POST"])
def calendrier():
    return response


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


# # Affiche la liste des mois ou il y a des heures
# @app.route('/<matricule>')
# def matricule_page(matricule):
#         response = make_response(render_template())
#         response.set_cookie("matricule_actuel", matricule)
#         return response


# La page 404.html en cas d'erreur
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
