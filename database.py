# BONNAIRE BENJAMIN BONB03049706
import sqlite3
# import .objets
import hashlib
import uuid


class Database:
    def __init__(self):
        self.connexion = None

    def get_connexion(self):
        if self.connexion is None:
            self.connexion = sqlite3.connect('./db/tp2.db')
        return self.connexion

    def deconnexion(self):
        if self.connexion is not None:
            self.connexion.close()


    # Creer un utilisateur
    def create_user(self, nom, email, mdp):
        salt = uuid.uuid4().hex
        hashed_password = (hashlib.sha512(str(mdp +
                           salt).encode("utf-8")).hexdigest())

        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO utilisateur (nom, email, salt,"
                        " hash) VALUES (?, "
                        "?, ?, ?)"), (nom, email,
                                                     salt, hashed_password,
                                                    ))
        self.get_connexion().commit()

    # Obtenir le prenom de l'utilisateur
    def get_fname(self):
        cursor = self.get_connexion().cursor()
        cursor.execute("SELECT Utilisateur.nom from Utilisateur CROSS JOIN"
                       " Sessions WHERE Sessions.email = Utilisateur.email")
        nom = cursor.fetchone()
        if nom is None:
            return None
        else:
            return nom[0]

    # Savoir si l'email existe deja dans la base de donnees
    def verification_email_existant(self, email):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT email "
                        "FROM utilisateur WHERE email = ?"), (email,))
        mail = cursor.fetchone()
        if mail is None:
            return None
        else:
            return mail[0]

    # Methode pour authentifier un utilisateur existant
    def get_login_info(self, email):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT salt, hash FROM utilisateur WHERE email=?"),
                       (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]

    

    # Avoir l'email de la session
    def get_email(self, id_session):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT email FROM Sessions where id_session=?"),
                       (id_session,))
        email = cursor.fetchone()
        if email is None:
            return None
        else:
            return email[0]

    # Pour obtenir toutes les infos de l'utilsateur
    def get_info(self, email):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT *"
                        " FROM Utilisateur WHERE email=?"), (email,))
        user_info = cursor.fetchall()
        if user_info == 0:
            return None
        else:
            return user_info[0]

    # Modifie le nom de l'utilisateur
    def modify_name(self, name, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set nom = ? where email = ?"),
                       (name, email,))
        co.commit()

    # # Modifie le prenom de l'utilisateur
    # def modify_fname(self, fname, email):
    #     co = self.get_connexion()
    #     cursor = co.cursor()
    #     cursor.execute(("UPDATE Utilisateur set prenom = ? where email = ?"),
    #                    (fname, email,))
    #     co.commit()

    # Modifie le numero de l'utilisateur
    def modify_num(self, num, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set num_de_tel = ? where email "
                        "= ?"), (num, email,))
        co.commit()

    # Modifie l'adresse de l'utilisateur
    def modify_addr(self, addr, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set adresse = ? where email = ?"),
                       (addr, email,))
        co.commit()

    # Modifie le cp de l'utilisateur
    def modify_mdp(self, mdp, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur SET hash = ? "
                        "WHERE email = ?"), (mdp, email,))
        co.commit()

    # Inserer une session courante
    def save_session(self, id_session, email):
        cursor = self.get_connexion()
        cursor.execute(("INSERT INTO Sessions(id_session, email) "
                        "VALUES(?, ?)"), (id_session, email,))
        self.get_connexion().commit()

    # Supprime une session
    def delete_session(self, id_session):
        connection = self.get_connexion()
        connection.execute(("DELETE FROM Sessions where id_session=?"),
                           (id_session,))
        connection.commit()

    # Regarde si une session existe deja
    def get_session(self, id_session):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT email FROM Sessions where id_session=?"),
                       (id_session,))
        email = cursor.fetchone()
        if email is None:
            return None
        else:
            return email[0]

    # Ajouter un évenement à un agenda
    def add_obj(self, objectif,id_utilisateur):
        cursor = self.get_connexion()
        print(objectif.titre,"   ", id_utilisateur)
        cursor.execute(("INSERT INTO Objectif(id_utilisateur,titre,duree,frequence)"
                        " VALUES(?,?,?,?) "), (id_utilisateur,objectif.titre, objectif.duree, objectif.freq))
        self.get_connexion().commit()
    #récupère tous les objectifs associés a un utilisateur
    def get_obj(self,id_utilisateur):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT * from Objectif WHERE id_utilisateur=?"),(id_utilisateur,))
        objectifs = cursor.fetchall()
        if  len(objectifs) == 0 :
            return None
        else:
            return objectifs

    # supprimer un objectif
    def supp_obj(self, titre,id_utilisateur):
        cursor = self.get_connexion()
        cursor.execute(("DELETE FROM Objectif where id_utilisateur = ? AND titre =?"), (id_utilisateur,titre))
        cursor.commit()

    # Inserer un token pour reset le mot de passe
    def single_token(self, email, exp, token):
        cursor = self.get_connexion()
        cursor.execute(("INSERT INTO Token(email, exp, token) "
                        "VALUES(?, ?, ?)"), (email, exp, token,))
        self.get_connexion().commit()

    def find_token(self, token):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT email, exp FROM token WHERE "
                        "token = ?"), (token,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0], user[1]
    
