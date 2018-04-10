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
            self.connexion = sqlite3.connect('./db/tp1.db')
        return self.connexion

    def deconnexion(self):
        if self.connexion is not None:
            self.connexion.close()

    def insert_animal1(self,animal):
        insert_animal(animal.nom, animal.type, animal.race, animal.age, animal.descrip)

    def insert_animal(self, nom, type, race, age, descrip):
        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO animal (nom, type"
                       ",race, age, descrip,photo) VALUES (?, ?, ?, ?, ?, ?)"),
                       (nom, date, race, age, descrip, photo.read()))
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
    
    #def insert_