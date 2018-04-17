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
from flask import Response
from functools import wraps
from .database import Database
from .objets import *
from .mail import *
from flask import jsonify
import re
import hashlib
import uuid
from random import *


# from .objets import *

app = Flask(__name__, static_url_path="", static_folder="static")


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


# Affiche la page d'accueil
@app.route('/')
def front_page():
    user = None
    if "id" in session:
        username = get_db().get_session(session["id"])
        return render_template('index.html',username=username)

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
        prenom = get_db().get_login(email)
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, prenom, email)
        session["id"] = id_session
        return redirect("/")
        # Si le mot de passe ne correspond pas, on recommence    
    else:
        return redirect('/authentification')


# Route pour l'application API
@app.route('/api/animals/', methods=["GET"])
def liste_animaux():
    if request.method == "GET":
        animals = get_db().get_animals()
        data = [{"nom": each[1],"type":each[2],"race":each[3],"age":each[4],"description":each[5],"mail_proprio":each[6], "_id": each[0]} for each in animals]
        return jsonify(data)


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
            prenom = get_db().get_login(email)
            # Accès autorisé
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, prenom, email)
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



@app.route('/<id>')
def page_animal(id):
    page = get_db().get_animal_by_id(id)
    if page is None :
        return render_template(("404.html"))
    else :
        animal = Animal(page[0],page[1],page[2],page[3],page[4],page[5],page[6])
        return render_template(("animal.html"),id=id, animal=animal)




@app.route('/cinq-animaux/<recherche>')
def cinq_animaux(recherche):
    animaux_raw = get_db().get_recherche(recherche)
    animaux = Animal.init_list(animaux_raw)
    return render_template('cinq-animaux.html', animaux=animaux)


# # La page 404.html en cas d'erreur
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404




def authentication_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_authenticated(session):
            return send_unauthorized()
        return f(*args, **kwargs)
    return decorated


@app.route('/logout')
@authentication_required
def logout():
    id_session = session["id"]
    session.pop('id', None)
    get_db().delete_session(id_session)
    return redirect("/")


def is_authenticated(session):
    return "id" in session


def send_unauthorized():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})    



app.secret_key = "(*&*&322387he738220)(*(*22347657"