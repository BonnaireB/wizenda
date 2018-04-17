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

    def insert_animal1(self,animal):
        insert_animal(animal.nom, animal.type, animal.race, animal.age, animal.email_proprio, animal.descrip)

    def insert_animal(self, nom, type, race, age,email, description):
        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO animal (nom, type"
                       ",race, age,email, description) VALUES (?, ?, ?, ?, ?, ?)"),
                       (nom, date, race, age, email, description))
        self.get_connexion().commit()
    
    def insert_user1(self, usr):
        insert_user(usr.nom, usr.prenom, usr.email, user.motDePasse)

    def insert_user(self, nom, prenom, email, mdp):
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()
        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO utilisateur (nom, prenom"
                       ",email, mdp) VALUES (?, ?, ?, ?)"),
                       (nom, prenom, email, hashed_password))
        self.get_connexion().commit()




# Creer un utilisateur
    def create_user(self, nom, prenom, email, mdp, tel, adresse, ville, cp):
        salt = uuid.uuid4().hex
        hashed_password = hashlib.sha512(str(mdp + salt).encode("utf-8")).hexdigest()

        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO utilisateur (nom, prenom, email, salt, hash,"
                       "num_de_tel, adresse, ville, cp) VALUES (?, ?, ?, ?, ?,"
                       "?, ?, ?, ?)"), (nom, prenom, email, salt,hashed_password, 
                                        tel, adresse, ville, cp,))
        self.get_connexion().commit()

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

# Methode pour obtenir info   
    def get_login(self, email):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT prenom FROM Utilisateur WHERE email=?"),
                       (email,))
        user = cursor.fetchone()
        if user is None:
            return None
        else:
            return user[0]


# Inserer une session courante 
    def save_session(self, id_session, prenom, email):
        cursor = self.get_connexion()
        cursor.execute(("INSERT INTO Sessions(id_session, prenom, email) VALUES(?, ?, ?)"), (id_session, prenom, email))
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
        cursor.execute(("SELECT prenom FROM Sessions where id_session=?"),
                       (id_session,))
        prenom = cursor.fetchone()
        if prenom is None:
            return None
        else:
            return prenom[0]


    #def insert_

    def get_animals(self):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT * FROM Animal"))

        animals = cursor.fetchall()
        return animals
    
    def get_animal_by_id(self,id):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT * FROM Animal WHERE id=?"),(id,))
        animal = cursor.fetchone()
        if animal is None:
            return None
        else:
            return animal
        return animals
    
    def get_recherche(self, recherche):
        format_recherche = recherche.lower().split()
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT id, description,type_animal, race FROM Animal"))
        pertinent = []
        liste = cursor.fetchall()
        for e in liste :
            points = 0
            for element in format_recherche :
                identificateurs = e[1].lower().split()+e[2].lower().split()+e[3].lower().split()
                if element in identificateurs:
                    points = points + 1
            tuple = (e[0],points)
            pertinent.append(tuple)
        animaux = []
        for animal in pertinent:
            if animal[1] >= 1:
                animaux.append(self.get_animal_by_id(animal[0]))
        return animaux
        

