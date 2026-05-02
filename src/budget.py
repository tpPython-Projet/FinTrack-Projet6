"""
budget.py
Projet : FinTrack - Moniteur de Budget Personnel
Bloc3: Architecture POO
Description : Définition de la classe Budget
Auteurs: HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date : 22/04/2026

"""
class Budget:
    """
    Classe représentant un budget mensuel pour une catégorie donnée.
    Encapsule le plafond défini par l'utilisateur et calcule le 
    montant restant en fonction des dépenses enregistrées.

    """
    def __init__(self, categorie, plafond, mois, annee):
        """
        Initialise un budget mensuel .
        categorie : la catégorie concernée (ex: Alimentation)
        plafond :  le montant maximum autorisé pour le mois
        mois : le mois concerné (ex: 4 pour Avril)
        annee : l'année concernée (ex: 2026)
        """
        self._categorie = categorie
        self._plafond = float(plafond)
        self._mois = mois
        self._annee = annee
        self._depenses = 0.0
    
    # Propriétés (getters)

    @property
    def categorie(self):
        """Retourne la catégorie du budget."""
        return self._categorie
    
    @property
    def plafond(self):
        """Retourne le plafond mensuel"""
        return self._plafond
    @property
    def mois(self):
        """Retourne le mois du budget."""
        return self._mois

    @property
    def annee(self):
        """Retourne l'année du budget."""
        return self._annee

    @property
    def depenses(self):
        """Retourne le montant total des dépenses."""
        return self._depenses

    # Setters

    @plafond.setter
    def plafond(self, valeur):
        """Modifie le montant du plafond après vérification."""
        if float(valeur) <= 0:
            raise ValueError("Le plafond doit être un nombre positif.")
        self._plafond = float(valeur)
    
    # Méthodes

    def ajouter_depense(self, montant):
        """
        Ajoute une dépense au total actuel.
        Le montant passé doit etre positif puisque la conversion est faite 
        automatiquement dans la classe Transaction.

        """
        self._depenses += abs(float(montant))

    def montant_restant(self):
        """ Calcule et retourne le montant restant dans le budget."""
        return self._plafond - self._depenses
    
    def pourcentage_utilisation(self):
        """
        Calcule le pourcentage d'utilisation du budget.
        Retourne O si le plafond est à O pour éviter une division par zéro.
        """
        if self._plafond == 0:
            return 0.0
        return(self._depenses / self._plafond)*100
    
    def est_depasse(self):
        """Retourne True si les dépenses dépassent le plafond, sinon False."""
        return self._depenses > self._plafond
    
    def alerte_80_pourcent(self):
        """Retourne True si les dépenses atteignent  80% du plafond."""
        return self.pourcentage_utilisation() >= 80
    
    def to_dict(self):
        """
        Convertit le budget en dictionnaire .
        Utilisé pour la sauvegarde dans le fichier CSV.
        """
        return {
            "categorie": self._categorie,
            "plafond": self._plafond,
            "mois": self._mois,
            "annee": self._annee,
        }
    def __str__(self):
        """Affichage lisible du budget."""
        return(f"[Budget {self._categorie}]"
                f" Plafond: {self._plafond} FCFA | "
                f"Dépenses: {self._depenses} FCFA | "
                f"Reste: {self.montant_restant()} FCFA | "
                f"Utilisation: {self.pourcentage_utilisation():.2f}%")


# Test 

if __name__ == "__main__":

    # Création d'un budget Alimentation
    b=Budget("Alimentation", 30000, "04", "2026")
    print(b)

    # Ajout de dépenses
    b.ajouter_depense(5500)
    b.ajouter_depense(8000)
    print(b)
    print(f"Budget dépassé : {b.est_depasse()}")
    print(f"Alerte 80% : {b.alerte_80_pourcent()}")

    # Test dépassement 
    b.ajouter_depense(20000)
    print(b)
    print(f"Budget dépassé : {b.est_depasse()}")
    print(f"Alerte 80% : {b.alerte_80_pourcent()}")

    # Test to_dict()
    print("\n === Test to_dict() ===")
    print(b.to_dict())