"""
csv_manager.py
Projet : FinTrack - Moniteur de Budget Personnel
Bloc 4 : Persistance des données
Description : Gestionnaire de la lecture et écriture des fichiers CSV
                (transactions, budgets, config, journal)
Auteurs: HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date: 25/04/2026

"""
import csv
import os
from datetime import datetime
"""
Chemins vers les fichiers de données
On utilise os.path pour que les chemins fonctionnent sur tous les OS
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRANSACTIONS_CSV = os.path.join(BASE_DIR, "data", "transactions.csv")
BUDGETS_CSV = os.path.join(BASE_DIR, "data", "budgets.csv")
CONFIG_CSV = os.path.join(BASE_DIR, "data", "config.csv")
JOURNAL_CSV = os.path.join(BASE_DIR, "data", "journal.csv")


# Gestion des transactions

def initialiser_csv(chemin, entetes):
    """
    Crée un fichier CSV avec ses en-tetes s'il n'existe pas encore.
    Appelée au démarrage pour garantir que tous les fichiers existent.
    """
    if not os.path.exists(chemin):
        with open(chemin,"w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=entetes)
            writer.writeheader()


def lire_transactions(chemin=TRANSACTIONS_CSV):
    """
    Lit toutes les transactions depuis le fichier CSV.
    Retourne une liste de dictionnaires (un par transaction).
    Retourne une liste vide si le fichier est absent ou vide.

    """

    transactions= []
    try:
        with open(chemin, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for ligne in reader:
                ligne["montant"] = float(ligne["montant"])
                ligne["id"] = int(ligne["id"])
                transactions.append(ligne)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erreur lecture transactions : {e}")
    return transactions


def sauvegarder_transactions(transactions, chemin=TRANSACTIONS_CSV):
    """
    Sauvegarde toutes les transactions dans le fichier CSV.
    Ecrase le contenu existant, c'est une sauvegarde complète.
    """

    entetes= ["id", "date", "description", "montant", "categorie", "type"]

    try:
        with open(chemin, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=entetes)
            writer.writeheader()
            for t in transactions:
                writer.writerow(t.to_dict())
    except Execption as e:
        print(f"Erreur sauvegarde transactions : {e}")
        

# Gestion des budgets CSV

def lire_budgets(chemin=BUDGETS_CSV):
    """
    Lit tous les budgets depuis le fichier CSV.
    Retourne une liste de dictonnaire, un par budget.
    Retourne une liste vide si le fichier est absent ou vide.
    """
    budgets = []
    try:
        with open(chemin, "r", newline="", encoding="utf-8") as f:
            reader =csv.DictReader(f)
            for ligne in reader:
                ligne["plafond"] = float(ligne["plafond"])
                budgets.append(ligne)
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"Erreur lecture budgets : {e}")
    return budgets

def sauvegarder_budgets(budgets, chemin=BUDGETS_CSV):
    """
    Sauvegarde tous les budgets dans le fichier CSV.
    Ecrase le contenu existant, sauvegarde complète. 
    """

    entetes= ["categorie", "plafond", "mois", "annee"]
    try:
        with open(chemin, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=entetes)
            writer.writeheader()
            for b in budgets:
                writer.writerow(b.to_dict())
    except Exception as e:
        print(f"Erreur sauvegarde budgets : {e}")


# Gestion du journal d'activité

def ecrire_journal(action, details, chemin=JOURNAL_CSV):
    """
    Enregistre une action dans le journal d'activité.
    Chaque entrée contient l'horodatage, le type d'action et les détails.
    Le journal ne s'effacee jamais, on ajoute toujours à la fin. 

    """

    entetes=["horodatage", "action", "details"]
    fichier_existe = os.path.exists(chemin)
    try:
        with open(chemin, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f,fieldnames=entetes)
            if not fichier_existe:
                writer.writeheader()
            writer.writerow({
                "horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": action,
                "details": details
            })
    except Exception as e:
        print(f"Erreur écriture : {e}")


# Gestion du profil utilisateur

def lire_config(chemin=CONFIG_CSV):
    """
    Lit le profil utilisateur depuis config.csv.
    Retourne un dictionnaire avec nom et devise.
    Retourne None si le fichier est absent.
    """       
    try:
        with open(chemin, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for ligne in reader:
                return ligne
    except FileNotFounderError:
        return None
    except Exception as e: 
        print(f"Erreur lecture config : {e}")
        return None

def sauvegarder_config(nom,devise="FCFA", chemin=CONFIG_CSV):
    """
    Sauvegarde le profil utilisteur dans cette config.csv.
    """

    entetes=["nom", "devise"]
    try:
        with open(chemin, "w", newline="", encoding="utf-8") as f:
            writer =csv.DictWriter(f,fieldnames=entetes)
            writer.writeheader()
            writer.writerow({"nom": nom, "devise":devise})
    except Exception as e : 
        print (f"Erreur sauvegarde confgig:{e} ")


def sauvegarder_backup(chemin=TRANSACTIONS_CSV):
    """Crée une copie de secours avant toute modification."""
    import shutil
    backup = chemin.replace(".csv", "_backup.csv")
    if os.path.exists(chemin):
        shutil.copy2(chemin, backup)

# Test 

if __name__=="__main__":

    # Test initialisation des fichiers
    print("=== Test initialisation CSV ===")
    initialiser_csv(TRANSACTIONS_CSV,
                    ["id", "date", "description", 
                     "montant", "categorie", "type"])
    initialiser_csv(BUDGETS_CSV, 
                    ["categorie", "plafond", "mois", "annee"])
    initialiser_csv(CONFIG_CSV, ["nom", "devise"])
    initialiser_csv(JOURNAL_CSV, 
                    ["horodatage", "action", "details"])
    print("Fichiers CSV initialisés.")

    # Test config
    print("\n=== Test config ===")
    sauvegarder_config("Bliss", "FCFA")
    config = lire_config()
    print(f"Utilisateur : {config['nom']}  | Devise :{config['devise']}")

    
    # Test journal 
    print("\n=== Test journal ===")
    ecrire_journal("TEST", "Vérification du journal d'activité")
    print("Entrée journal écrite.")

    # Test lecture transactions vide
    print("\n=== Test lecture transactions ===")
    transactions = lire_transactions()
    print(f"Transactions lues : {len(transactions)}")