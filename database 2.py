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


# Inserer une session courante 
    def save_session(self, id_session, email):
        cursor = self.get_connexion().cursor()
        cursor.execute(("INSERT INTO Sessions(id_session, email) "
                            "VALUES(?, ?)"), (id_session, email))
        self.get_connexion().commit()            


    #def insert_
    def get_animals(self):
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT * FROM Animal"))
        animals = cursor.fetchall()
        if animals is None:
            return None
        else:
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
        format_recherche = recherche.split()
        cursor = self.get_connexion().cursor()
        cursor.execute(("SELECT id, description FROM Animal"))
        pertinent = []
        liste = cursor.fetchall()
        for e in liste :
            points = 0
            for element in format_recherche :
                if element in e[1].split():
                    points = points + 1
            tuple = (e[0],points)
            pertinent.append(tuple)
        pertinent.sort(key=lambda tup: tup[1])
        pertinent.reverse()
        animaux = []
        for n in range(0,5):
            animaux.append(self.get_animal_by_id(pertinent[n][0]))
        return animaux
        

