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
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])

    ids = get_db().get_latest_id()
    liste_aleatoire = []
    for i in range(0,len(ids)):
        index = randrange( len(ids))
        animal = get_db().get_animal_by_id(int(ids[index][0]))
        ids[index] = ids[-1]
        del ids[-1]
        liste_aleatoire.append(animal)
    liste_animaux = Animal.init_list(liste_aleatoire)
    return render_template('accueil.html',cinq=liste_animaux[:5], username=username)


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
        return redirect("/mes-informations")
        # Si le mot de passe ne correspond pas, on recommence    
    else:
        return redirect('/authentification')


# Redirige vers une page de connexion sur le site
@app.route('/authentification', methods=["GET", "POST"])
def authentification():
    if "id" in session:
        return redirect('/')

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
            return redirect("/mes-informations")
        # Si le mot de passe ne correspond pas, on recommence    
        else:
            return render_template(
                "authentification.html",
                                 mdp="mdp incorrect")


# Route pour l'information client 
@app.route('/mes-informations')
def info_client():
    username = None
    email = None
    if "id" in session:
            username = get_db().get_session(session["id"])
            email = get_db().get_email(session["id"])
    else:
        return render_template('authentification.html', wrongMatricule="fx"), 401

    if request.method == "GET":
        return render_template("info-client.html", username=username, 
                                                       email=email)
    else:
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        mdp = request.form["mdp"]
        num_tel = request.form["tel"]
        adresse = request.form["addr"]
        ville = request.form["ville"]
        cp = request.form["CP"]

        regex_cp = r'[A-Za-z0-9]{6}'
        if re.match(regex_cp, cp) is None:
            return render_template("info-client.html", wrong="Wrong") 

        return render_template("info-client.html", modif="OK")    
        

# Route pour faire adopter un animal
@app.route('/adoption', methods=["GET", "POST"])
def adoption():
    username = None
    email = None
    if "id" in session:
        email = get_db().get_email(session["id"])
        username = get_db().get_session(session["id"])
    else:
        return render_template('authentification.html', wrongMatricule="fx"), 401

    if request.method == "GET":
            return render_template("adoption.html", username=username)
    else:
        nom_animal = request.form["nom_animal"]
        type_animal = request.form["type_animal"]
        race = request.form["race"]
        age = request.form["age"]
        description = request.form["description"]
        
        image = None
        image_id = None
        if "photo" in request.files:
            image = request.files["photo"]
            image_id = str(uuid.uuid4().hex)

        # Si des champs sont vides
        if (nom_animal == "" or type_animal == "" or race== "" or age == ""
            or  description == ""):
            return render_template("adoption.html", error="obligatoires")

        db = get_db()
        db.insert_animal(nom_animal, type_animal, race, age, email, description, image_id)
        if image_id is not None :
          db.insert_animal_photo(image_id, image)

        id = db.get_animal_from_image_id(nom_animal, email, image_id)

        return redirect("/confirmation")


# Route qui permet l'inscription d'un nouvel utilisateur
@app.route('/inscription', methods=["GET", "POST"])
def inscription():
    if "id" in session:
        return redirect('/')

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
    username = None
    email = None
    if "id" in session:
        username = get_db().get_session(session["id"])
       

    page = get_db().get_animal_by_id(id)
    if page is None :
        return render_template(("404.html"))
    else :
        animal = Animal(page[0],page[1],page[2],page[3],page[4],page[5],page[6])
        return render_template(("animal.html"),id=id, animal=animal, username=username)




@app.route('/cinq-animaux/<recherche>')
def cinq_animaux(recherche):
    username = None
    if "id" in session:
        username = get_db().get_session(session["id"])

    animaux_raw = get_db().get_recherche(recherche)
    animaux = Animal.init_list(animaux_raw)
    return render_template('cinq-animaux.html', animaux=animaux, username=username)


# Route pour l'application API
@app.route('/api/animals/', methods=["GET"])
def liste_animaux():
    if request.method == "GET":
        animals = get_db().get_animals()
        data = [{"nom": each[1],"type":each[2],"race":each[3],"age":each[4],"description":each[5],"mail_proprio":each[6], "_id": each[0]} for each in animals]
        return jsonify(data)

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