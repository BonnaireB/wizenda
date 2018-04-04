class Animal:
    def __init__(self,nom,type,race,age,descrip, emailProprio):
        self.nom = nom
        self.type = type
        self.race = race
        self.age = age
        self.descrip = descrip
        self.email emailProprio

class Personne:
    def __init__(self, nom, prenom, email):
        self.nom = nom
        self.prenom = prenom
        self. email = email

class Utilisateur(Personne):
    def __init__(self, nom, prenom, email, motDePasse):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.motDePasse = motDePasse