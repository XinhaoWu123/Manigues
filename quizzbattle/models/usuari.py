from abc import ABC, abstractmethod
class Usuari:
    noms_existents = []

    def __init__(self, nom, edat, correu):
        self._nom = nom
        self._edat = edat
        self._correu = correu
        if nom not in Usuari.noms_existents:
            self._nom = nom
            Usuari.noms_existents.append(nom)
        else:
            print("Aquest nom d'usuari ja existeix")

    def get_nom(self):
        return self._nom

    def set_nom(self, nou_nom):
        self._nom = nou_nom

    def get_edat(self):
        return self._edat
    def set_edat(self, nova_edat):
            self._edat = nova_edat
            
    def get_correu(self):
        return self._correu

    def set_correu(self, nou_correu):
        self._correu = nou_correu

    def __str__(self): return (f"Nom: {self._nom}\n" 
                                f"Edat: {self._edat}\n" 
                                f"Correu: {self._correu}")
        
