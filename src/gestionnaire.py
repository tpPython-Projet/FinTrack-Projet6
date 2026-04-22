"""
gestionnaire.py
Projet : FinTrack - Moniteur de Budget Personnel
Bloc3: Architecture POO
Description : Classe GestionnaireFinancier (moteur central de FinTrack)
                Gère les transactions, budgets et catégorisation automatique.
Auteurs: HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date : 22/04/2026
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.transaction import Transaction, Depense, Revenu
from src.budget import Budget
# =============================================================================
# Dictionnaire de mots-clés pour la catégorisation automatique
# Chaque catégorie est associée à une liste de mots-clés.
# Si un mot de la description d'une dépense correspond à un mot-clé,
# la catégorie est assignée automatiquement.
# =============================================================================

MOTS_CLES = {
    "Alimentation": [
        "riz", "pain", "viande", "poisson", "legume", "huile",
        "marché", "supermarché", "alimentaire", "nourriture",
        "restaurant", "manger", "courses", "azerkè", "fiduciaire"
    ],
    "Transport": [
        "carburant", "essence", "taxi", "zem", "moto", "bus",
        "transport", "voyage", "billet", "total", "station"
    ],
    "Logement": [
        "loyer", "maison", "chambre", "logement", "eau", "electricite",
        "facture", "location", "appartement", "immeuble"
    ],
    "Santé": [
        "medicament", "hopital", "clinique", "sante", "pharmacie",
        "consultation", "medecin", "infirmier", "ordonnance"
    ],
    "Loisirs": [
        "cinema", "sport", "jeu", "loisir", "sortie", "fete",
        "musique", "concert", "voyage", "vacances"
    ],
    "Éducation": [
        "cahier", "stylo", "livre", "ecole", "universite", "frais",
        "scolarite", "formation", "cours", "iut", "parakou"
    ],
    "Autre": []
}

class GestionnaireFinancier:
    """
    Moteur central de FinTrack.
    Gère les transactions, les budgets, la catégorisation automatique 
    et les calsuls statistiques. Orchestre toutes les interactions entre
    les données et les fonctionnalités de l'application(l'interface utilisateur).
    """
    def __init__(self):
        self._transactions=[]
        self._budgets=[]
        self.prochain_id=1
        self._mots_cles = MOTS_CLES

    
    # Propriétés

    @property
    def transactions(self):
        """Retourne la liste des transactions."""
        return self._transactions
    
    @property
    def budgets(self):
        """Retourne la liste de tous les budgets."""
        return self._budgets
    
    #Catégorisation automatique

    def categoriser(self, description):
        """
        Analyse la description d'une transaction et retourne
        automatiquement la catégorie correspondante.
        Si aucun mot-clé ne correspond, retourne "Autre".
        """
        description_lower = description.lower()
        for categorie, mots in self._mots_cles.items():
            for mot in mots:
                if mot in description_lower:
                    return categorie
        return "Autre"
    
    def ajouter_mot_cle(self, categorie, mot):
        """
        Ajout un nouveau mot-clé à une catégorie exixtante.
        Permet à l'utilisateur d'enrichir le dictionnaire.
        """
        if categorie in self._mots_cles:
            self._mots_cles[categorie].append(mot.lower())
            return True
        return False
    
    # Gestion des transactions

    def ajouter_transaction(self, description, montant,
                            categorie=None, date=None):
        """
        Crée et ajoute une nouvelle transaction à la liste.
        Si une catégorie n'est pas fournie, elle est déterminéee 
        automatiquement par la méthode categoriser().
        """
        if categorie is None:
            categorie = self.categoriser(description)
        
        if float(montant) < 0:
            t= Depense(self.prochain_id, description,
                        montant, categorie, date)
        else:
            t= Revenu(self.prochain_id, description,
                        montant, categorie, date)
        
        self._transactions.append(t)
        self.prochain_id += 1
        return t
    
    def supprimer_transaction(self, id):
        """
        Supprime une transaction par son id.
        Retourne True si la transaction a été trouvée et supprimée,
         sinon False.
        """
        for i, t in enumerate(self._transactions):
            if t._id == id:
                self._transactions.pop(i)
                return True
        return False
    
    def modifier_transaction(self, id, description=None,
                              montant=None, categorie=None, date=None):
        """
        Modifie les champs d'une transaction existante.
        Seuls les champs fournis sont modifiés.
        """

        for t in self._transactions:
            if t._id == id:
                if description:
                    t._description = description
                if montant is not None:
                    t._montant = montant
                if categorie:
                    t._categorie = categorie
                if date:
                    t._date = date
                return True
        return False
    
    # Calculs 

    def calculer_solde(self):
        """Calcule et retourne le solde total."""
        return sum(t._montant for t in self._transactions)
    
    def total_depenses(self):
        """Calcule le total de toutes les dépenses en valeur absolue."""
        return sum(abs(t.montant) for t in self._transactions
                    if t.type_transaction() == "depense")

    def total_revenus(self):
        """Calcule le total de tous les revenus."""
        return sum(t.montant for t in self._transactions
                if t.type_transaction() == "revenu")
    # Recherge et filtrage

    def filtrer_par_categorie(self, categorie):
        """Retourne les transactions d'une catégorie donnée."""
        return [t for t in self._transactions 
                if t._categorie == categorie]
    
    def filtrer_par_date(self, date):
        """Retourne les transactions d'une date donnée."""
        return [t for t in self._transactions 
                if t._date == date]
    
    def rechercher(self, mot_cle):
        """Retourne les transactions dont la description 
           contient le mot-clé donné.
        """
        mot_lower = mot_cle.lower()
        return [t for t in self._transactions 
                if mot_lower in t._description.lower()]
    
    #Budgets

    def ajouter_budget(self, categorie, plafond, mois, annee):
        """Crée et ajoute un nouveau budget mensuel à la liste."""
        b= Budget(categorie, plafond, mois, annee)
        self._budgets.append(b)
        return b
    
    def verifier_budget(self, categorie, mois, annee):
        """
        Vérifie l'état du budget d'une catégorie.
        Retourne le bubget correspondant ou None si inexistant.
        """
        for b in self._budgets:
            if (b._categorie == categorie and 
                b._mois == mois and b._annee == annee):
                return b
        return None
    
