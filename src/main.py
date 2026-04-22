"""
main.py
Projet : FinTrack - Moniteur de Budget Personnel
Bloc 3 : Architecture POO
Description : Menu principal: point d'entrée de l'application FinTrack
Auteurs : HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date : 22/04/2026
"""
import sys 
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.gestionnaire import GestionnaireFinancier
def afficher_menu():
    """Affiche le menu principal de l'application"""
    print("\n" + "=" * 50)
    print("  FINTRACK - Moniteur de Budget Personnel")
    print("=" * 50)
    print("  1. Ajouter une transaction")
    print("  2. Consulter l'historique")
    print("  3. Modifier une transaction")
    print("  4. Supprimer une transaction")
    print("  5. Gérer les budgets ")
    print("  6. Rechercher une transaction")
    print("  7. Calculer les statistiques")
    print("  0. Quitter")
    print("=" * 50)

def ajouter_transaction(g):
    """Gère la saisie et l'ajout d'une nouvelle transaction."""
    print("\n--- Ajouter une transaction ---")
    description = input("Description : ").strip()
    if not description:
        print("Erreur : la description ne peut pas être vide.")
        return
    try:
        montant = float(input("Montant (négatif pour dépense) : "))
    except ValueError:
        print("Erreur : le montant doit être un nombre.")
        return

    date = input("Date (AAAA-MM-JJ, Entrée pour aujourd'hui) : ").strip()
    if not date:
        date = None
    
    # Catégorisation automatique
    categorie_auto = g.categoriser(description)
    print(f"Catégorie détectée automatiquement : {categorie_auto}")
    confirmer = input("Confirmer cette catégorie ? (o/n) : ").strip().lower()
    if confirmer != "o":
        from src.transaction import Transaction
        CATEGORIES = (
            "Alimentation", "Transport", "Logement",
            "Santé", "Loisirs", "Éducation", "Revenu", "Autre"
        )
        print("Catégories disponibles : ")
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"  {i}. {cat}")
        try:
            choix = int(input("Votre choix : ")) - 1
            categorie = CATEGORIES[choix]
        except (ValueError, IndexError):
            print("Choix invalide. Catégorie 'Autre' assignée.")
            categorie = "Autre"
    else: 
        categorie= categorie_auto 
    t=g.ajouter_transaction(description,montant, categorie, date)
    print(f"Transaction ajoutéé : {t}")
    print(f"Nouveau solde : {g.calculer_solde()} FCFA")

def consulter_historique(g):
    """Affiche toutes les transactions enregistrées."""
    print("\n--- Historique des transactions ---")
    if not g.transactions:
        print("Aucune transaction enregistrée.")
        return
    
    print(f"{'ID':<5} {'Date':<12} {'Description':<30} "
          f"{'Catégorie':<15} {'Montant':>12} {'Type':<10}")
    print("-" * 85)

    for t in sorted(g.transactions,
                key=lambda x: x.date, reverse=True):
        print(f"{t.id:<5} {t.date:<12} {t.description:<30} "
            f"{t.categorie:<15} {t.montant:>12.1f} "
            f"{t.type_transaction():<10}")
        
    print("-" * 85)
    print(f"{'Solde total':<50} {g.calculer_solde():>12.1f} FCFA")
    print(f"{'Total revenus':<50} {g.total_revenus():>12.1f} FCFA")
    print(f"{'Total dépenses':<50} {g.total_depenses():>12.1f} FCFA")


def modifier_transaction(g):
    """Gère la modification d'une transaction existante."""
    print("\n--- Modifier une transaction ---")
    consulter_historique(g)
    if not g.transactions:
        return
    
    try:
        id = int(input("ID de la transaction à modifier : "))
    except ValueError:
        print("Erreur : l'ID doit être un nombre entier.")
        return
    
    print("Laissez vide pour ne pas modifier le champ.")
    description = input("Nouvelle description : ").strip() or None
    montant_str = input("Nouveau montant : ").strip()
    montant = float(montant_str) if montant_str else None
    date = input("Nouvelle date (AAAA-MM-JJ) : ").strip() or None
    categorie = input("Nouvelle catégorie : ").strip() or None
    if g.modifier_transaction(id, description, montant,
                              categorie, date):
        print("Transaction modifiée avec succès.")
    else:
        print(f"Erreur : aucune transaction avec l'ID {id}.")

def supprimer_transaction(g):
    """Gère la suppression d'une transaction."""
    print("\n--- Supprimer une transaction ---")
    consulter_historique(g)
    if not g.transactions:
        return
    
    try:
        id = int(input("ID de la transaction à supprimer : "))
    except ValueError:
        print("Erreur : l'ID doit être un nombre entier.")
        return

    confirmation = input(
        f"Confirmer la suppression de la transaction {id} ? (o/n) : "
    ).strip().lower()

    if confirmation == "o":
        if g.supprimer_transaction(id):
            print("Transaction supprimée.")
            print(f"Nouveau solde : {g.calculer_solde()} FCFA")
        else:
            print(f"Erreur : aucune transaction avec l'ID {id}.")
    else:
        print("Suppression annulée.")
        
