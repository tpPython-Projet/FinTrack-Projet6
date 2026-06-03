"""
main.py
Projet : FinTrack - Moniteur de Budget Personnel
Bloc 4, 5 & 6 : Persistance, Qualité et Interface
Description : Menu principal, point d'entrée de l'application FinTrack
Auteurs : HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
Date : 25/04/2026

"""

import sys
import os
from datetime import date as Date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gestionnaire import GestionnaireFinancier
from src.couleurs import (
    VERT, ROUGE, JAUNE, BLEU, BLANC, GRAS, RESET,
    COULEURS_CATEGORIES, ICONES_CATEGORIES, OK, ERREUR,
    ALERTE, INFO, SEP_EPAIS, SEP_FIN, SEP_TITRE, SEP_BAS

)


# Fonctions utilitaires

def formater_montant(montant):
    """
    Formate un montat avec un séparateur de milliers.
    Exemple : 5500.0 ---> "5 500 FCFA"
    """
    return f"{montant:,.0f}".replace(",", " ") + " FCFA"

def barre_progression(pourcentage, largeur=20):
    """
    Génère une barre de progression ASCII.
    Exemple : [████████░░░░░░░░░░░░] 40%
    """
    rempli = int((pourcentage/100)*largeur)
    rempli = min(rempli, largeur)
    barre = "█" * rempli + "░" * (largeur - rempli)
    if pourcentage >= 100:
        couleur = ROUGE
    elif pourcentage >= 80:
        couleur = JAUNE
    else: 
        couleur = VERT
    return f"{couleur}[{barre}] {pourcentage:.1f}%{RESET}"


def saisir_montant(message):
    """
    Demande un montant à l'utilisateur et valide la saisie.
    Redemande tant que la saisie n'est pas un nombre valide.
    """
    while True:
        try:
            valeur = float(input(message).strip())
            if valeur <= 0:
                print(f"{ERREUR} Le montant doit etre spérieur à zéro.")
                continue
            return valeur
        except ValueError:
            print(f"{ERREUR} Montant invalide. Entrez un nombre.")


def saisir_description():
    """
    Demande une description avec limite de 50 caractères.
    Affiche un compteur en temps réel.
    """
    while True:
        desc = input("Description (max 50 caractères) : ").strip()
        if not desc:
            print(f"{ERREUR} La description ne peut pas etre vide.")  
            continue
        if len(desc) > 50:
            print(f"{ERREUR} Trop long ({len(desc)}/50). Raccourcissez.")
            continue
        print(f"{BLEU} ({len(desc)}/50 caractères){RESET}")
        return desc


def saisir_date():
    """
    Propose la date du jour par défaut.
    L'utilisateur peut accepter ou saisir un autre date. 
    """
    aujourd_hui = str(Date.today())
    choix = input(
        f"Date : Aujourd'hui ({aujourd_hui})? (o/n) : "
    ).strip().lower()
    if choix == "o" or choix == "":
        return aujourd_hui
    while True: 
        date = input("Entrez la date (AAAA-MM-JJ) : ").strip()
        if len(date) == 10 and date[4] == "-" and date[7] == "-":
            return date
        print(f"{ERREUR} Format invalide. EXemple : 2026-04-25")

# Menu principal

