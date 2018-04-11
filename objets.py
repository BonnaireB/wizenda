class Animal:
    def __init__(self, nom, type_animal, race, age, description, email_proprio):
        self.nom = nom
        self.type_animal = type_animal
        self.race = race
        self.age = age
        self.description = description
        self.email_proprio = email_proprio

    def init_list(list):
        liste_animaux = []
        for x in list:
            new = Animal(x[1],x[2],x[3],x[4],x[5],x[6])
            liste_animaux.append(new)
        return liste_animaux
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