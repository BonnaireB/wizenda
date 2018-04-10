class Animal:
    def __init__(self, nom, type_animal, race, age, description, email_proprio):
        self.nom = nom
        self.type_animal = type_animal
        self.race = race
        self.age = age
        self.description = descrip
        self.email_proprio = email_proprio

class Personne:
    def __init__(self, nom, prenom, email):
        self.nom = nom
        self.prenom = prenom
        self.email = email

class Utilisateur(Personne):
    def __init__(self, nom, prenom, email, mdp):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp