"""
transaction.py 
Projet : FinTrack - Moniteur de Budget Personnel
Bloc3: Architecture POO
Description : Définition des classes Transaction, Depense et Revenu
Auteurs: HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date : 22/04/2026

"""
from datetime import date as Date
class Transaction:
    """
    Classe de base représentant une transaction financière financière.
    Encapsule les données d'une opération (dépense ou revenu)
    et fournit les méthodes communes à tous les types de transactions afin 
    d'y accéder et les manipuler.
    """
    def __init__(self, id, description, montant, categorie, date=None):
        """
        Initialise une transaction.
        Les attributs sont protégés ou privés(underscore) et on y accède 
        uniquement ia les propriétés ci-dessous.
        """
        self._id = id
        self._description = description
        self._montant=float(montant)
        self._categorie=categorie
        self._date = date if date else str(Date.today())
        
    #Propriétés (getters)

    @property
    def id(self):
        """Retourne l'identifiant de la transaction."""
        return self._id
    @property
    def description(self):
        """Retourne la description de la transaction."""
        return self._description
    @property 
    def montant(self):
        """Retourne le montant de la transaction."""
        return self._montant
    @property 
    def categorie(self):
        """Retourne la catégorie de la transaction."""
        return self._categorie
    @property
    def date(self):
        """Retourne la date de la transaction."""
        return self._date

    # Setters 

    @description.setter
    def description(self, value):
        """Modifie la description après vérification."""
        if not valeur.strip():
            raise ValueError("La description est vide.")
        self._description = valeur

    @montant.setter
    def montant(self, valeur):
        """Modifie le montant après vérification."""
        self._montant=float(valeur)

    @categorie.setter
    def categorie(self, valeur):
        """Modifie la catégorie"""
        self._categorie = valeur
    @date.setter
    def date(self, valeur):
        """Modifie la date"""
        self._date = valeur

    # Méthodes
    def type_transaction(self):
        """
        Retourne le type de la transaction.
        Méthode surchargée dans les classes enfants Depense et Revenu.
        """
        return "transaction"
    
    def to_dict(self):
        """
        Convertit la transaction en dictionnaire.
        Utilisé pour la sauvegarde dans le fichier CSV.
        """
        return {
            "id": self._id,
            "date": self._date, 
            "description": self._description,
            "montant": self._montant,
            "categorie": self._categorie,
            "type": self.type_transaction()
        }
    def __str__(self):
        """Affichage lisible d'une transaction."""
        return (f"[{self._id}] {self._date} | {self._description} "
                f"| {self._montant} FCFA | {self._categorie}")

class Depense(Transaction):
    """
    Classe représentant une dépense.
    Hérite de Transaction. Le montant est toujours négatif
    car une dépense diminue le solde.
    """

    def __init__(self, id, description, montant, categorie, date=None):
        """
        Initialise une dépense.
        Force le montant à etre négatif(une dépense ne peut pas avoir 
        un montant positif).
        
        """
        montant_negatif = -abs(float(montant))
        super().__init__(id, description, montant_negatif, categorie, date)
    
    def type_transaction(self):
        """Retourne le type 'depense'."""
        return "depense"

class Revenu(Transaction):
    """
    Classe représentant un revenu.
    Hérite de Transaction. Le montant est toujours positif
    car un revenu augmente le solde.
    """

    def __init__(self, id, description, montant, categorie, date=None):
        """
        Initialise un revenu.
        Force le montant à etre positif(un revenu ne peut pas avoir
         un montant négatif).

        """
        montant_positif=abs(float(montant))
        super().__init__(id, description, montant_positif, categorie, date)
        
    def type_transaction(self):
        """Retourne le type 'revenu'."""
        return "revenu"

#Test 

if __name__ == "__main__":

    # Test classe Depense

    d=Depense(1, "Achat riz marché Azerkè", 5500, "Alimentation")
    print(d)
    print(f"Type : {d.type_transaction()}")
    print(f"Montant :{d.montant}FCFA")

    
    # Test classe Revenu
    
    r=Revenu(1, "Salaire du mois d'Avril", 75000, "Revenu")
    print(r)
    print(f"Type : {r.type_transaction()}")
    print(f"Montant :{r.montant}FCFA")

    # Test to_dict()
    print("\n=== Test to_dict() ===")
    print(d.to_dict())
    print(r.to_dict())
