
class Utilisateur:
    def __init__(self, nom, email, jsonText, objectifs):
        self.nom = nom
        self.email = email
        self.jsonText = jsonText
        self.objectifs = objectifs
    def updateJson(self,new_Text):
        self.jsonText = new_Text
    
    def updateName(self,new_Name):
        self.name = new_Name

class Objectif:
    def __init__(self,titre, duree,freq):
        self.titre = titre
        self.duree = duree
        self.freq = freq
    
    def modifier_titre(self,titre):
        self.titre = titre

    def modifier_duree(self,duree):
        self.duree = duree
    
    def modifier_frequence(self, freq):
        self.freq = freq

#class Evenement:
 #   def __init__(self, description, heure_debut, heure_fin, recurrent, color):
 #       self.description = description
 #       self.heure_debut = heure_debut
 #       self.heure_fin = heure_fin
 #      self.recurrent = recurrent
 #      self.color = color

#  def __init__(self, description, heure_debut, heure_fin):
 #       self.description = description
 #       self.heure_debut = heure_debut
 #       self.heure_fin = heure_fin
 #       self.recurrent = False  
 #      self.color = None


#   def modifier_DescriptionEvenement(self,nouveau_description):
#       self.description = nouveau_description 

#    def modifier_heure_debut(self, heure_debut):
#        self.heure_debut = heure_debut 

#    def modifier_heure_fin(self, heure_fin):
#        self.heure_fin = heure_fin 

#    def modifier_recurrent(self, recurrent):
#        self.recurrent = recurrent
        
#    def modifier_color(self, color):
#        self.color = color
        

#class Agenda:
#    def __init__(self, email):
#        self.email = email
#        self.events = None
        
#    def add_event(self, evenement):
#        self.events.append(evenement)