def afficher_menu(g):
    """Afficher le menu principal avec solde en temps réel."""
    solde= g.calculer_solde()
    couleur_solde = VERT if solde >= 0 else ROUGE

    print("\n" + SEP_TITRE)
    print(BLEU + "||" + GRAS + 
        "     FINTRACK — Moniteur de Budget Personnel     " +
        RESET + BLEU + "||" + RESET)
    
    print(SEP_BAS)
    print(f"  🕐 {Date.today().strftime('%A %d %B %Y')}")
    print(f"  💰 Solde actuel : " 
          f"{couleur_solde}{GRAS}"
          f"{formater_montant(solde)}{RESET}")
    print(SEP_FIN)
    print(f"  {GRAS}1{RESET} ou {GRAS}a{RESET} - Ajouter une transaction")
    print(f"  {GRAS}2{RESET} ou {GRAS}h{RESET} - Consulter l'historique")
    print(f"  {GRAS}3{RESET} ou {GRAS}m{RESET} - Modifier une transaction")
    print(f"  {GRAS}4{RESET} ou {GRAS}s{RESET} - Supprimer une transaction")
    print(f"  {GRAS}5{RESET} ou {GRAS}b{RESET} - Gérer les budgets")
    print(f"  {GRAS}6{RESET} ou {GRAS}r{RESET} - Rechercher une transaction")
    print(f"  {GRAS}7{RESET} ou {GRAS}t{RESET} - Statistiques")
    print(f"  {GRAS}8{RESET} ou {GRAS}k{RESET} - Ajouter un mot-clé")
    print(f"  {GRAS}?{RESET}          - Aide")
    print(f"  {GRAS}0{RESET} ou {GRAS}q{RESET} - Quitter")
    print(SEP_EPAIS)


# Fonctions principales

def afficher_bienvenue(g):
    """Afficher le message de bienvenue personnalisé au démarrage."""
    from src.csv_manager import lire_config
    config = lire_config()
    nom = config["nom"] if config else "utilisateur"
    solde = g.calculer_solde()
    nb = len(g.transactions)
    couleur_solde = VERT if solde >= 0 else ROUGE

    print("\n" + SEP_TITRE)
    print(BLEU + "║" + GRAS + 
           "     FINTRACK - Moniteur de Budget personnel    " +
           RESET + BLEU + "║" + RESET)
    print(SEP_BAS)
    print(f"\n 👋 Bonjour {GRAS}{nom}{RESET} !")
    print(f"\n  📊 Vous avez {GRAS}{nb}{RESET} transaction(s) ce mois.")
    print(f"    💰 Solde actuel : "
          f"{couleur_solde}{GRAS}{formater_montant(solde)}{RESET}")
    print("\n" + SEP_EPAIS)


