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
from .email import *
from flask import jsonify
from random import *
from uuid import uuid4

import re
import hashlib
import uuid
import calendar
import datetime

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
        username = get_db().get_fname()

    ids = get_db().get_latest_id()
    liste_aleatoire = []
    for i in range(0, len(ids)):
        index = randrange(len(ids))
        animal = get_db().get_animal_by_id(int(ids[index][0]))
        ids[index] = ids[-1]
        del ids[-1]
        liste_aleatoire.append(animal)
    liste_animaux = Animal.init_list(liste_aleatoire)
    return render_template('accueil.html', cinq=liste_animaux[:5],
                           username=username)


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
        return render_template("authentification.html",
                               mail="mail n'existe pas")

    # On verifie si le mail correspond au mot de passe
    salt = mail[0]
    hashed_password = (hashlib.sha512(str(mdp +
                       salt).encode("utf-8")).hexdigest())
    if hashed_password == mail[1]:
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, email)
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
            return render_template("authentification.html",
                                   champs="tous champs obligatoires")

    # Si le mail n'existe pas
        mail = get_db().get_login_info(email)
        if mail is None:
            return render_template("authentification.html",
                                   mail="mail n'existe pas")

    # On verifie si le mail correspond au mot de passe
        salt = mail[0]
        hashed_password = (hashlib.sha512(str(mdp +
                           salt).encode("utf-8")).hexdigest())
        if hashed_password == mail[1]:
            # Accès autorisé
            id_session = uuid.uuid4().hex
            get_db().save_session(id_session, email)
            session["id"] = id_session
            return redirect("/mes-informations")
        # Si le mot de passe ne correspond pas, on recommence
        else:
            return render_template("authentification.html",
                                   mdp="mdp incorrect")


# Route pour l'information client
@app.route('/mes-informations', methods=["GET", "POST"])
def info_client():
    username = None
    email = None
    # Si une session existe
    if "id" in session:
            username = get_db().get_fname()
            email = get_db().get_email(session["id"])
    else:
        return render_template('authentification.html',
                               wrongMatricule="fx"), 401

    if request.method == "GET":
        info = get_db().get_info(email)
        if info is None:
            return redirect('/')
        else:
            return render_template("info-client.html", username=username,
                                   email=email,
                                   infos=info)
    else:
        info = get_db().get_info(email)
        username = get_db().get_fname()

        nom = request.form["nom"]
        prenom = request.form["prenom"]
        mdp = request.form["mdp"]
        num_tel = request.form["tel"]
        adresse = request.form["addr"]
        ville = request.form["ville"]
        cp = request.form["CP"]

        db = get_db()
        if nom != "":
            db.modify_name(nom, email)
        if prenom != "":
            db.modify_fname(prenom, email)
        if num_tel != "":
            db.modify_num(prenom, email)
        if adresse != "":
            db.modify_addr(adresse, email)
        if ville != "":
            db.modify_ville(ville, email)
        if mdp != "":
            db.modify_mdp(mdp, email)
        if cp != "":
            regex_cp = r'[A-Za-z0-9]{6}'
            if re.match(regex_cp, cp) is None:
                return render_template("info-client.html", wrong="Wrong",
                                       username=username,
                                       infos=info)

            db.modify_cp(cp, email)

        info = get_db().get_info(email)
        username = get_db().get_fname()
        return render_template("info-client.html", modif="OK",
                               username=username,
                               email=email, infos=info)


# Route pour faire adopter un animal
@app.route('/adoption', methods=["GET", "POST"])
def adoption():
    username = None
    email = None
    if "id" in session:
        email = get_db().get_email(session["id"])
        username = get_db().get_fname()
    else:
        return render_template('authentification.html',
                               wrongMatricule="fx"), 401

    if request.method == "GET":
            return render_template("adoption.html", username=username)
    else:
        nom_animal = request.form["nom_animal"]
        type_animal = request.form["type_animal"]
        race = request.form["race"]
        age = request.form["age"]
        description = request.form["description"]
        addr = request.form["adresse"]

        # Si des champs sont vides
        if (nom_animal == "" or type_animal == "" or race == "" or age == ""
           or description == "" or addr == ""):
            return render_template("adoption.html", error="obligatoires")

        image = None
        image_id = None
        if "photo" in request.files:
            image = request.files["photo"]
            image_id = str(uuid.uuid4().hex)

        db = get_db()
        db.insert_animal(nom_animal, type_animal, race,
                         age, email, description, addr, image_id)
        if image_id is not None:
            db.insert_animal_photo(image_id, image)

        return redirect("/ok")


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
           or num_tel == "" or adresse == "" or ville == "" or cp == ""):
            return render_template("inscription.html",
                                   error="Tous les champs sont obligatoires.")
        elif re.match(regex_cp, cp) is None:
            return render_template("inscription.html", wrong="Wrong")

        if (verification_email == email):
            return render_template("inscription.html",
                                   email="mail existe deja")

        db.create_user(nom, prenom, email, mdp, num_tel, adresse, ville, cp)

        return redirect("/confirmation")


