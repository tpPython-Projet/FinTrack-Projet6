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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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
        "scolarite", "formation", "cours", "iut", "up", "releve", "attestation", "formation"
    ],
    "Arts": ["peinture", "dessin", "flyer", "pierre", "artiste", "sculpture", 

    ],
    "Culture & Tourisme":[ "vodoun", "album", "voyage", "découverte", "aventure"

    ],
    "Autre": []
}

class GestionnaireFinancier:
    """
    Moteur central de FinTrack.
    Gère les transactions, les budgets, la catégorisation automatique 
    et les calculs statistiques. Orchestre toutes les interactions entre
    les données et les fonctionnalités de l'application(l'interface utilisateur).
    """
    def __init__(self):
        """
        Initialise le gestionnaire et charge les données depuis les CSV.
        """
        from src.csv_manager import (
            initialiser_csv, lire_transactions,
            lire_budgets, ecrire_journal
        )
        self._transactions = []
        self._budgets = []
        self._prochain_id = 1
        self._mots_cles = MOTS_CLES

        # Initialiser les fichiers CSV s'ils n'existent pas
        initialiser_csv(
            os.path.join(BASE_DIR, "data", "transactions.csv"),
            ["id", "date", "description", "montant", "categorie", "type"]
        )
        initialiser_csv(
            os.path.join(BASE_DIR, "data", "budgets.csv"),
            ["categorie", "plafond", "mois", "annee"]
        )
        initialiser_csv(
            os.path.join(BASE_DIR, "data", "config.csv"),
            ["nom", "devise"]
        )
        initialiser_csv(
            os.path.join(BASE_DIR, "data", "journal.csv"),
            ["horodatage", "action", "details"]
        )

        # Charger les données existantes
        self._charger_transactions()
        self._charger_budgets()
        self._recalculer_depenses_budgets()

        # Enregistrer le démarrage
        ecrire_journal("DEMARRAGE", "Application FinTrack démarrée")

    def _charger_transactions(self):
        """
        Charge les transactions depuis le fichier CSV au démarrage.
        Reconstruit les objets Depense et Revenu depuis les données CSV.
        Gère les erreurs de lecture et de format de donnés.
        """
        from src.csv_manager import lire_transactions
        try:
            donnees = lire_transactions()
            for d in donnees:
                try:
                    if d["type"] == "depense":
                        t = Depense(int(d["id"]), d["description"],
                                    float(d["montant"]), d["categorie"], d["date"])
                    else:
                        t = Revenu(int(d["id"]), d["description"],
                                float(d["montant"]), d["categorie"], d["date"])
                    self._transactions.append(t)
                    if int(d["id"]) >= self._prochain_id:
                        self._prochain_id = int(d["id"]) + 1
                except (ValueError, KeyError) as e:
                    print(f"⚠ Ligne ignorée dans transaction.csv : {e}")
        except Exception as e:
            print(f"⚠ Erreur chargement transactions : {e}")


    def _charger_budgets(self):
        """
        Charge les budgets depuis le fichier CSV au démarrage.
        Reconstruit les objets Budget depuis les données CSV.
        Gère les erreurs de la lecture et de format de données.
        """
        from src.csv_manager import lire_budgets
        try:
            donnees = lire_budgets()
            for d in donnees:
                try:
                    b = Budget(d["categorie"], float(d["plafond"]),
                            d["mois"], d["annee"])
                    self._budgets.append(b)
                except (ValueError, KeyError) as e:
                    print(f"⚠ Ligne ignorée dans budgets.csv : {e}")
        except Exception as e: 
            print(f"⚠ Erreur chargement budgets : {e}")

    def _recalculer_depenses_budgets(self):
        """
        Recalcule les dépenses de chaque budget en fonction
        des transactions chargées depuis le CSV.
        Appelée au démarrage après le chargement des données.
        """

        for b in self._budgets:
            b._depenses = 0.0
            for t in self._transactions:
                if(t.type_transaction() == "depense" and
                        t._categorie == b._categorie and
                        t._date[5:7] == b._mois.zfill(2) and
                        t._date[:4] == b._annee):
                    b._depenses += abs(t._montant)

        
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
        Gère le cas où la description est None ou vide.
        """
        try:
            if not description:
                return "Autre"
            description_lower = description.lower()
            for categorie, mots in self._mots_cles.items():
                for mot in mots:
                    if mot in description_lower:
                        return categorie
            return "Autre"
        except AttributeError:
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
        Sauvegarde automatiquement dans le CSV après ajout.
        Gère les erreurs de type et sauvegarde CSV.
        """
        from src.csv_manager import sauvegarder_transactions, ecrire_journal
        try:
            if categorie is None:
                categorie = self.categoriser(description)
            
            if float(montant) < 0:
                t= Depense(self._prochain_id, description,
                            montant, categorie, date)
            else:
                t= Revenu(self._prochain_id, description,
                            montant, categorie, date)
            
            self._transactions.append(t)
            self._recalculer_depenses_budgets()
            self._prochain_id += 1
            sauvegarder_transactions(self._transactions)
            ecrire_journal("AJOUT",
                        f"Transaction #{t.id} : "
                        f"{t.montant} FCFA - {t.description}")
            return t
        except ValueError as e:
            print(f"⚠ Erreur ajout transaction: {e}")
            return None
    
    def supprimer_transaction(self, id):
        """
        Supprime une transaction par son id.
        Sauvegarde automatiquement après suppression.
        Gère les erreurs du type sur l'id.
        """
        
        from src.csv_manager import (sauvegarder_transactions, 
                                     ecrire_journal, sauvegarder_backup)
        try:
            id=int(id)
            for i, t in enumerate(self._transactions):
                if t._id == id:
                    sauvegarder_backup()
                    self._transactions.pop(i)
                    sauvegarder_transactions(self._transactions)
                    ecrire_journal("SUPPRESSION", 
                                f"Transaction #{id} supprimée !")
                    return True
            return False
        except (ValueError, TypeError) as e:
            print(f"⚠ Erreur suppression : {e}")
            return False
    
    def modifier_transaction(self, id, description=None,
                              montant=None, categorie=None, date=None):
        """
        Modifie les champs d'une transaction existante.
        Sauvegarde automatiquement après modification.
        """

        from src.csv_manager import (sauvegarder_transactions, 
                                     ecrire_journal, sauvegarder_backup)
        try:
            id = int(id)
            for t in self._transactions:
                if t._id == id:
                    sauvegarder_backup()
                    if description:
                        t._description = description
                    if montant is not None:
                        # On conserve le type (revenu/depense)
                        if t.type_transaction() == "revenu":
                            t._montant = abs(float(montant))
                        else:
                            t._montant = -abs(float(montant))
                    if categorie:
                        t._categorie = categorie
                    if date:
                        t._date = date
                    sauvegarder_transactions(self._transactions)
                    ecrire_journal("MODIFICATION", 
                                f"Transactin #{id} modifiée !")
                    return True
            return False
        except (ValueError, TypeError) as e:
            print(f"⚠ Erreur modification: {e}")
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
    
    def filtrer_par_periode(self, date_debut, date_fin):
        """
        Retourne les transactions entre deux dates (incluses).
        Les dates doivent être au format AAAA-MM-JJ. 
        """
        try:
            return [t for t in self._transactions
                    if date_debut <= t._date <= date_fin]
        except Exception as e:
            print(f"⚠ Erreur filtrage période : {e}")
            return []
    
    def rechercher(self, mot_cle):
        """Retourne les transactions dont la description 
           contient le mot-clé donné.
        """
        mot_lower = mot_cle.lower()
        return [t for t in self._transactions 
                if mot_lower in t._description.lower()]
    
    #Budgets

    def ajouter_budget(self, categorie, plafond, mois, annee):
        """
        Crée et ajoute un nouveau budget mensuel à la liste.
        Sauvegarde automatiquement dans le CSV.
        Gère les erreurs de type sur le planfond.
        """
        from src.csv_manager import sauvegarder_budgets, ecrire_journal
        try:
            b= Budget(categorie, plafond, mois, annee)
            self._budgets.append(b)
            sauvegarder_budgets(self._budgets)
            ecrire_journal("BUDGET",
                        f"Budget {categorie} défini : {plafond} FCFA")
            return b
        except (ValueError, TypeError) as e:
            print(f"⚠ Erreur ajout budget : {e}")
            return None
        
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
    

    def exporter_rapport_mensuel(self, mois, annee):
        """
        Exporte un rapport mensuel complet en CSV.
        Contient toutes les transactions du mois, les totaux 
        et le récapitulatif par catégorie.
        """
        from src.csv_manager import ecrire_journal
        import os
        try:
            import csv
            BASE = os.path.dirname(os.path.dirname(
                os.path.abspath(__file__)))
            dossier = os.path.join(BASE, "exports")
            os.makedirs(dossier, exist_ok=True)

            nom_fichier = f"rapport_{mois}_{annee}.csv"
            chemin = os.path.join(dossier, nom_fichier)

            # Filtrer les transactions du mois
            transactions_mois = [
                t for t in self._transactions 
                if t._date[5:7] == mois and t._date[:4] == annee
            ]
            
            with open(chemin, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)

                # En-tete du rapport
                writer.writerow(["RAPPORT MENSUEL FINTRACK"])
                writer.writerow([f"Période : {mois}/{annee}"])
                writer.writerow([])

                # Transactions 

                writer.writerow(["ID", "Date", "Description",
                                  "Catégorie", "Montant", "Type"])
                for t in transactions_mois:
                    writer.writerow([
                        t.id, t._date, t._description,
                        t._categorie, t._montant,
                        t.type_transaction()
                    ])
                writer.writerow([])

                # Totaux
                revenus = sum(t._montant for t in transactions_mois
                              if t.type_transaction() == "revenu")
                depenses = sum(abs(t._montant) for t in transactions_mois
                              if t.type_transaction() == "depense")
                solde = revenus - depenses

                writer.writerow(["TOTAUX"])
                writer.writerow(["Total revenus", revenus])
                writer.writerow(["Total dépenses", depenses])
                writer.writerow(["Solde", solde])
                writer.writerow([])

                # Récapitulatif par catégorie
                writer.writerow(["RÉCAPITULATIF PAR CATÉGORIE"])
                writer.writerow(["Catégorie", "Total dépenses",
                                 "Budget prévu", "Écart"])
                
                categories = {}
                for t in transactions_mois:
                    if t.type_transaction() == "depense":
                        cat = t._categorie
                        categories[cat] = (categories.get(cat, 0)
                                           + abs(t._montant))
                for cat, total in sorted(categories.items(),
                                         key=lambda x: x[1],
                                         reverse=True):
                    budget = self.verifier_budget(cat, mois, annee)
                    plafond = budget.plafond if budget else 0
                    ecart = plafond - total
                    writer.writerow([cat, total, plafond, ecart])

            ecrire_journal("EXPORT", 
                           f"Rapport {mois}/{annee} → {nom_fichier}")
            return chemin
        except Exception as e:
            print(f"⚠ Erreur export rapport : {e}")
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