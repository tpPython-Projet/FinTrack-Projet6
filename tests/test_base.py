# =============================================================================
# test_base.py
# Projet : FinTrack - Moniteur de Budget Personnel
# Bloc 3 : Architecture POO
# Description : Tests unitaires de base avec Pytest
# Auteurs : HOUSSOU Towanou Bliss Espérance / AMOUSSOU Firmin
# Date : 22/04/2026
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.transaction import Transaction, Depense, Revenu
from src.budget import Budget
from src.gestionnaire import GestionnaireFinancier


def test_depense_montant_negatif():
    d = Depense(1, "Achat riz", 5500, "Alimentation")
    assert d.montant == -5500.0

def test_depense_montant_deja_negatif():
    d = Depense(1, "Achat riz", -5500, "Alimentation")
    assert d.montant == -5500.0

def test_depense_type():
    d = Depense(1, "Achat riz", 5500, "Alimentation")
    assert d.type_transaction() == "depense"

def test_depense_to_dict():
    d = Depense(1, "Achat riz", 5500, "Alimentation", "2026-04-22")
    d_dict = d.to_dict()
    assert d_dict["id"] == 1
    assert d_dict["montant"] == -5500.0
    assert d_dict["type"] == "depense"
    assert d_dict["categorie"] == "Alimentation"

def test_revenu_montant_positif():
    r = Revenu(2, "Salaire", 75000, "Revenu")
    assert r.montant == 75000.0

def test_revenu_type():
    r = Revenu(2, "Salaire", 75000, "Revenu")
    assert r.type_transaction() == "revenu"

def test_budget_montant_restant():
    b = Budget("Alimentation", 30000, "04", "2026")
    b.ajouter_depense(5500)
    assert b.montant_restant() == 24500.0


def test_budget_pourcentage():
    b = Budget("Alimentation", 30000, "04", "2026")
    b.ajouter_depense(15000)
    assert b.pourcentage_utilisation() == 50.0

def test_budget_non_depasse():
    b = Budget("Alimentation", 30000, "04", "2026")
    b.ajouter_depense(20000)
    assert b.est_depasse() == False

def test_budget_depasse():
    b = Budget("Alimentation", 30000, "04", "2026")
    b.ajouter_depense(35000)
    assert b.est_depasse() == True

def test_budget_alerte_80():
    b = Budget("Alimentation", 30000, "04", "2026")
    b.ajouter_depense(24000)
    assert b.alerte_80_pourcent() == True

def test_budget_to_dict():
    b = Budget("Transport", 15000, "04", "2026")
    b_dict = b.to_dict()
    assert b_dict["categorie"] == "Transport"
    assert b_dict["plafond"] == 15000.0

def test_categorisation_alimentation():
    g = GestionnaireFinancier()
    assert g.categoriser("Achat riz marché") == "Alimentation"


def test_categorisation_transport():
    g = GestionnaireFinancier()
    assert g.categoriser("Achat carburant Total") == "Transport"

def test_categorisation_inconnue():
    g = GestionnaireFinancier()
    assert g.categoriser("Description inconnue xyz") == "Autre"

def test_ajouter_transaction_depense():
    g = GestionnaireFinancier()
    t = g.ajouter_transaction("Achat riz", -5500, "Alimentation")
    assert t.type_transaction() == "depense"
    assert t.montant == -5500.0

def test_ajouter_transaction_revenu():
    g = GestionnaireFinancier()
    t = g.ajouter_transaction("Salaire", 75000, "Revenu")
    assert t.type_transaction() == "revenu"
    assert t.montant == 75000.0


def test_calculer_solde():
    g = GestionnaireFinancier()
    g.ajouter_transaction("Salaire", 75000, "Revenu")
    g.ajouter_transaction("Achat riz", -5500, "Alimentation")
    g.ajouter_transaction("Transport zem", -1500, "Transport")
    assert g.calculer_solde() == 68000.0

def test_supprimer_transaction():
    g = GestionnaireFinancier()
    g.ajouter_transaction("Salaire", 75000, "Revenu")
    g.ajouter_transaction("Achat riz", -5500, "Alimentation")
    assert g.supprimer_transaction(1) == True
    assert len(g.transactions) == 1


def test_supprimer_transaction_inexistante():
    g = GestionnaireFinancier()
    assert g.supprimer_transaction(999) == False

def test_filtrer_par_categorie():
    g = GestionnaireFinancier()
    g.ajouter_transaction("Achat riz", -5500, "Alimentation")
    g.ajouter_transaction("Transport zem", -1500, "Transport")
    g.ajouter_transaction("Achat huile", -2000, "Alimentation")
    resultats = g.filtrer_par_categorie("Alimentation")
    assert len(resultats) == 2

def test_ajouter_mot_cle():
    g = GestionnaireFinancier()
    g.ajouter_mot_cle("Alimentation", "fiduciaire")
    assert g.categoriser("Achat fiduciaire") == "Alimentation"