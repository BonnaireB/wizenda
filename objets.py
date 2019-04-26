
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