def afficher_aide():
    """Affiche l'aide contextuelle."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS}  AIDE - FINTRACK{RESET}")
    print(SEP_FIN)
    print(f"  {GRAS}1{RESET} ou {GRAS}a{RESET} - Ajouter une transaction")
    print(f"  {GRAS}2{RESET} ou {GRAS}h{RESET} - Voir l'historique complet") 
    print(f"  {GRAS}3{RESET} ou {GRAS}m{RESET} - Modifier une transaction") 
    print(f"  {GRAS}4{RESET} ou {GRAS}s{RESET} - Supprimer une transaction") 
    print(f"  {GRAS}5{RESET} ou {GRAS}b{RESET} - Gérer les budgets mensuels") 
    print(f"  {GRAS}6{RESET} ou {GRAS}r{RESET} - Rechercher par mot-clé") 
    print(f"  {GRAS}7{RESET} ou {GRAS}t{RESET} - Statistiques et Top 5") 
    print(f"  {GRAS}8{RESET} ou {GRAS}k{RESET} - Ajouter un mot-clé") 
    print(f"  {GRAS}?{RESET}           - Afficher cette aide") 
    print(f"  {GRAS}0{RESET} ou {GRAS}q{RESET} - Quitter l'application")
    print(SEP_EPAIS)


def ajouter_transaction(g):
    """Gère la saisie et l'ajout d'une nouvelle transaction."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS}  AJOUTER UNE TRANSACTION{RESET}")
    print(SEP_FIN)

    # Dépense ou Revenu
    print(f"  {GRAS}1{RESET} - Dépense")
    print(f"  {GRAS}2{RESET} - Revenu")
    while True:
        choix_type = input("Type (1/2) : ").strip()
        if choix_type in ["1", "2"]:
            break
        print(f"{ERREUR} Choisissez 1 (Dépense) ou 2 (Revenu).")
    est_depense = choix_type == "1"

    # Description
    description = saisir_description()

    # Montant 
    montant = saisir_montant("Montant (FCFA) : ")
    if est_depense:
        montant = -montant 

    # Date
    date = saisir_date()

    # Catégorisation automatique
    categorie_auto = g.categoriser(description)
    icone = ICONES_CATEGORIES.get(categorie_auto, "📌")
    couleur = COULEURS_CATEGORIES.get(categorie_auto, BLANC)
    print(f"\n   {INFO} Catégorie détectée : "
          f"{couleur}{icone}  {categorie_auto}{RESET}")
    
    confirmer = input("   Confirmer ? (o/n) : ").strip().lower()
    if confirmer != "o":
        CATEGORIES = (
            "Alimentation", "Transport", "Logement",
            "Santé", "Loisirs", "Education", "Revenu", "Autre"
        )
        print(f"\n{SEP_FIN}")
        for i, cat in enumerate(CATEGORIES, 1):
            icone_cat = ICONES_CATEGORIES.get(cat, "📌")
            print(f"  {GRAS}{i}{RESET}. {icone_cat} {cat}")
        while True:
            try:
                idx = int(input("Votre choix : ")) -1
                if 0 <= idx < len(CATEGORIES):
                    categorie = CATEGORIES[idx]
                    break
                print(f"{ERREUR} Choix invalide.")
            except ValueError:
                print(f"{ERREUR} Entrez un nombre.")
    else:
        categorie = categorie_auto


    # Détection de doublon
    doublons = [t for t in g.transactions
                if t.description.lower() == description.lower()
                and t.date == date]
    
    if doublons:
        print(f"\n{ALERTE} Une transaction similaire existe déjà "
              f"aujourd'hui. Confirmer quand même ? (o/n) : ", end="")
        if input().strip().lower() != "o":
            print(f"{INFO} Ajout annulé.")
            return
        
    t = g.ajouter_transaction(description, montant, categorie, date)
    print(f"\n{OK} Transaction ajoutée : {t}")
    couleur_solde = VERT if g.calculer_solde() >= 0 else ROUGE
    print(f"  💰 Nouveau solde : "
          f"{couleur_solde}{formater_montant(g.calculer_solde())}{RESET}")
    print(SEP_EPAIS)


def consulter_historique(g):
    """Affiche toutes les transactions avec couleurs et icones."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS} HISTORIQUE DES TRANSACTIONS{RESET}")
    print(SEP_FIN)
    
    if not g.transactions:
        print(f"    {INFO} Aucune transaction enregistrée.")
        print(SEP_EPAIS)
        return

    # Résumé du mois en haut
    solde = g.calculer_solde()
    couleur_solde = VERT if solde >= 0 else ROUGE
    print(f"  Solde : {couleur_solde}{GRAS}"
          f"{formater_montant(solde)}{RESET}  |  "
          f"{VERT}Revenus : {formater_montant(g.total_revenus())}{RESET}  |  "
          f"{ROUGE}Dépenses : {formater_montant(g.total_depenses())}{RESET}")
    print(SEP_FIN)

    print(f"  {'ID':<4} {'Date':<12} {'Description':<28} "
          f"{'Catégorie':<14} {'Montant':>14}")
    print(SEP_FIN)

    for t in sorted(g.transactions,
                    key=lambda x: x.date, reverse=True):
        icone = ICONES_CATEGORIES.get(t.categorie, "📌")
        couleur = VERT if t.type_transaction() == "revenu" else ROUGE
        montant_formate = formater_montant(t.montant)
        print(f"  {t.id:<4} {t.date:<12} "
            f"{t.description:<28} "
            f"{icone} {t.categorie:<12} "
            f"{couleur}{montant_formate:>14}{RESET}")
    
    print(SEP_EPAIS)


def modifier_transaction(g):
    """Gère la modification d'une transaction existante."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS} MODIFIER UNE TRANSACTION{RESET}")
    print(SEP_FIN)
    consulter_historique(g)
    if not g.transactions:
        return
    try:
        id_t = int(input("ID de la transaction à modifier : "))
    except ValueError:
        print(f"{ERREUR} L'ID doit etre un nombre entier.")
        return
    
    print(f"  {INFO} Laissez vide pour ne pas modifier le champ.")
    description = input("Nouvelle description : ").strip() or None
    montant_str = input("Nouveau montant : ").strip()
    montant = float(montant_str) if montant_str else None
    date = input("Nouvelle date (AAAA-MM-JJ) : ").strip() or None
    categorie = input("Nouvelle catégorie : ").strip() or None

    if g.modifier_transaction(id_t, description, montant, 
                              categorie, date):
        print(f"\n{OK} Transaction modifiée avec succès.")
    else:
        print(f"\n{ERREUR} Aucune transaction avec l'ID {id_t}.")
    print(SEP_EPAIS)