# Test
if __name__ == "__main__":

    g=GestionnaireFinancier()

    # Test catégorisation automatique
    print("=== Test catégorisation automatique ===")
    print(g.categoriser("Achat riz au marché Azerkè"))
    print(g.categoriser("Achat carburant total"))
    print(g.categoriser("Paiement loyer mensuel"))
    print(g.categoriser("Description inconnue"))

    # Test ajout de transactions 
    print("=== Test ajout transactions ===")
    g.ajouter_transaction("Bourse mensuelle", 50000)
    g.ajouter_transaction("Achat riz marché ", -5500)
    g.ajouter_transaction("Transport zem", -1500)
    g.ajouter_transaction("Achat livre IUT ", -2500)

    for t in g.transactions:
        print(t)

    # Test calculs

    print(f"\nSolde total : {g.calculer_solde()} FCFA")
    print(f"Total dépenses : {g.total_depenses()} FCFA")
    print(f"Total revenus : {g.total_revenus()} FCFA")

    # Test filtrage

    print("\n=== Test filtrage ===")
    transport = g.filtrer_par_categorie("Transport")
    for t in transport:
        print(t)
    
    #Test budget 
    print("\n=== Test budget ===")
    g.ajouter_budget("Alimentation", 30000, "04", "2026")
    b = g.verifier_budget("Alimentation", "04", "2026")
    b.ajouter_depense(5500)
    print(b)
    print(f"Budget dépassé : {b.est_depasse()}")