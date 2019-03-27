
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


    def modifier_DescriptionEvenement(self,nouveau_description):
        self.description = nouveau_description 

    def modifier_heure_debut(self, heure_debut):
        self.heure_debut = heure_debut 

    def modifier_heure_fin(self, heure_fin):
        self.heure_fin = heure_fin 

    def modifier_recurrent(self, recurrent):
        self.recurrent = recurrent
        
    def modifier_color(self, color):
        self.color = color
        

class Agenda:
    def __init__(self, email, evenements):
        pass

        # method add event