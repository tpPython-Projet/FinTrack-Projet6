"""
============================================================================
fondations.py 
Projet : FinTrack - Moniteur de Budget Personnel
Bloc2: Workflow et Fondations 
Description : Démonstration des types de données complexes Python
                 utilisés dans le projet FinTrack.
Auteurs: HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin 
Date : 22/04/2026
============================================================================
"""


"""
PARTIE 1 : Type Dict - Représenter une transaction

Un dictionnaire associe des clés nommées à des valeurs. C'est donc le
type de données idéal pour représenter une transaction financière car
chaque champ a un nom précis : on accède à transaction ["montant] plutot
qu'à transaction [3] et c'est plus lisible et moins sujet aux erreurs.

"""
transaction_1={
    "id":1,
    "date":"2026-04-22",
    "description":"Achat de riz au marché Azerkè",
    "montant": -5500.0,
    "categorie":"Alimentation",
    "type":"depense"
}

transaction_2={
    "id":2,
    "date":"2026-04-22",
    "description":"Salaire du mois d'Avril",
    "montant": 75000.0,
    "categorie":"Revenu",
    "type":"revenu"
}

#Pour à un champ en utilisant sa clé
print("=== PARTIE 1 : Dictionnaire ===")
print(f"Description : {transaction_1['description']}")
print(f"Catégorie : {transaction_1['categorie']}")

#Modification d'un champ
transaction_1["montant"] = -6000.0
print(f"Montant modifié : {transaction_1['montant']} FCFA")

"""
PARTIE 2 : Type List : Stocker une collection de transactions 
Une liste est une collection ordonnée et modifiable.
C'est le type idéal pour stocker toutes les transactions chargées
depuis le fichier CSV : on peut l'ordonner, la filtrer, y ajouter ou 
supprimer des éléments facilement.

"""
transactions=[transaction_1, transaction_2]

#Ajout d'une nouvelle transaction
transaction_3={
    "id":3,
    "date": "2026-04-22",
    "description":"Achat carburant Total",
    "montant":-3000.0,
    "categorie":"Transport",
    "type":"depense"
}
transactions.append(transaction_3)
print("\n=== PARTIE 2 : Liste ===")
print(f"Nombre de transactions : {len(transactions)}")

#Parcourir toutes les transactions

for t in transactions:
    print(f"[{t['id']}] {t['description']} : {t['montant']} FCFA")

#Calculer le solde total
solde = sum(t["montant"] for t in transactions)
print(f"Solde total : {solde} FCFA")

#Filtrer uniquement les dépenses 
depenses =[t for t in transactions if t["type"]=="depense"]
print(f"Nombre de dépenses : {len(depenses)}")
#Suppression d'une transaction de la liste
transactions.remove(transaction_3)
print(f"Après suppression : {len(transactions)} transactions restantes.")



"""
PARTIE 3 : Type Tuple : Catégories fixes et protégées

Un tuple est une collection immuable, on ne peut donc pas modifier 
après sa création. C'est le type idéal pour les catégories de FinTrack
car elles doivent rester stables tout au long de l'exécution pour 
éviter qu'une erreur de code les modifie.
"""

CATEGORIES= (
    "Alimentation",
    "Transport",
    "Logement",
    "Santé",
    "Loisirs",
    "Éducation",
    "Revenu",
    "Autre"
)

print("\n=== PARTIE 3 : Tuple ===")
print(f"Catégories disponibles : {CATEGORIES}")
print(f"Nombre de catégories : {len(CATEGORIES)}")

#Vérifier si une catégorie est valide
categorie_saisie ="Transport"
if categorie_saisie in CATEGORIES:
    print(f" '{categorie_saisie}' est une catégorie valide.")
else:
    print(f" '{categorie_saisie}' n'est pas une catégorie valide.")

#Démonstration de l'immuabilité par une tentative de modification du tuple
try:
    CATEGORIES[0] = "Nourriture"
except TypeError as e:
    print(f"Erreur capturée : {e}")
    print("Le tuple protège les catégories contre toute modification accidentelle.")


"""
PARTIE 4 : Démonstration de l'utilisation combinée des types de données complexes et
                Simulation
On combine dict, list et tuple pour simuler les opérations principales de FinTrack : ajout, 
calcul du solde, filtrage par catégorie et vérification de la validité des catégories.
"""
print("\n=== PARTIE 4 : Démonstration combinée ===")

def ajouter_transaction(liste, id, date, description, montant, categorie):
    """
    Ajoute une transaction à la liste après validation de la catégorie.
    La catégorie doit obligatoirement faire partie du tuple CATEGORIES. 
    """
    if categorie not in CATEGORIES:
        print(f"Erreur : '{categorie}' n'est pas une catégorie valide.")
        return
    type_transaction = "depense" if montant < 0 else "revenu"
    transaction= {
        "id": id,
        "date": date,
        "description": description,
        "montant": montant,
        "categorie": categorie,
        "type": type_transaction
    }
    liste.append(transaction)
    print(f"Transaction ajoutée : {description} ({montant} FCFA)")

def calculer_solde(liste):
        """Calcule et retourne le solde de toutes les transactions."""
        return sum(t["montant"] for t in liste)
    
def filtrer_par_categorie(liste, categorie):
        """Retourne uniquement les transactions d'une catégorie donnée."""
        return[ t for t in liste if t["categorie"]==categorie]

def supprimer_transaction(liste,id):
     """Supprime une transaction de la liste par son id."""
     for i, t in enumerate(liste):
          if t["id"]==id:
               supprime= liste.pop(i)
               print(f"Transaction supprimée : {supprime['description']}")
               return True
     print(f"Erreur : Aucune transaction trouvée avec l'id {id}.")
     return False
# Simulation
historique = []
ajouter_transaction(historique, 4, "2026-04-22", "Bourse mensuelle", 50000.0, "Revenu")
ajouter_transaction(historique, 5, "2026-04-22", "Achat cahiers", -2500.0, "Éducation")
ajouter_transaction(historique, 6, "2026-04-22", "Transport zem ", -1500.0, "Transport")
ajouter_transaction(historique, 7, "2026-04-22", "Catégorie invalide", -1000.0, "Inconnu")

print(f"\nSolde actuel : {calculer_solde(historique)} FCFA")
transport= filtrer_par_categorie(historique, "Transport")
print(f"Transactions Transport : {len(transport)}")
for t in transport:
     print(f" - {t['description']} : {t['montant']} FCFA")
supprimer_transaction(historique, 5)
print(f"Solde après suppression : {calculer_solde(historique)} FCFA")

    
