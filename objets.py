
class Utilisateur:
    def __init__(self, nom, email, mdp):
        self.nom = nom
        self.email = email
        self.mdp = mdp

class Evenement:
    def __init__(self, description, heure_debut, heure_fin, recurrent, color):
        self.description = description
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.recurrent = recurrent
        self.color = color

class Agenda:
    def __init__(self, email, evenements):
        pass