def supprimer_transaction(g):
    """Gère la suppresssion d'une transaction."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS} SUPPRIMER UNE TRANSACTION{RESET}")
    print(SEP_FIN)
    consulter_historique(g)
    if not g.transactions:
        return
    
    try:
        id_t =int(input("ID de la transaction à supprimer :"))
    except ValueError:
        print(f"{ERREUR} L'ID doit être un nombre entier.")
        return
    
    print(f"\n{ALERTE} Confirmer la suppression de la "
          f"transaction {id_t} ? (o/n) : ", end="")
    if input().strip().lower() == "o":
        if g.supprimer_transaction(id_t):
            print(f"\n{OK} Transaction supprimée.")
            couleur_solde = VERT if g.calculer_solde () >= 0 else ROUGE
            print(f"  💰 Nouveau solde : "
                f"{couleur_solde}"
                f"{formater_montant(g.calculer_solde())}{RESET}")
        else:
            print(f"\n{ERREUR} Aucune transaction avec l'ID {id_t}.")
    else:
        print(f"{INFO} Suppression annulée.")
    print(SEP_EPAIS)

def gerer_budgets(g):
    """Gère l'ajout et la consultation des budgets mensuels."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS}  GESTION DES BUDGETS{RESET}")
    print(SEP_FIN)
    print(f"  {GRAS}1{RESET} - Définir un nouveau budget")
    print(f"  {GRAS}2{RESET} - Connsulter les budgets")
    print(f"  {GRAS}0{RESET} - Retour")
    print(SEP_FIN)

    choix = input("Votre choix : ").strip()

    if choix == "1":
        CATEGORIES = (
            "Alimentation", "Transport", "Logement",
            "Santé", "Loisirs", "Education", "Autre"
        )
        for i, cat in enumerate(CATEGORIES, 1):
            icone = ICONES_CATEGORIES.get(cat, "📌")
            print(f"   {GRAS}{i}{RESET}. {icone} {cat}")
        try:
            idx= int(input("Catégorie : ")) - 1
            categorie = CATEGORIES[idx]
        except (ValueError, IndexError):
            print(f"{ERREUR} Choix invalide.")
            return
        
        plafond = saisir_montant("Plafond mensuel (FCFA) : ")


        # Mois et année par défaut
        mois_actuel = Date.today().strftime("%m")
        annee_actuelle = Date.today().strftime("%Y")
        mois_input = input(
            f"Mois (Entrée pour {mois_actuel}) : "
        ).strip() or mois_actuel
        annee_input = input(
            f"Année (Entrée pour {annee_actuelle}) : "
        ).strip() or annee_actuelle

        g.ajouter_budget(categorie, plafond, mois_input, annee_input)
        print(f"\n{OK} Budget {categorie} défini : "
              f"{formater_montant(plafond)}")

    elif choix == "2":
        if not g.budgets:
            print(f"   {INFO} Aucun budget défini.")
            return
        
        print(f"\n  {'Catégorie':<15} {'Plafond':>12} "
              f"{'Dépensé':>12} {'Restant':>12}")
        print(SEP_FIN)

        for b in g.budgets:
            icone = ICONES_CATEGORIES.get(b.categorie, "📌")
            pct = b.pourcentage_utilisation()
            print(f"  {icone} {b.categorie:<13} "
                  f"{formater_montant(b.plafond):>12} "
                  f"{formater_montant(b.depenses):>12} "
                  f"{formater_montant(b.montant_restant()):>12}")
            print(f"    {barre_progression(pct)}")


            # Projection fin de mois
            from datetime import datetime
            aujourd_hui = datetime.today()
            jours_ecoules = aujourd_hui.day
            jours_mois = 30
            if jours_ecoules > 0:
                projection = (b.depenses /
                              jours_ecoules) * jours_mois
                print(f"    📈 Projection fin de mois : "
                      f"{formater_montant(projection)}")

            if b.est_depasse():
                print(f"    {ALERTE} BUDGET DÉPASSÉ !")
            elif b.alerte_80_pourcent():
                print(f"    {ALERTE} Attention : 80% atteint !")
            print(SEP_EPAIS)

