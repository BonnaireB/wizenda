
class Utilisateur:
    def __init__(self, nom, email, mdp, jsonText):
        self.nom = nom
        self.email = email
        self.mdp = mdp
        self.jsonText = jsonText
    def updateJson(self,new_Text):
        self.jsonText = new_Text
    
    def updateName(self,new_Name):
        self.name = new_Name

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
