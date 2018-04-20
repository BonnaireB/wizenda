# PHOUANGSY SOPHIE PHOS06609507
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

    # def insert_animal1(self,animal):
    #   insert_animal(animal.nom, animal.type, animal.race, animal.age, animal.email_proprio, animal.descrip)

    # Ajoute l'animal avec photo
    def insert_animal_photo(self, image_id, image):
        cursor = self.get_connexion()
        cursor.execute("INSERT INTO Image(id, image)"
                       " VALUES (?, ?)", [image_id,
                                          sqlite3.Binary(image.read())])
        cursor.commit()

    # Insere un animal a adopter
    def insert_animal(self, nom, type_animal, race, age, email, description,
                      image_id):
        cursor = self.get_connexion()
        cursor.execute(("INSERT INTO Animal(nom_animal, type_animal,"
                        "race, age, mail_proprio, description, image_id) "
                        "VALUES(?, ?, ?, ?, ?, ?, ?)"), (nom, type_animal,
                                                         race, age, email,
                                                         description,
                                                         image_id))
        cursor.commit()

    # Creer un utilisateur
    def create_user(self, nom, prenom, email, mdp, tel, adresse, ville, cp):
        salt = uuid.uuid4().hex
        hashed_password = (hashlib.sha512(str(mdp +
                           salt).encode("utf-8")).hexdigest())

        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO utilisateur (nom, prenom, email, salt,"
                        " hash, num_de_tel, adresse, ville, cp) VALUES (?, "
                        "?, ?, ?, ?, ?, ?, ?, ?)"), (nom, prenom, email,
                                                     salt, hashed_password,
                                                     tel, adresse, ville,
                                                     cp,))
        self.get_connexion().commit()

    # Obtenir le prenom de l'utilisateur
    def get_fname(self):
        cursor = self.get_connexion().cursor()
        cursor.execute("SELECT Utilisateur.prenom from Utilisateur CROSS JOIN"
                       " Sessions WHERE Sessions.email = Utilisateur.email")
        prenom = cursor.fetchone()
        if prenom is None:
            return None
        else:
            return prenom[0]

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
        cursor.execute(("SELECT nom, prenom, num_de_tel, adresse, ville, cp"
                        " FROM Utilisateur WHERE email=?"), (email,))
        user_info = cursor.fetchall()
        if user_info == 0:
            return None
        else:
            return [(user[0], user[1], user[2], user[3], user[4], user[5])
                    for user in user_info]

    # Modifie le nom de l'utilisateur
    def modify_name(self, name, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set nom = ? where email = ?"),
                       (name, email,))
        co.commit()

    # Modifie le prenom de l'utilisateur
    def modify_fname(self, fname, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set prenom = ? where email = ?"),
                       (fname, email,))
        co.commit()

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

    # Modifie la ville de l'utilisateur
    def modify_ville(self, ville, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set ville = ? where email = ?"),
                       (ville, email,))
        co.commit()

    # Modifie le cp de l'utilisateur
    def modify_cp(self, cp, email):
        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur set cp = ? where email = ?"),
                       (cp, email,))
        co.commit()

    # Modifie le cp de l'utilisateur
    def modify_mdp(self, mdp, email):
        salt = uuid.uuid4().hex
        hashed_password = (hashlib.sha512(str(mdp +
                           salt).encode("utf-8")).hexdigest())

        co = self.get_connexion()
        cursor = co.cursor()
        cursor.execute(("UPDATE Utilisateur SET salt = ? AND hash = ? "
                        "WHERE email = ?"), (salt, hashed_password, email,))
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

    # Charger l'image de l'animal
    def load_picture(self, id_image):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT image FROM Image where id = ?"), (id_image,))
        photo = cursor.fetchone()
        if photo is None:
            return None
        else:
            blob_image = photo[0]
            return photo

    # def insert_

    def get_animals(self):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT * FROM Animal"))
        animals = cursor.fetchall()
        return animals

    def get_latest_id(self):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT id FROM Animal"))
        ids = cursor.fetchall()
        return ids

    def get_animal_by_id(self, id):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT * FROM Animal WHERE id=?"), (id,))
        animal = cursor.fetchone()
        if animal is None:
            return None
        else:
            return animal

    def get_recherche(self, recherche):
        format_recherche = recherche.lower().split()
        cursor = self.get_connexion().cursor()
<<<<<<< HEAD
        cursor.execute(("SELECT id, description,type_animal, race, nom_animal FROM Animal"))
=======
        cursor.execute(("SELECT id, description, type_animal,"
                        "race FROM Animal"))
>>>>>>> 59fc4c92591d88fd885ff0ab0a4866d701caa894
        pertinent = []
        liste = cursor.fetchall()
        for e in liste:
            points = 0
<<<<<<< HEAD
            for element in format_recherche :
                identificateurs = e[1].lower().split()+e[2].lower().split()+e[3].lower().split()+e[4].lower().split()
=======
            for element in format_recherche:
                identificateurs = (e[1].lower().split() +
                                   e[2].lower().split() +
                                   e[3].lower().split())
>>>>>>> 59fc4c92591d88fd885ff0ab0a4866d701caa894
                if element in identificateurs:
                    points = points + 1
            tuple = (e[0], points)
            pertinent.append(tuple)
        animaux = []
        for animal in pertinent:
            if animal[1] >= 1:
                animaux.append(self.get_animal_by_id(animal[0]))
        return animaux