def rechercher_transaction(g):
    """Rechercher des transactions par mot-clé."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS} RECHERCHER UNE TRANSACTION{RESET}")
    print(SEP_FIN)

    mot_cle = input("Mot-clé : ").strip()
    if not mot_cle:
        print(f"{ERREUR} Le mot-clé ne peut pas être vide.")
        return
    
    resultats = g.rechercher(mot_cle)
    if not resultats:
        print(f"   {INFO} Aucune transaction pour '{mot_cle}'.")
        print(SEP_EPAIS)
        return
    
    print(f"\n  {VERT}{len(resultats)} résultat(s){RESET} :")
    print(SEP_FIN)
    for t in resultats:
        icone = ICONES_CATEGORIES.get(t.categorie, "📌")
        couleur = VERT if t.type_transaction() == "revenu" else ROUGE
        print(f"  [{t.id}] {t.date} | {t.description} | "
              f"{icone} {t.categorie} | "
              f"{couleur}{formater_montant(t.montant)}{RESET}")
    print(SEP_EPAIS)


def afficher_statistiques(g):
    """Affiche les statistiques et le Top 5 des dépenses."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS}  STATISTIQUES FINANCIÈRES{RESET}")
    print(SEP_FIN)

    if not g.transactions:
        print(f"   {INFO} Aucune transaction enregistrée.")
        print(SEP_EPAIS)
        return
    
    solde = g.calculer_solde()
    total_dep = g.total_depenses()
    total_rev = g.total_revenus()
    couleur_solde = VERT if solde >= 0 else ROUGE


    print(f"  💰 Solde actuel    : "
          f"{couleur_solde}{GRAS}{formater_montant(solde)}{RESET}")
    print(f"  {VERT}📈 Total revenus   : "
          f"{formater_montant(total_rev)}{RESET}")
    print(f"  {ROUGE}📉 Total dépenses  : "
          f"{formater_montant(total_dep)}{RESET}")

    # Moyenne journalière
    from datetime import datetime
    aujourd_hui = datetime.today().day
    if aujourd_hui > 0 and total_dep > 0:
        moyenne = total_dep / aujourd_hui
        print(f"  📊 Moyenne/jour    : {formater_montant(moyenne)}")

    # Dépenses par catégorie avec barre de progression
    print(f"\n{SEP_FIN}")
    print(f"  {GRAS}Dépenses par catégorie :{RESET}")
    categories = {}
    for t in g.transactions:
        if t.type_transaction() == "depense":
            cat = t.categorie
            categories[cat] = categories.get(cat, 0) + abs(t.montant)

    for cat, montant in sorted(categories.items(),
                               key=lambda x: x[1], reverse=True):
        pct = (montant / total_dep * 100) if total_dep > 0 else 0
        icone = ICONES_CATEGORIES.get(cat, "📌")
        couleur = COULEURS_CATEGORIES.get(cat, BLANC)
        print(f"  {icone} {couleur}{cat:<13}{RESET} "
              f"{formater_montant(montant):>14}  "
              f"{barre_progression(pct, 15)}")

    # Top 5 des dépenses
    print(f"\n{SEP_FIN}")
    print(f"  {GRAS}🏆 Top 5 des dépenses :{RESET}")
    depenses = [t for t in g.transactions
                if t.type_transaction() == "depense"]
    top5 = sorted(depenses, key=lambda x: x.montant)[:5]
    for i, t in enumerate(top5, 1):
        print(f"  {GRAS}{i}.{RESET} {t.description:<28} "
              f"{ROUGE}{formater_montant(abs(t.montant))}{RESET}")
        
    
    # Conseil automatique

    if categories:
        cat_max = max(categories, key=categories.get)
        print(f"\n  {ALERTE} Conseil : Vous dépensez beaucoup"
              f"en {GRAS}{cat_max}{RESET}."
              f"Pensez à réduire cette catégorie.")
    
    print(SEP_EPAIS)


