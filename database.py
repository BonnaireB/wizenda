# PHOUANGSY SOPHIE PHOS06609507
# BONNAIRE BENJAMIN BONB03049706
import sqlite3


class Database:
    def __init__(self):
        self.connexion = None

    def get_connexion(self):
        if self.connexion is None:
            self.connexion = sqlite3.connect('./db/tp1.db')
        return self.connexion

    def deconnexion(self):
        if self.connexion is not None:
            self.connexion.close()

    # def get_matricule(self, matricule):
    #     cursor = self.get_connexion().cursor()
    #     cursor.execute(("SELECT matricule "
    #                     "FROM heures WHERE matricule = ?"), (matricule,))
    #     id_matricule = cursor.fetchone()
    #     if id_matricule is None:
    #         return None
    #     else:
    #         return id_matricule[0]

    # def get_age(self, matricule, date):
    #     cursor = self.get_connexion().cursor()
    #     cursor.execute(("SELECT  race,"
    #                     "SUM(age) FROM heures WHERE matricule = ?"
    #                     " AND date_publication = ? GROUP BY race,"
    #                     " date_publication"), (matricule, date,))
    #     liste_age = cursor.fetchall()
    #     taille = len(liste_age)

    #     if taille == 0:
    #         return None
    #     else:
    #         return [(age[0], age[1]) for age in liste_age]

    # def get_code_projet_form(self, matricule, date):
    #     cursor = self.get_connexion().cursor()
    #     cursor.execute(("SELECT DISTINCT race "
    #                    "FROM heures WHERE matricule = ?"
    #                     "AND date_publication = ?"), (matricule, date,))
    #     liste_code_projet = cursor.fetchall()
    #     if liste_code_projet is None:
    #         return None
    #     else:
    #         return [code[0] for code in liste_code_projet]

    # def get_liste_mois(self, matricule):
    #     cursor = self.get_connexion().cursor()
    #     cursor.execute(("SELECT date_publication "
    #                     "FROM heures WHERE matricule = ? "
    #                     "AND age > 0"), (matricule,))
    #     liste_mois = cursor.fetchall()
    #     if liste_mois is None:
    #         return None
    #     else:
    #         return [mois[0] for mois in liste_mois]

    # def get_heures_totales(self, matricule, date):
    #     cursor = self.get_connexion().cursor()
    #     cursor.execute(("SELECT SUM(age) FROM heures WHERE matricule = ?"
    #                    " AND date_publication = ?"), (matricule, date,))
    #     liste_heures_totales = cursor.fetchall()
    #     taille = len(liste_heures_totales)

    #     if taille == 0:
    #         return None
    #     else:
    #         return [heures[0] for heures in liste_heures_totales]

    def insert_animal(self, nom, type, race, age, descrip, photo):
        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO heures (nom, type"
                       ",race, age,descrip,photo) VALUES (?, ?, ?, ?, ?, ?)"),
                       (nom, date, race, age, descrip, photo.read()))
        self.get_connexion().commit()

    def delete_projet(self, matricule, race, date):
        cursor = self.get_connexion().cursor()
        cursor.execute(("DELETE FROM heures WHERE matricule = ? AND "
                       "race = ? AND date_publication = ?"),
                       (matricule, race, date,))
        self.get_connexion().commit()
