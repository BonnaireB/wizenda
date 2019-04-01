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
from flask import jsonify
from random import *
from uuid import uuid4

import re
import hashlib
import uuid
import calendar
import datetime


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
    return render_template('accueil.html',username = username)


# Récupère les données de connexion et redirige l'utilisateur a l'index
@app.route('/', methods=["POST"])
def connexion():
    email = request.form["email"]
    mdp = request.form["mot_de_passe"]

    if email == "" or mdp == "":
        return render_template("authentification.html", champs="no")

    # Si le mail n'existe pas
    mail = get_db().get_login_info(email)
    if mail is None:
        return render_template("authentification.html",
                               mail="mail n'existe pas")
        response = make_response(
            redirect(url_for('authentification', mail=mail)))
        return response

    # On verifie si le mail correspond au mot de passe
    salt = mail[0]
    hashed_password = (hashlib.sha512(str(mdp +
                       salt).encode("utf-8")).hexdigest())
    if hashed_password == mail[1]:
        # Accès autorisé
        id_session = uuid.uuid4().hex
        get_db().save_session(id_session, email)
        session["id"] = id_session
        return redirect("/mon-agenda")
        # Si le mot de passe ne correspond pas, on recommence
    else:
        response = make_response(
            redirect(url_for('authentification',
                             mdp="no")))
        return response


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
                               wrongMatricule="faux"), 401

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

        mail = get_db().get_login_info(email)
        if mail is None:
            return render_template("authentification.html",
                                   mail="mail n'existe pas")

        # On verifie si le mail correspond au mot de passe
        salt = mail[0]

        nom = request.form["nom"]
        mdp = request.form["mdp"]

        db = get_db()
        if nom != "":
            db.modify_name(nom, email)
        if mdp != "":
            hashed = (hashlib.sha512(str(mdp +
                           salt).encode("utf-8")).hexdigest())
            db.modify_mdp(hashed, email)

        info = get_db().get_info(email)
        username = get_db().get_fname()
        return render_template("info-client.html", modif="OK",
                               username=username,
                               email=email, infos=info)


# Route pour l'information client
@app.route('/mon-agenda')
def calendrier_user():
    if "id" in session:
        username = get_db().get_fname()
        return render_template("user-calendar.html",
                               username=username)




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
        email = request.form["email"]
        mdp = request.form["mdp"]

        # On se connecte a la base de donnees
        db = get_db()
        verification_email = db.verification_email_existant(email)

        # # regex_cp = r'[A-Za-z0-9]{6}'

        # Si des champs sont vides
        if (nom == "" or email == "" or mdp == ""):
            return render_template("inscription.html",
                                   error="Tous les champs sont obligatoires.")
        

        if (verification_email == email):
            return render_template("inscription.html",
                                   email="mail existe deja")

        db.create_user(nom, email, mdp)

        return redirect("/confirmation")


@app.route('/test')
def test_calendrier():
    if "id" in session:
        username = get_db().get_fname()
        return render_template("tester_calendar.html",username=username)
    else :
        return render_template("tester_calendar.html")
# Route qui confirme l'inscription d'un utilisateur
@app.route('/confirmation')
def confirmation():
    return render_template("confirmation.html")




# Route pour modifier son mot de passe
@app.route('/reinit', methods=["GET", "POST"])
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

        return redirect('/reset_reinit')


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



@app.route('/mail-sent/<mail>')
def mail_sent(mail):
    return render_template('mail-sent.html')



# Route pour l'application API
# @app.route('/api/agenda/', methods=["GET"])
# def agenda():


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
