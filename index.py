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
from .date import *
import re
import calendar

app = Flask(__name__, static_folder="static")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


# Fonction qui permet d'eviter de repeter les mois
def liste_mois(liste_mois):
    liste = []
    for matricule in liste_mois:
        annee, mois, jour = matricule.split("-")
        date = annee + "-" + mois
        if (date in liste) is False:
            liste.append(date)
    return liste


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
    matricule = request.form["matricule"]
    regex = r'[A-Z]{3}-[0-9]{2}'
    # Si le champs de matricule est vide, on le renvoit au formulaire
    if matricule == "":
        return render_template("form-index.html", error="Matricule needed")
    elif re.match(regex, matricule) is None:
        return render_template("form-index.html", wrong="Wrong")
    else:
        # On prend la date d'aujourd'hui
        today = get_date(get_today())
        # On essaye d'acceder a la BD
        db = get_db()
        id_matricule = db.get_matricule(matricule)
        if id_matricule is None:
            return render_template('form-index.html', wrongMatricule="fx"), 404
        response = make_response(
            redirect(url_for('calendrier_jour',
                             matricule=id_matricule, date_du_jour=today)))
        response.set_cookie('user_matricule', matricule)
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
    user_matricule = request.cookies.get('user_matricule')
    code_de_projet = request.form["code_de_projet"]
    duree = request.form["duree"]
    if len(code_de_projet) == 0:
        if int(duree) < 1:
            return render_template(
                "calendrier-jour.html", error="Mettre des champs corrects",
                user_matricule=user_matricule, today=date_du_jour)
    else:
        get_db().insert_heures(user_matricule,
                               date_du_jour, code_de_projet, duree)
        response = make_response(
            redirect(url_for('calendrier_jour',
                             matricule=matricule, date_du_jour=date_du_jour)))
        return response


# Supprime un projet existant
@app.route('/supprimer_projet/<matricule>/<date_du_jour>')
def form_projet(matricule, date_du_jour):
    user_matricule = request.cookies.get("user_matricule")
    mois = date_separate(date_du_jour)[1]
    db = get_db()
    code = db.get_code_projet_form(user_matricule, date_du_jour)
    elems = db.get_duree(user_matricule, date_du_jour)
    return render_template("suppression.html", user_matricule=user_matricule,
                           today=date_du_jour, code=code,
                           mois_nom=year[int(mois)-1],
                           mois=date_separate(date_du_jour)[1],
                           mois_annee=date_separate(date_du_jour)[3],
                           elements=elems)


# Redirige l'user lorsque la suppression est faite
@app.route('/supprimer/<matricule>/<date_du_jour>', methods=["POST"])
def suppression(matricule, date_du_jour):
    user_matricule = request.cookies.get('user_matricule')
    code_de_projet = request.form["code_projet"]
    db = get_db()
    db.delete_projet(user_matricule, code_de_projet, date_du_jour)
    response = make_response(
            redirect(url_for('calendrier_jour',
                             matricule=user_matricule,
                             date_du_jour=date_du_jour)))
    return response


# Affiche le jour, les projets et les heures associées
@app.route('/<matricule>/<date_du_jour>')
def calendrier_jour(matricule, date_du_jour):
    user_matricule = request.cookies.get('user_matricule')
    mois = date_separate(date_du_jour)[1]
    previous_day = get_yesterday(date_du_jour)
    next_day = get_tomorrow(date_du_jour)
    db = get_db()
    elems = db.get_duree(user_matricule, date_du_jour)
    if elems is None:
        return render_template(
            "calendrier-jour.html", no_elem="no elem",
            user_matricule=user_matricule,
            mois=date_separate(date_du_jour)[1],
            mois_annee=date_separate(date_du_jour)[3],
            today=date_du_jour,
            mois_nom=year[int(mois)-1],
            previous=previous_day,
            next=next_day)
    elif user_matricule is None:
        return render_template("calendrier-jour.html",
                               no_matricule="no Matricule")
    else:
        return render_template("calendrier-jour.html",
                               elem="element existant",
                               user_matricule=user_matricule,
                               mois=date_separate(date_du_jour)[1],
                               mois_annee=date_separate(date_du_jour)[3],
                               today=date_du_jour,
                               mois_nom=year[int(mois)-1],
                               elements=elems,
                               previous=previous_day,
                               next=next_day)


# Affiche le calendrier du mois
@app.route('/<matricule>/overview/<mois>')
def calendrier_mois(matricule, mois):
    cal = calendar.Calendar(firstweekday=6)
    format_mois = int(mois[-2:])
    format_year = int(mois[:4])
    previous_month = get_previous_month(format_year, format_mois)
    next_month = get_next_month(format_year, format_mois)
    iterator = cal.itermonthdays(format_year, format_mois)
    nweek = calendar.monthcalendar(format_year, format_mois)
    a = []
    db = get_db()
    monthdays = []
    for days in iterator:
        monthdays.append(days)
    for x in range(0, len(monthdays)):
        data = db.get_heures_totales(matricule,
                                     to_date(format_year,
                                             format_mois,
                                             monthdays[x]))
        if monthdays[x] != 0:
            a.append(data[0])
    return render_template('calendrier-mois.html', user_matricule=matricule,
                           mois_nom=year[format_mois-1], mois=mois,
                           annee=format_year, total_heures=a,
                           weeks=nweek, nweek=len(nweek),
                           previous=previous_month, next=next_month)


# Affiche la liste des mois ou il y a des heures
@app.route('/<matricule>')
def matricule_page(matricule):
    user_matricule = request.cookies.get('user_matricule')
    liste_mois_total = get_db().get_liste_mois(matricule)
    nb_element = len(liste_mois_total)
    mois = current_month
    today = get_date(get_today())
    dates = datetime.datetime.strptime(today, "%Y-%m-%d")
    mois_total = liste_mois(liste_mois_total)
    if liste_mois_total is None:
        return render_template('form-index.html'), 404
    else:
        response = make_response(render_template('matricule.html',
                                                 liste_mois=mois_total,
                                                 matricule=matricule,
                                                 mois=mois,
                                                 mois_nom=year[int(mois)-1]))
        response.set_cookie("matricule_actuel", matricule)
        return response


# La page 404.html en cas d'erreur
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