# Route qui confirme l'inscription d'un utilisateur
@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")


# Route qui confirme l'espace de creation d'adoption
@app.route('/ok')
def confirmation_animal():
    return render_template("conf-animal.html")


# Route qui confirme l'espace de creation d'adoption
@app.route('/reinit')
def confirmation_pwd():
    return render_template("conf-pwd.html")


# Route qui confirme l'espace de creation d'adoption
@app.route('/expire')
def expire():
    return render_template("lien-out.html")


# Route pour modifier son mot de passe
@app.route('/reset', methods=["GET", "POST"])
def reinitialisation():
    if request.method == "GET":
        return render_template("reinit.html")
    else:
        email = request.form["email"]

        # On se connecte a la base de donnees
        db = get_db()
        verification_email = db.verification_email_existant(email)

        if (verification_email != email):
            return render_template("reinit.html",
                                   mail="mail n'existe pas")

        # On cree un unique token au hasard
        unique_token = str(uuid.uuid4())
        # On decide quand est-ce que cette cle sera expire
        expiration = (datetime.datetime.utcnow() +
                      datetime.timedelta(days=0,
                                         seconds=1800))
        exp = str(expiration.hour) + ":" + str(expiration.minute)
        hour = datetime.datetime.utcnow()
        now = str(hour.hour) + ":" + str(hour.minute)

        db.single_token(email, exp, unique_token)

        corps = ("Cliquez sur le lien pour réinitialiser votre mot de"
                 " passe : http://localhost:5000/reset/%s" % (unique_token))
        msg = Email(email, corps).send_msg(email, corps)

        return redirect('/reinit')


@app.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    token_exist = None
    email = None
    db = get_db()
    token_exist = db.find_token(token)

    if request.method == "GET":

        # Si la cle existe
        if token_exist is not None:
            daa = datetime.datetime.utcnow()
            now = str(daa.hour) + ":" + str(daa.minute)
            exp = token_exist[1]
            hour_exp = exp.split(':')
            hour_now = now.split(':')

            if hour_exp[0] == '23' and hour_now[0] == '0':
                return redirect('/expire')
            elif hour_exp[0] < hour_now[0]:
                return redirect('/expire')
            elif hour_exp[0] == hour_now[0]:
                if hour_exp[1] < hour_now[1]:
                    return redirect('/expire')

            return render_template("new-pwd.html")
        # Si la cle n'existe pas
        else:
            return redirect('/expire')

    else:
        email = token_exist[0]
        mdp = request.form["password"]
        db.modify_mdp(self, mdp, email)

        return render_template("lien-out.html", mdp=mdp)


@app.route('/<id>')
def page_animal(id):
    username = None
    email = None
    if "id" in session:
        username = get_db().get_fname()

    page = get_db().get_animal_by_id(id)
    if page is None:
        return render_template(("404.html"))
    else:
        animal = Animal(page[0], page[1], page[2],
                        page[3], page[4], page[5], page[6], page[7], page[8])
        return render_template(("animal.html"),
                               id=id, animal=animal, username=username)


@app.route('/image/<id_image>.png')
def photo(id_image):
    db = get_db()
    binary_data = db.load_picture(id_image)
    if binary_data is None:
        return Response(status=404)
    else:
        response = make_response(binary_data)
        response.headers.set('Content-Type', 'image/png')
    return response


@app.route('/cinq-animaux/<recherche>')
def cinq_animaux(recherche):
    username = None
    if "id" in session:
        username = get_db().get_fname()

    animaux_raw = get_db().get_recherche(recherche)
    animaux = Animal.init_list(animaux_raw)
    return render_template('cinq-animaux.html', animaux=animaux,
                           username=username)


# Route pour l'application API
@app.route('/api/animals/', methods=["GET"])
def liste_animaux():
    if request.method == "GET":
        animals = get_db().get_animals()
        data = [{"nom": each[1], "type":each[2], "race":each[3],
                 "age":each[4], "description":each[5], "mail_proprio":each[6],
                 "adresse": each[7], "_id": each[0]} for each in animals]
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
