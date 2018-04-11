# PHOUANGSY SOPHIE PHOS06609507
# BONNAIRE BENJAMIN BONB03049706
from flask import Flask
from flask import render_template
from flask import request
from flask import g
from flask import redirect
from flask import make_response
from flask import url_for
from flask import session
from .database import Database
from .objets import *
from .mail import *
import re
import hashlib
import uuid
from random import *
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
    animaux_raw = get_db().get_animals()
    liste_aleatoire = []
    for x in range(0,5):
        index = randrange( len(animaux_raw) - 1)
        animal = animaux_raw[index]
        animaux_raw[index] = animaux_raw[-1]
        del animaux_raw[-1]
        liste_aleatoire.append(animal)
    liste_animaux = Animal.init_list(liste_aleatoire)
    return render_template('index.html',cinq=liste_animaux)


# Récupère les données de connexion et redirige l'utilisateur a l'index
@app.route('/', methods=["POST"])
def connexion():
    email = request.form["email"]
    mdp = request.form["mot_de_passe"]

    if email == "" or mdp == "":
        return redirect("/authentification")

# Si le mail n'existe pas
        mail = get_db().get_login_info(email)
        if mail is None:
            return render_template(
                "authentification.html",
                                 mail="mail n'existe pas")

    # On verifie si le mail correspond au mot de passe
        salt = mail[0]
        hashed_password = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()
        if hashed_password == mail[1]:
            # Accès autorisé
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, email)
            session["id"] = id_session
            return redirect("/")
        # Si le mot de passe ne correspond pas, on recommence    
        else:
            return redirect('/authentification')



# Redirige vers une page de connexion sur le site
@app.route('/authentification', methods=["GET", "POST"])
def authentification():
    if request.method == "GET":
        return render_template("authentification.html")
    else: 
        email = request.form["email"]
        mdp = request.form["mot_de_passe"]

        if email == "" or mdp == "":
            return render_template(
                "authentification.html",
                                 champs="tous champs obligatoires")


    # Si le mail n'existe pas
        mail = get_db().get_login_info(email)
        if mail is None:
            return render_template(
                "authentification.html",
                                 mail="mail n'existe pas")

    # On verifie si le mail correspond au mot de passe
        salt = mail[0]
        hashed_password = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()
        if hashed_password == mail[1]:
            # Accès autorisé
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, email)
            session["id"] = id_session
            return redirect("/")
        # Si le mot de passe ne correspond pas, on recommence    
        else:
            return render_template(
                "authentification.html",
                                 mdp="mdp incorrect")



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










# # La page 404.html en cas d'erreur
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404




app.secret_key = "(*&*&322387he738220)(*(*22347657"