def ajouter_mot_cle(g):
    """Permet d'ajouter un mot-clé à une catégorie."""
    print("\n" + SEP_EPAIS)
    print(f"{BLEU}{GRAS}  AJOUTER UN MOT-CLÉ{RESET}")
    print(SEP_FIN)

    CATEGORIES = (
        "Alimentation", "Transport", "Logement",
        "Santé", "Loisirs", "Éducation", "Autre"
    )
    for i, cat in enumerate(CATEGORIES, 1):
        icone = ICONES_CATEGORIES.get(cat, "📌")
        print(f"  {GRAS}{i}{RESET}. {icone} {cat}")

    try:
        idx = int(input("Catégorie : ")) - 1
        categorie = CATEGORIES[idx]
    except (ValueError, IndexError):
        print(f"{ERREUR} Choix invalide.")
        return
    
    mot = input(f"Nouveau mot-clé pour {categorie}: ").strip().lower()
    if not mot:
        print(f"{ERREUR} Le mot-clé ne peut pas être vide.")
        return
    
    if g.ajouter_mot_cle(categorie, mot):
        print(f"\n{OK} Mot-clé '{mot}' ajouté à {categorie}.")
    else:
        print(f"{ERREUR} Catégorie introuvable.")
    print(SEP_EPAIS)






# Point d'entrée principal

def main():
    """Fonction principale: lance l'application FinTrack."""
    g=GestionnaireFinancier()
    afficher_bienvenue(g)

    while True:
        afficher_menu(g)
        choix = input("Votre choix : ").strip().lower()

        if choix in ["1", "a"]:
            ajouter_transaction(g)
        elif choix in ["2", "h"]:
            consulter_historique(g)
        elif choix in ["3", "m"]:
            modifier_transaction(g)
        elif choix in ["4", "s"]:
            supprimer_transaction(g)
        elif choix in ["5", "b"]:
            gerer_budgets(g)
        elif choix in ["6", "r"]:
            rechercher_transaction(g)
        elif choix in ["7", "t"]:
            afficher_statistiques(g)
        elif choix in ["8", "k"]:
            ajouter_mot_cle(g)
        elif choix in "?":
            afficher_aide()
        elif choix in ["0", "q"]:
            print(f"\n{ALERTE} Voulez-vous vraiment quitter ? "
                  f"(o/n) : ", end="")
            if input().strip().lower() == "o":
                print(f"\n{OK} Merci d'avoir utilisé FinTrack. "
                      f"À bientôt ! 👋")
                break
        else:
            print(f"{ERREUR} Choix invalide. "
                  f"Tapez {GRAS}?{RESET} pour l'aide.")

if __name__ == "__main__":
    main()



    




