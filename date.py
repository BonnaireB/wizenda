# PHOUANGSY SOPHIE PHOS06609507
# BONNAIRE BENJAMIN BONB03049706
import datetime
import calendar


# Obtenir la date
def get_today():
    now = datetime.datetime.now()
    return now


# Obtenir l'annee
def get_annee(date):
    return date.year


# Obtenir le mois
def get_mois(date):
    return date.month


# Obtenir le jour
def get_jour(date):
    return date.day


# Obtenir la date en entier
def get_date(date):
    now = datetime.datetime.date(date).isoformat()
    return now


# Prend trois paramètre année mois et jour et crèe un chaîne en format iso
def to_date(annee, mois, jour):
    month = str(mois)
    day = str(jour)
    if mois < 10:
        month = "0"+str(mois)
    if int(jour) < 10:
        day = "0"+str(jour)
    retour = str(annee)+"-"+month+"-"+day
    return retour


# Prend une date en format iso, sépare les éléments et renvoie une liste
def date_separate(date):
    annee = date[:4]
    mois = date[5:-3]
    jour = date[-2:]
    return [annee, mois, jour, annee+'-'+mois]


# Prend en paramètre une année et un mois et retourne le mois précédant
def get_previous_month(year, month):
    new_month = int(month) - 1
    new_year = int(year)
    if new_month == 0:
        new_month = 12
        new_year = new_year - 1
    new_date = to_date(new_year, new_month, 1)
    new = date_separate(new_date)[3]

    return new


# Prend en paramètre une année et un mois et retourne le mois suivant
def get_next_month(year, month):
    new_month = int(month) + 1
    new_year = int(year)
    if new_month == 13:
        new_month = 1
        new_year = new_year + 1
    new_date = to_date(new_year, new_month, 1)
    new = date_separate(new_date)[3]
    return new


# Prend en paramètre une date et retourne la date du jour précédant
def get_yesterday(date):
    separee = date_separate(date)
    jour = int(separee[2])
    mois = int(separee[1])
    annee = int(separee[0])
    if jour == 1:
        if mois == 1:
            mois = 12
            annee = annee-1
        mois = mois-1
        jour = calendar.monthrange(annee, mois)[1]
    else:
        jour = jour-1
    return to_date(annee, mois, jour)


# Prend en paramètre une date et retourne la date du jour suivant
def get_tomorrow(date):
    separee = date_separate(date)
    jour = int(separee[2])
    mois = int(separee[1])
    annee = int(separee[0])
    if jour == calendar.monthrange(annee, mois)[1]:
        if mois == 12:
            mois = 0
            annee = annee-1
        mois = mois+1
        jour = 1
    else:
        jour = jour+1
    return to_date(annee, mois, jour)


year = ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet',
        'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
current_month = get_mois(get_today())
current_year = get_annee(get_today())