def gerer_budgets(g):
    """Gère l'ajout et la consultation des budgets mensuels."""
    print("\n--- Gestion des budgets ---")
    print("  1. Définir un nouveau budget")
    print("  2. Consulter les budgets")
    print("  0. Retour")

    choix = input("Votre choix : ").strip()

    if choix == "1":
        CATEGORIES = (
            "Alimentation", "Transport", "Logement",
            "Santé", "Loisirs", "Éducation", "Autre"
        )
        print("Catégories disponibles :")
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"  {i}. {cat}")
        try:
            idx = int(input("Choisir une catégorie : ")) - 1
            categorie = CATEGORIES[idx]
        except (ValueError, IndexError):
            print("Choix invalide.")
            return

        try:
            plafond= float(input("Budget maximum (FCFA) : "))

        except ValueError:
            print("Erreur : montant invalide.")
            return

        mois = input("Mois (ex: 04) : ").strip()
        annee = input("Année (ex: 2026) : ").strip()

        g.ajouter_budget(categorie, plafond, mois, annee)
        print(f"Budget {categorie} défini : {plafond} FCFA")

    elif choix == "2":
        if not g.budgets:
            print("Aucun budget défini.")
            return
        print(f"\n{'Catégorie':<15} {'Max':>10} "
              f"{'Dépensé':>10} {'Restant':>10} {'%':>8}")
        print("-" * 55)
        for b in g.budgets:
            print(f"{b.categorie:<15} {b.plafond:>10.1f} "
                  f"{b.depenses:>10.1f} "
                  f"{b.montant_restant():>10.1f} "
                  f"{b.pourcentage_utilisation():>7.1f}%")
            if b.est_depasse():
                print(f"  ⚠ ALERTE : Budget {b.categorie} dépassé !")
            elif b.alerte_80_pourcent():
                print(f"  ⚠ ATTENTION : 80% du budget {b.categorie} atteint !")


def rechercher_transaction(g):
    """Recherche des transactions par mot-clé."""
    print("\n--- Rechercher une transaction ---")
    mot_cle = input("Mot-clé à rechercher : ").strip()
    if not mot_cle:
        print("Erreur : le mot-clé ne peut pas être vide.")
        return

    resultats = g.rechercher(mot_cle)
    if not resultats:
        print(f"Aucune transaction trouvée pour '{mot_cle}'.")
        return

    print(f"\n{len(resultats)} résultat(s) trouvé(s) :")
    for t in resultats:
        print(t)

def afficher_statistiques(g):
    """Affiche les statistiques financières du mois."""
    print("\n--- Statistiques financières ---")
    if not g.transactions:
        print("Aucune transaction enregistrée.")
        return
    solde = g.calculer_solde()
    total_dep = g.total_depenses()
    total_rev = g.total_revenus()

    print(f"Solde actuel        : {solde:.1f} FCFA")
    print(f"Total revenus       : {total_rev:.1f} FCFA")
    print(f"Total dépenses      : {total_dep:.1f} FCFA")

    # Dépenses par catégorie
    print("\nDépenses par catégorie :")
    categories = {}
    for t in g.transactions:
        if t.type_transaction() == "depense":
            cat = t.categorie
            categories[cat] = categories.get(cat, 0) + abs(t.montant)
    for cat, montant in sorted(categories.items(),
                               key=lambda x: x[1], reverse=True):
        if total_dep > 0:
            pct = (montant / total_dep) * 100
        else:
            pct = 0
        print(f"  {cat:<15} : {montant:>10.1f} FCFA ({pct:.1f}%)")

def main():
    """Fonction principale — lance l'application FinTrack."""
    print("\nBienvenue sur FinTrack — Moniteur de Budget Personnel")
    g = GestionnaireFinancier()

    while True:
        afficher_menu()
        choix = input("Votre choix : ").strip()
        if choix == "1":
            ajouter_transaction(g)
        elif choix == "2":
            consulter_historique(g)
        elif choix == "3":
            modifier_transaction(g)
        elif choix == "4":
            supprimer_transaction(g)
        elif choix == "5":
            gerer_budgets(g)
        elif choix == "6":
            rechercher_transaction(g)
        elif choix == "7":
            afficher_statistiques(g)
        elif choix == "0":
            print("\nMerci d'avoir utilisé FinTrack. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez choisir entre 0 et 7.")


if __name__ == "__main__":
    main()

    

