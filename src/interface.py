# ======================================================================
# interface.py 
# Projet : FinTrack - Moniteur de Budget Personnel 
#  Bloc 6 : Interface & Livraison 
# Description : Interface graphique Tkinter - point d'entrée graphique 
# AUteurs : HOUSSOU Towanou Bliss Espérance & AMOUSSOU Firmin 
#  Date : 27/04/2026 
# ======================================================================== 

import sys 
import os
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import date as Date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gestionnaire import GestionnaireFinancier 
from src.csv_manager import lire_config, sauvegarder_config

# -- Couleurs et styles --- 
COULEUR_FOND       = "#1E1E2E"
COULEUR_SURFACE    = "#2A2A3E"
COULEUR_ACCENT     = "#7C3AED"
COULEUR_VERT       = "#10B981"
COULEUR_ROUGE      = "#EF4444"
COULEUR_JAUNE      = "#F59E0B"
COULEUR_TEXTE      = "#E2E8F0"
COULEUR_TEXTE_GRIS = "#94A3B8"
POLICE_TITRE       = ("Arial", 14, "bold")
POLICE_NORMAL      = ("Arial", 11)
POLICE_PETIT       = ("Arial", 9)

class FinTrackApp:
    """
    CLasse principale de l'interface graphique FinTrack.
    Gère la fenêtre principale et tous les ongrets.
    """

    def __init__(self, root):
        """Initialise l'application et la fenêtre principale."""
        self.root = root
        self.root.title("FinTrack - Moniteur de Budget Personnel")
        self.root.geometry("900x650")
        self.root.configure(bg=COULEUR_FOND)
        self.root.resizable(True, True)
        
        #Gestionnaire financier
        self.g = GestionnaireFinancier()

        #Charger le profil utilisateur
        config = lire_config()
        if config and config.get("nom"):
            self.nom_utilisateur = config["nom"]
        else:
            self.nom_utilisateur = simpledialog.askstring(
                "Bienvenue sur FinTrack",
                "Entrez votre prénom :",
                initialvalue="Utilisateur"                 
            ) or "Utilisateur"
            sauvegarder_config(self.nom_utilisateur, "FCFA")
        
        #configurer le style ttk
        self._configurer_style()

        #Construire l'interface
        self._construire_header()
        self._construire_onglets()

        #Rafraîchir l'affichage
        self.rafraichir()

    def _configurer_style(self):
        """Configure le style vituel des widgets ttk."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TNotebook", background=COULEUR_FOND, 
                        borderwidth=0)
        style.configure("TNotebook.Tab", background=COULEUR_SURFACE,
                        foreground=COULEUR_TEXTE,
                        padding=[15, 8],
                        font=POLICE_NORMAL)

        style.map("TNotebook.Tab",
                        background=[("selected", COULEUR_ACCENT)], foreground=[("selected","white")])
        
        
        style.configure("TFrame",
                        background=COULEUR_FOND)
        style.configure("TLabel",
                        background=COULEUR_FOND, foreground=COULEUR_TEXTE,
                        font=POLICE_NORMAL)
        style.configure("TButton",
                        background=COULEUR_ACCENT, foreground="white",
                        font=POLICE_NORMAL,
                        padding=[10, 6],
                        borderwidth=0)
        style.map("TButton", 
                  background=[("active",
                  "#6D28D9")])
        style.configure("Treeview",
                        background=COULEUR_SURFACE,
                        foreground=COULEUR_TEXTE,
                        fieldbackground=COULEUR_SURFACE,font= POLICE_NORMAL,
                        rowheight=30)
        style.configure("Treeview.Heading",
                        background=COULEUR_ACCENT,
                        foreground="white",
                        font=("Arial", 11, "bold"))
        

    def _construire_header(self):
        """Construit l'en_tête avec le titre et tableaude bord."""
        header = tk.Frame(self.root,
        bg=COULEUR_ACCENT,pady=15)
        header.pack(fill="x")

        tk.Label(header,
                text="💰 FinTrack - Moniteur de Budget Personnel",
                font=("Arial", 16, "bold"),
                bg=COULEUR_ACCENT,
                fg="white").pack()
        # Tableau de bord
        dashboard = tk.Frame(self.root,
        bg=COULEUR_SURFACE, pady=10)
        dashboard.pack(fill="x", padx=0)

        # Solde
        self.lbl_solde = tk.Label(dashboard,
                                            text="Solde : 0 FCFA",
                                            font=("Arial",
                                            13,
                                            "bold"),bg=COULEUR_SURFACE,
                                            fg=COULEUR_VERT )
        self.lbl_solde.pack(side="left", padx=20)

        #Revenus
        self.lbl_revenus = tk.Label(dashboard,
                                                text="📈 Revenus : 0 FCFA ",
                                                font=POLICE_NORMAL,
                                                bg=COULEUR_SURFACE,
                                                fg=COULEUR_VERT)
        self.lbl_revenus.pack(side="left",padx=20)

        #Dépenses
        self.lbl_depenses = tk.Label(dashboard,
                                                text="📉 Dépenses : 0 FCFA",
                                                font=POLICE_NORMAL,
                                                bg=COULEUR_SURFACE,
                                            fg=COULEUR_ROUGE )  
        self.lbl_depenses.pack(side="left",padx=20)

        # Date
        tk.Label(dashboard,
                            text=f"🗓 {Date.today().strftime('%d/%m/%Y')}",
                            font= POLICE_NORMAL,
                            bg=COULEUR_SURFACE,
                            fg=COULEUR_TEXTE_GRIS).pack(side="right",padx=20)

        # Bienvenue                  
        tk.Label(dashboard,
                            text=f"👋 {self.nom_utilisateur}",
                            font= ("Arial", 11, "bold"),
                            bg=COULEUR_SURFACE,
                            fg=COULEUR_TEXTE).pack(side="right",
                            padx=10)
    def _construire_onglets(self):
        """Construit les onglets principaux de l'application."""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        #Onglet Transactions
        self.frame_transactions = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_transactions, text="💳 Transaction" )
        self._construire_onglet_transactions()

        #Onglet Budgets
        self.frame_budgets = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_budgets,text="🎯 Budgets")
        self._construire_onglet_budgets()

        # Onglet Statistiques
        self.frame_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_stats,text="📊 Statistiques")
        self._construire_onglet_stats()

        #Onglet Recherche
        self.frame_recherche = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_recherche,
                        text="🔍 Recherche")
        self._construire_onglet_recherche()

    def _construire_onglet_transactions(self):
        """Construit l'onglet de gestion des transactions."""
        frame = self.frame_transactions

        # Boutons d'action 
        btn_frame = tk.Frame(frame, bg=COULEUR_FOND, pady=8)
        btn_frame.pack(fill="x", padx=10)
        ttk.Button(btn_frame,
                    text="➕  Ajouter", 
                    command=self.ouvrir_ajout_transaction).pack(
                        side="left", padx=5)
        
        ttk.Button(btn_frame,
                    text="✏️ Modifier", 
                    command=self.modifier_transaction).pack(
                        side="left", padx=5)
        
        ttk.Button(btn_frame,
                    text="🗑️  Supprimer", 
                    command=self.supprimer_transaction).pack(
                        side="left", padx=5)
        ttk.Button(btn_frame,
                    text="🔄 Rafraîchir", 
                    command=self.rafraichir).pack(
                    side="right", padx=5)
        
        #Tableau des transactions
        cols = ("ID", "Date", "Description",
                "Catégorie", "Montant", "Type")
        self.tree_transactions = ttk.Treeview(
            frame, columns=cols, show="headings", height=18)

        for col in cols:
            self.tree_transactions.heading(col, text=col)

        self.tree_transactions.column("ID", width=50, anchor="center")
        self.tree_transactions.column("Date", width=100, anchor="center")
        self.tree_transactions.column("Description", width=250)
        self.tree_transactions.column("Catégorie", width=130)
        self.tree_transactions.column("Montant", width=130, anchor="e")
        self.tree_transactions.column("Type", width=90, anchor="center")

        #Scrollbar
        scrollbar = ttk.Scrollbar(frame,            orient="vertical",         
                            command=self.tree_transactions.yview)
        self.tree_transactions.configure(yscrollcommand=scrollbar.set)




        self.tree_transactions.pack(side="left", fill="both",
                                        expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 10))

        #Tags couleurs
        self.tree_transactions.tag_configure("revenu",foreground=COULEUR_VERT)

        self.tree_transactions.tag_configure("depense",foreground=COULEUR_ROUGE)
    
    def _construire_onglet_budgets(self):
        """Construit l'onglet de gestion des budgets."""
        frame = self.frame_budgets

        #Boutons
        btn_frame = tk.Frame(frame, bg=COULEUR_FOND, pady=8)
        btn_frame.pack(fill="x", padx=10)

        ttk.Button(btn_frame,
                  text="➕ Définir un budget",
                  command=self.ouvrir_ajout_budget).pack(
                    side="left", padx=5)
        ttk.Button(btn_frame,
                  text="🔄 Rafraîchir",
                  command=self.rafraichir).pack(
                    side="right", padx=5)

        # Tableau des budgets
        cols = ("Catégorie", "Plafond", "Dépensé", "Restant", "Utilisation")
        self.tree_budgets = ttk.Treeview(frame,     
            columns=cols, show= "headings", height=15)

        for col in cols:
            self.tree_budgets.heading(col, text=col)

        self.tree_budgets.column("Catégorie", width=150)    
        self.tree_budgets.column("Plafond", width=150, anchor="e")    
        self.tree_budgets.column("Dépensé", width=150, anchor="e")    
        self.tree_budgets.column("Restant", width=150, anchor="e")    
        self.tree_budgets.column("Utilisation", width=150, anchor="center")    
        self.tree_budgets.pack(fill="both", expand=True,
                                 padx=10, pady=5) 

        # Tags couleurs budgets
        self.tree_budgets.tag_configure(
            "ok", foreground =COULEUR_VERT) 
        self.tree_budgets.tag_configure(
            "alerte", foreground =COULEUR_JAUNE) 
        self.tree_budgets.tag_configure(
            "depasse", foreground =COULEUR_ROUGE) 

    def _construire_onglet_stats(self):
        """Construire l'onglet des statatistiques."""
        frame = self.frame_stats

        btn_frame = tk.Frame(frame, bg=COULEUR_FOND, pady=8)
        btn_frame.pack(fill="x", padx = 10)

        ttk.Button(btn_frame,
                  text="🥧 Camembert dépenses",
                   command=self.afficher_camembert).pack(
                       side="left", padx=5)
          
        ttk.Button(btn_frame,
                  text="📊 Histogramme mensuel",
                   command=self.afficher_histogramme).pack(
                       side="left", padx=5)
          
        ttk.Button(btn_frame,
                  text="📈 Évolution solde",
                   command=self.afficher_courbe).pack(
                       side="left", padx=5)
          
        ttk.Button(btn_frame,
                  text="📥 Exporter rapport CSV",
                   command=self.exporter_rapport).pack(
                       side="left", padx=5)
          
        ttk.Button(btn_frame,
                  text="🎯 Budget vs Réel",
                   command=self.afficher_budget_vs_reel).pack(
                       side="left", padx=5)
          
        # Zone statistiques texte
        self.txt_stats = tk.Text(frame,
                                 bg=COULEUR_SURFACE,
                                 fg=COULEUR_TEXTE,
                                 font=POLICE_NORMAL,
                                 padx=15,
                                 pady=15,
                                 wrap="word",
                                 state="disabled")
        self.txt_stats.pack(fill="both", expand=True,
                                    padx=10, pady=5)
                                   
    def _construire_onglet_recherche(self):
        """Construit l'onglet de recherche."""
        frame = self.frame_recherche

        #Barre de recherche
        search_frame = tk.Frame(frame, bg=COULEUR_FOND, pady=10)
        search_frame.pack(fill="x", padx=10)

        tk.Label(search_frame,
                 text="🔍 Mot-clé :",
                 bg=COULEUR_FOND,
                 fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).pack(side="left", padx=5)

        self.entry_recherche = tk.Entry(search_frame,
                                         bg=COULEUR_SURFACE,
                                         fg=COULEUR_TEXTE,
                                         font=POLICE_NORMAL,
                                         width=30,
                                         insertbackground="white")
        self.entry_recherche.pack(side="left", padx=5)


        ttk.Button(search_frame,
                    text="Rechercher",
                    command=self.rechercher).pack(side="left", padx=5)
         # Filtre par période
        periode_frame = tk.Frame(frame, bg=COULEUR_FOND, pady=5)
        periode_frame.pack(fill="x", padx=10)

        tk.Label(periode_frame, text="📅 Du :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).pack(side="left", padx=5)

        self.entry_date_debut = tk.Entry(periode_frame,
                                          bg=COULEUR_SURFACE,
                                          fg=COULEUR_TEXTE,
                                          font=POLICE_NORMAL,
                                          width=12,
                                          insertbackground="white")
        self.entry_date_debut.pack(side="left", padx=5)

        tk.Label(periode_frame, text="Au :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).pack(side="left", padx=5)

        self.entry_date_fin = tk.Entry(periode_frame,
                                        bg=COULEUR_SURFACE,
                                        fg=COULEUR_TEXTE,
                                        font=POLICE_NORMAL,
                                        width=12,
                                        insertbackground="white")
        self.entry_date_fin.pack(side="left", padx=5)

        ttk.Button(periode_frame,
                   text="Filtrer par période",
                   command=self.filtrer_periode).pack(
                       side="left", padx=5)
        
        # Résultats
        cols = ("ID", "Date", "Description",
                "Catégorie", "Montant", "Type")
        self.tree_recherche = ttk.Treeview(
            frame, columns=cols, show="headings", height=18)

        for col in cols:
            self.tree_recherche.heading(col, text=col)

        self.tree_recherche.column("ID", width=50, anchor="center")
        self.tree_recherche.column("Date", width=100, anchor="center")
        self.tree_recherche.column("Description", width=250)
        self.tree_recherche.column("Catégorie", width=130)
        self.tree_recherche.column("Montant", width=130,
                                    anchor="e")
        self.tree_recherche.column("Type", width=90, anchor="center")

        self.tree_recherche.pack(fill="both", expand=True,
                                  padx=10, pady=5)

        self.tree_recherche.tag_configure(
            "revenu", foreground=COULEUR_VERT)
        self.tree_recherche.tag_configure(
            "depense", foreground=COULEUR_ROUGE)
    def rafraichir(self):
        """Rafraîchit tous les affichages."""
        self._maj_dashboard()
        self._maj_transactions()
        self._maj_budgets()
        self._maj_stats()

    def _maj_dashboard(self):
        """Met à jour le tableau de bord."""
        solde = self.g.calculer_solde()
        revenus = self.g.total_revenus()
        depenses = self.g.total_depenses()

        couleur_solde = COULEUR_VERT if solde >= 0 else COULEUR_ROUGE
        self.lbl_solde.config(
            text=f"💰 Solde : {solde:,.0f} FCFA".replace(",", " "),
            fg=couleur_solde)
        self.lbl_revenus.config(
            text=f"📈 Revenus : {revenus:,.0f} FCFA".replace(",", " "))
        self.lbl_depenses.config(
            text=f"📉 Dépenses : {depenses:,.0f} FCFA".replace(",", " "))

    def _maj_transactions(self):
        """Met à jour le tableau des transactions."""
        for item in self.tree_transactions.get_children():
            self.tree_transactions.delete(item)

        for t in sorted(self.g.transactions,
                        key=lambda x: x.date, reverse=True):
            montant = f"{t.montant:,.0f} FCFA".replace(",", " ")
            tag = t.type_transaction()
            self.tree_transactions.insert(
                "", "end",
                values=(t.id, t.date, t.description,
                        t.categorie, montant,
                        t.type_transaction()),
                tags=(tag,))

    def _maj_budgets(self):
        """Met à jour le tableau des budgets."""
        for item in self.tree_budgets.get_children():
            self.tree_budgets.delete(item)

        for b in self.g.budgets:
            pct = b.pourcentage_utilisation()
            if pct >= 100:
                tag = "depasse"
            elif pct >= 80:
                tag = "alerte"
            else:
                tag = "ok"

            self.tree_budgets.insert(
                "", "end",
                values=(
                    b.categorie,
                    f"{b.plafond:,.0f} FCFA".replace(",", " "),
                    f"{b.depenses:,.0f} FCFA".replace(",", " "),
                    f"{b.montant_restant():,.0f} FCFA".replace(",", " "),
                    f"{pct:.1f}%"
                ),
                tags=(tag,))

    def _maj_stats(self):
        """Met à jour la zone de statistiques texte."""
        self.txt_stats.config(state="normal")
        self.txt_stats.delete("1.0", "end")

        if not self.g.transactions:
            self.txt_stats.insert("end",
                                   "Aucune transaction enregistrée.")
            self.txt_stats.config(state="disabled")
            return

        solde = self.g.calculer_solde()
        revenus = self.g.total_revenus()
        depenses = self.g.total_depenses()
        nb = len(self.g.transactions)

        from datetime import datetime
        jour_actuel = datetime.today().day
        projection = ((depenses / jour_actuel) * 30
                      if jour_actuel > 0 and depenses > 0 else 0)

        texte = f"""📊 STATISTIQUES FINANCIÈRES
{'─' * 40}
💰 Solde actuel    : {solde:,.0f} FCFA
📈 Total revenus   : {revenus:,.0f} FCFA
📉 Total dépenses  : {depenses:,.0f} FCFA
📋 Nb transactions : {nb}
📈 Projection mois : {projection:,.0f} FCFA

🏆 TOP 5 DES DÉPENSES
{'─' * 40}
""".replace(",", " ")

        depenses_list = [t for t in self.g.transactions
                         if t.type_transaction() == "depense"]
        top5 = sorted(depenses_list,
                      key=lambda x: x.montant)[:5]
        for i, t in enumerate(top5, 1):
            texte += (f"{i}. {t.description:<30} "
                      f"{abs(t.montant):,.0f} FCFA\n".replace(",", " "))

        texte += f"\n📂 DÉPENSES PAR CATÉGORIE\n{'─' * 40}\n"
        categories = {}
        for t in self.g.transactions:
            if t.type_transaction() == "depense":
                cat = t.categorie
                categories[cat] = (categories.get(cat, 0)
                                   + abs(t.montant))

        for cat, montant in sorted(categories.items(),
                                    key=lambda x: x[1],
                                    reverse=True):
            pct = (montant / depenses * 100) if depenses > 0 else 0
            texte += (f"{cat:<15} : "
                      f"{montant:,.0f} FCFA "
                      f"({pct:.1f}%)\n".replace(",", " "))

        self.txt_stats.insert("end", texte)
        self.txt_stats.config(state="disabled")
    def ouvrir_ajout_transaction(self):
        """Ouvre une fenêtre pour ajouter une transaction."""
        fenetre = tk.Toplevel(self.root)
        fenetre.title("Ajouter une transaction")
        fenetre.geometry("450x420")
        fenetre.configure(bg=COULEUR_FOND)
        fenetre.grab_set()

        tk.Label(fenetre,
                 text="➕ AJOUTER UNE TRANSACTION",
                 font=POLICE_TITRE,
                 bg=COULEUR_FOND,
                 fg=COULEUR_TEXTE).pack(pady=15)

        form = tk.Frame(fenetre, bg=COULEUR_FOND)
        form.pack(padx=20, fill="x")

        # Type
        tk.Label(form, text="Type :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).grid(
                     row=0, column=0, sticky="w", pady=8)
        type_var = tk.StringVar(value="depense")
        tk.Radiobutton(form, text="💸 Dépense",
                       variable=type_var, value="depense",
                       bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                       selectcolor=COULEUR_SURFACE,
                       font=POLICE_NORMAL).grid(
                           row=0, column=1, sticky="w")
        tk.Radiobutton(form, text="💰 Revenu",
                       variable=type_var, value="revenu",
                       bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                       selectcolor=COULEUR_SURFACE,
                       font=POLICE_NORMAL).grid(
                           row=0, column=2, sticky="w")

        # Description
        tk.Label(form, text="Description :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).grid(
                     row=1, column=0, sticky="w", pady=8)
        entry_desc = tk.Entry(form, bg=COULEUR_SURFACE,
                               fg=COULEUR_TEXTE,
                               font=POLICE_NORMAL, width=28,
                               insertbackground="white")
        entry_desc.grid(row=1, column=1, columnspan=2,
                         sticky="ew", pady=8)
    
        # Montant
        tk.Label(form, text="Montant (FCFA) :",
                bg=COULEUR_FOND, fg=COULEUR_TEXTE, font=POLICE_NORMAL).grid(
                    row=2, column=0,sticky="w", pady=8)
        entry_montant = tk.Entry(form, bg=COULEUR_SURFACE,
                                fg=COULEUR_TEXTE,font=POLICE_NORMAL,
                                width=28, insertbackground="white")
        entry_montant.grid(row=2, column=1, columnspan=2,  sticky="ew", pady=8)                              
            
        # Date
        tk.Label(form, text="Date :",
                    bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                    font=POLICE_NORMAL).grid(
                        row=3, column=0, sticky="w", pady=8) 
        entry_date = tk.Entry(form, bg=COULEUR_SURFACE,
                                fg=COULEUR_TEXTE, font=POLICE_NORMAL, width=28,
                                insertbackground="white" )
                
        entry_date.insert(0, str(Date.today()))
        entry_date.grid(row=3, column=1, columnspan=2,
                            sticky="ew", pady=8 )

        
        #Catégorie
        tk.Label(form, text="Catégorie :",
                    bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                    font=POLICE_NORMAL).grid(
                        row=4, column=0, sticky="w", pady=8)
        CATEGORIES = ["Alimentation","Transport","Logement",
                        "Santé", "Loisirs", "Éducation",
                        "Revenu", "Autre"]
        cat_var = tk.StringVar(value="Autre")
        combo_cat = ttk.Combobox(form, textvariable=cat_var,
                                    values=CATEGORIES,
                                    state="readonly", width=26)
        combo_cat.grid(row=4, column=1, columnspan=2,
                            sticky="ew", pady=8)

        def on_desc_change(*args):
                    """Catégorisation automatique à la saisie."""
                    desc = entry_desc.get()
                    if desc:
                        cat = self.g.categoriser(desc)
                        cat_var.set(cat)

        entry_desc.bind("<KeyRelease>", on_desc_change)

        def valider():
                desc = entry_desc.get().strip()
                if not desc:
                    messagebox.showerror("Erreur",
                                        "La description est vide.")
                    return
                try:
                    montant = float(entry_montant.get())
                    if montant <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Erreur",
                                        "Montant invalide.")
                    return

                if type_var.get() == "depense":
                    montant = -montant

                date = entry_date.get().strip() or str(Date.today())
                categorie = cat_var.get()

                self.g.ajouter_transaction(desc, montant,
                                            categorie, date)
                self.rafraichir()
                # Vérification des alertes de budget
                cat = categorie
                mois = date[:7].split("-")[1] if date else Date.today().strftime("%m")
                annee = date[:4] if date else Date.today().strftime("%Y")
                budget = self.g.verifier_budget(cat, mois, annee)
                if budget and type_var.get() == "depense":
                    pct = budget.pourcentage_utilisation()
                    if budget.est_depasse():
                        messagebox.showwarning(
                            "⚠ Budget dépassé !",
                            f"ALERTE : Vous avez dépassé votre budget "
                            f"{cat} !\n\n"
                            f"Plafond : {budget.plafond:,.0f} FCFA\n"
                            f"Dépensé : {budget.depenses:,.0f} FCFA\n"
                            f"Dépassement : "
                            f"{budget.depenses - budget.plafond:,.0f} FCFA"
                        )
                    elif pct >= 80:
                        messagebox.showinfo(
                            "⚠ Attention",
                            f"Vous avez atteint {pct:.1f}% de votre "
                            f"budget {cat}.\n"
                            f"Restant : {budget.montant_restant():,.0f} FCFA"
                        )
                fenetre.destroy()
                messagebox.showinfo("Succès",
                                    "✓ Transaction ajoutée !")

        ttk.Button(fenetre, text="✓ Valider",
                    command=valider).pack(pady=15)


    def modifier_transaction(self):
        """Modifie la transaction sélectionnée."""
        selection = self.tree_transactions.selection()
        if not selection:
            messagebox.showwarning("Attention",
                                "Sélectionnez une transaction.")
            return

        item = self.tree_transactions.item(selection[0])
        id_t = int(item["values"][0])
        desc_actuelle = item["values"][2]
        montant_actuel = item["values"][4].replace(" FCFA", "").replace(" ", "")
        cat_actuelle = item["values"][3]
        date_actuelle = item["values"][1]

        fenetre = tk.Toplevel(self.root)
        fenetre.title("Modifier une transaction")
        fenetre.geometry("450x380")
        fenetre.configure(bg=COULEUR_FOND)
        fenetre.grab_set()

        tk.Label(fenetre,
                text="✏️ MODIFIER LA TRANSACTION",
                font=POLICE_TITRE,
                bg=COULEUR_FOND,
                fg=COULEUR_TEXTE).pack(pady=15)

        form = tk.Frame(fenetre, bg=COULEUR_FOND)
        form.pack(padx=20, fill="x")

        tk.Label(form, text="Description :",
                bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                font=POLICE_NORMAL).grid(
                    row=0, column=0, sticky="w", pady=8)
        entry_desc = tk.Entry(form, bg=COULEUR_SURFACE,
                            fg=COULEUR_TEXTE,
                            font=POLICE_NORMAL, width=28,
                            insertbackground="white")
        entry_desc.insert(0, desc_actuelle)
        entry_desc.grid(row=0, column=1, sticky="ew", pady=8)

        tk.Label(form, text="Montant :",
                bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                font=POLICE_NORMAL).grid(
                    row=1, column=0, sticky="w", pady=8)
        entry_montant = tk.Entry(form, bg=COULEUR_SURFACE,
                                fg=COULEUR_TEXTE,
                                font=POLICE_NORMAL, width=28,
                                insertbackground="white")
        entry_montant.insert(0, montant_actuel)
        entry_montant.grid(row=1, column=1, sticky="ew", pady=8)

        tk.Label(form, text="Date :",
                bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                font=POLICE_NORMAL).grid(
                    row=2, column=0, sticky="w", pady=8)
        entry_date = tk.Entry(form, bg=COULEUR_SURFACE,
                            fg=COULEUR_TEXTE,
                            font=POLICE_NORMAL, width=28,
                            insertbackground="white")
        entry_date.insert(0, date_actuelle)
        entry_date.grid(row=2, column=1, sticky="ew", pady=8)

        tk.Label(form, text="Catégorie :",
                bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                font=POLICE_NORMAL).grid(
                    row=3, column=0, sticky="w", pady=8)
        CATEGORIES = ["Alimentation", "Transport", "Logement",
                    "Santé", "Loisirs", "Éducation",
                    "Revenu", "Autre"]
        cat_var = tk.StringVar(value=cat_actuelle)
        combo_cat = ttk.Combobox(form, textvariable=cat_var,
                                values=CATEGORIES,
                                state="readonly", width=26)
        combo_cat.grid(row=3, column=1, sticky="ew", pady=8)

        def valider():
            desc = entry_desc.get().strip() or None
            try:
                montant = float(
                    entry_montant.get().replace(" ", ""))
            except ValueError:
                messagebox.showerror("Erreur", "Montant invalide.")
                return
            date = entry_date.get().strip() or None
            categorie = cat_var.get() or None

            self.g.modifier_transaction(id_t, desc, montant,
                                        categorie, date)
            self.rafraichir()
            fenetre.destroy()
            messagebox.showinfo("Succès", "✓ Transaction modifiée !")

        ttk.Button(fenetre, text="✓ Valider",
                command=valider).pack(pady=15)


    def supprimer_transaction(self):
        """Supprimer la transaction sélectionnée."""
        selection = self.tree_transactions.selection()
        if not selection:
            messagebox.showwarning("Attention",
                                    "Sélectionnez une transaction.")            
            return
        item = self.tree_transactions.item(selection[0])
        id_t = int (item["values"][0])
        desc = item["values"][2]
        if messagebox.askyesno(
            "Comfirmer",
            f"Supprimer la transaction:\n{desc}?"):
            self.g.supprimer_transaction(id_t)
            self.rafraichir()
            messagebox.showinfo("Succès","✓ Transaction supprimée!")

    def ouvrir_ajout_budget(self):
        """Ouvre une fenêtre pour définir un budget."""
        fenetre = tk.Toplevel(self.root)     
        fenetre.title("Définir un budget")     
        fenetre.geometry ("400x300")     
        fenetre.configure (bg=COULEUR_FOND)     
        fenetre.grab_set()  

        tk.Label(fenetre,
                 text="🎯 DÉFINIR UN BUDGET",
                 font=POLICE_TITRE,
                 bg=COULEUR_FOND,
                 fg=COULEUR_TEXTE).pack(pady=15)

        form = tk.Frame(fenetre, bg=COULEUR_FOND)
        form.pack(padx=20, fill="x")

        # Catégorie
        tk.Label(form, text="Catégorie :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).grid(
                     row=0, column=0, sticky="w", pady=8)
        CATEGORIES = ["Alimentation", "Transport", "Logement",
                      "Santé", "Loisirs", "Éducation", "Autre"]
        cat_var = tk.StringVar(value="Alimentation")
        combo_cat = ttk.Combobox(form, textvariable=cat_var,
                                  values=CATEGORIES,
                                  state="readonly", width=25)
        combo_cat.grid(row=0, column=1, sticky="ew", pady=8)

        # Plafond
        tk.Label(form, text="Plafond (FCFA) :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).grid(
                     row=1, column=0, sticky="w", pady=8)
        entry_plafond = tk.Entry(form, bg=COULEUR_SURFACE,
                                  fg=COULEUR_TEXTE,
                                  font=POLICE_NORMAL, width=27,
                                  insertbackground="white")
        entry_plafond.grid(row=1, column=1, sticky="ew", pady=8)

        # Mois
        tk.Label(form, text="Mois :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).grid(
                     row=2, column=0, sticky="w", pady=8)
        entry_mois = tk.Entry(form, bg=COULEUR_SURFACE,
                               fg=COULEUR_TEXTE,
                               font=POLICE_NORMAL, width=27,
                               insertbackground="white")
        entry_mois.insert(0, Date.today().strftime("%m"))
        entry_mois.grid(row=2, column=1, sticky="ew", pady=8)

        # Année
        tk.Label(form, text="Année :",
                 bg=COULEUR_FOND, fg=COULEUR_TEXTE,
                 font=POLICE_NORMAL).grid(
                     row=3, column=0, sticky="w", pady=8)
        entry_annee = tk.Entry(form, bg=COULEUR_SURFACE,
                                fg=COULEUR_TEXTE,
                                font=POLICE_NORMAL, width=27,
                                insertbackground="white")
        entry_annee.insert(0, Date.today().strftime("%Y"))
        entry_annee.grid(row=3, column=1, sticky="ew", pady=8)

        def valider():
            try:
                plafond = float(entry_plafond.get())
                if plafond <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Erreur", "Plafond invalide.")
                return
            self.g.ajouter_budget(cat_var.get(), plafond,
                                   entry_mois.get(),
                                   entry_annee.get())
            self.rafraichir()
            fenetre.destroy()
            messagebox.showinfo("Succès", "✓ Budget défini !")

        ttk.Button(fenetre, text="✓ Valider",
                   command=valider).pack(pady=15)

    def rechercher(self):
        """Recherche des transactions par mot-clé."""
        mot_cle = self.entry_recherche.get().strip()
        if not mot_cle:
            messagebox.showwarning("Attention",
                                   "Entrez un mot-clé.")
            return

        for item in self.tree_recherche.get_children():
            self.tree_recherche.delete(item)

        resultats = self.g.rechercher(mot_cle)
        for t in resultats:
            montant = f"{t.montant:,.0f} FCFA".replace(",", " ")
            tag = t.type_transaction()
            self.tree_recherche.insert(
                "", "end",
                values=(t.id, t.date, t.description,
                        t.categorie, montant,
                        t.type_transaction()),
                tags=(tag,))

        if not resultats:
            messagebox.showinfo("Résultat",
                                f"Aucun résultat pour '{mot_cle}'.")

    
    def afficher_camembert(self):
        """Camembert des dépenses par catégorie."""
        import matplotlib.pyplot as plt

        categories = {}
        for t in self.g.transactions:
            if t.type_transaction() == "depense":
                cat = t.categorie
                categories[cat] = (categories.get(cat, 0)
                                   + abs(t.montant))
        if not categories:
            messagebox.showinfo("Info", "Aucune dépense enregistrée.")
            return

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.patch.set_facecolor("#1E1E2E")
        ax.set_facecolor("#1E1E2E")
        couleurs = ["#7C3AED", "#10B981", "#F59E0B",
                    "#EF4444", "#3B82F6", "#EC4899", "#6B7280"]
        wedges, texts, autotexts = ax.pie(
            categories.values(),
            labels=categories.keys(),
            autopct="%1.1f%%",
            colors=couleurs[:len(categories)],
            textprops={"color": "white"},
            startangle=90,
            wedgeprops={"edgecolor": "#1E1E2E", "linewidth": 2}
        )
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight("bold")
        ax.set_title("Répartition des dépenses par catégorie",
                     color="white", fontsize=14, pad=20)
        plt.tight_layout()
        plt.show()

    def afficher_histogramme(self):
        """
        Histogramme des dépenses et revenus par jour du mois.
        Montre l'évolution quotidienne jour par jour.
        """
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
        from datetime import datetime

        if not self.g.transactions:
            messagebox.showinfo("Info", "Aucune transaction enregistrée.")
            return

        # Regrouper par jour
        revenus_par_jour = {}
        depenses_par_jour = {}

        for t in self.g.transactions:
            jour = t._date
            if t.type_transaction() == "revenu":
                revenus_par_jour[jour] = (
                    revenus_par_jour.get(jour, 0) + t.montant)
            else:
                depenses_par_jour[jour] = (
                    depenses_par_jour.get(jour, 0) + abs(t.montant))

        # Tous les jours présents
        tous_jours = sorted(set(
            list(revenus_par_jour.keys()) +
            list(depenses_par_jour.keys())
        ))

        x = range(len(tous_jours))
        rev = [revenus_par_jour.get(j, 0) for j in tous_jours]
        dep = [depenses_par_jour.get(j, 0) for j in tous_jours]

        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor("#1E1E2E")
        ax.set_facecolor("#2A2A3E")

        largeur = 0.35
        barres_rev = ax.bar(
            [i - largeur/2 for i in x], rev,
            width=largeur, color=COULEUR_VERT,
            label="Revenus", alpha=0.85,
            edgecolor="#1E1E2E")
        barres_dep = ax.bar(
            [i + largeur/2 for i in x], dep,
            width=largeur, color=COULEUR_ROUGE,
            label="Dépenses", alpha=0.85,
            edgecolor="#1E1E2E")

        # Valeurs sur les barres
        for barre in barres_rev:
            h = barre.get_height()
            if h > 0:
                ax.text(barre.get_x() + barre.get_width()/2,
                        h * 1.01,
                        f"{h:,.0f}".replace(",", " "),
                        ha="center", color="white",
                        fontsize=7, rotation=45)
        for barre in barres_dep:
            h = barre.get_height()
            if h > 0:
                ax.text(barre.get_x() + barre.get_width()/2,
                        h * 1.01,
                        f"{h:,.0f}".replace(",", " "),
                        ha="center", color="white",
                        fontsize=7, rotation=45)

        ax.set_xticks(list(x))
        ax.set_xticklabels(
            [j[5:] for j in tous_jours],
            rotation=45, color="white", fontsize=9)
        ax.set_title("Revenus et Dépenses par jour",
                     color="white", fontsize=14)
        ax.tick_params(colors="white")
        ax.legend(facecolor="#2A2A3E",
                  labelcolor="white", fontsize=10)
        ax.spines["bottom"].set_color("#94A3B8")
        ax.spines["left"].set_color("#94A3B8")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.show()

    
    def afficher_courbe(self):
        """
        Deux courbes : évolution cumulée des revenus et des dépenses.
        Courbes lisses interpolées style mathématique.
        """
        import matplotlib.pyplot as plt
        import numpy as np
        from scipy.interpolate import make_interp_spline
        import matplotlib.patheffects as pe
        from datetime import datetime, date as DateType
        import matplotlib.dates as mdates

        if not self.g.transactions:
            messagebox.showinfo("Info", "Aucune transaction enregistrée.")
            return

        def to_datetime(d):
            """Convertit n'importe quel format de date en datetime."""
            if isinstance(d, datetime):
                return d
            if isinstance(d, DateType):
                return datetime(d.year, d.month, d.day)
            if isinstance(d, str):
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
                    try:
                        return datetime.strptime(d.strip(), fmt)
                    except ValueError:
                        continue
            return None  # date non convertible → ignorée

        transactions_triees = sorted(self.g.transactions,
                                    key=lambda x: str(x.date))
        dates_dt = []
        revenus_cumules = []
        depenses_cumulees = []
        rev_cumule = 0
        dep_cumule = 0

        for t in transactions_triees:
            dt = to_datetime(t.date)
            if dt is None:
                continue  # ignore les dates invalides
            dates_dt.append(dt)
            if t.type_transaction() == "revenu":
                rev_cumule += t.montant
            else:
                dep_cumule += abs(t.montant)
            revenus_cumules.append(rev_cumule)
            depenses_cumulees.append(dep_cumule)

        if len(dates_dt) < 2:
            messagebox.showinfo(
                "Info",
                "Pas assez de transactions valides pour tracer la courbe.")
            return

        # Conversion unique et fiable en float matplotlib
        dates_num = np.array(mdates.date2num(dates_dt))
        rev_arr = np.array(revenus_cumules, dtype=float)
        dep_arr = np.array(depenses_cumulees, dtype=float)

        def lisser_courbe(x, y):
            """Lisse une courbe avec spline cubique si assez de points."""
            if len(x) >= 4:
                try:
                    x_new = np.linspace(x.min(), x.max(), 400)
                    spl = make_interp_spline(x, y, k=3)
                    return x_new, spl(x_new)
                except Exception:
                    pass  # si spline échoue → courbe brute
            return x, np.array(y)

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 11))
        fig.patch.set_facecolor("#0F0F1A")
        fig.subplots_adjust(hspace=0.4)

        # ── GRAPHIQUE 1 : Revenus et Dépenses cumulés ──
        ax1.set_facecolor("#13132A")
        ax1.grid(color="#ffffff10", linestyle="--",
                linewidth=0.6, zorder=0)

        x_s, rev_s = lisser_courbe(dates_num, rev_arr)
        _, dep_s   = lisser_courbe(dates_num, dep_arr)

        ax1.plot(x_s, rev_s,
                color=COULEUR_VERT, linewidth=2.8,
                label="Revenus cumulés",
                path_effects=[
                    pe.SimpleLineShadow(shadow_color="#10B98155", linewidth=8),
                    pe.Normal()])
        ax1.fill_between(x_s, rev_s, alpha=0.12, color=COULEUR_VERT)

        ax1.plot(x_s, dep_s,
                color=COULEUR_ROUGE, linewidth=2.8,
                label="Dépenses cumulées",
                path_effects=[
                    pe.SimpleLineShadow(shadow_color="#EF444455", linewidth=8),
                    pe.Normal()])
        ax1.fill_between(x_s, dep_s, alpha=0.12, color=COULEUR_ROUGE)

        ax1.scatter(dates_num, revenus_cumules,
                    color=COULEUR_VERT, s=50, zorder=5,
                    edgecolors="white", linewidths=0.8)
        ax1.scatter(dates_num, depenses_cumulees,
                    color=COULEUR_ROUGE, s=50, zorder=5,
                    edgecolors="white", linewidths=0.8)

        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax1.xaxis_date()
        ax1.set_title("📈 Évolution cumulée — Revenus vs Dépenses",
                    color="white", fontsize=13, fontweight="bold", pad=15)
        ax1.tick_params(colors="white", rotation=45, labelsize=9)
        ax1.legend(facecolor="#1E1E2E", labelcolor="white",
                fontsize=10, framealpha=0.8)
        for spine in ax1.spines.values():
            spine.set_color("#ffffff20")

        # ── GRAPHIQUE 2 : Solde net ──
        ax2.set_facecolor("#13132A")
        ax2.grid(color="#ffffff10", linestyle="--",
                linewidth=0.6, zorder=0)

        soldes  = [r - d for r, d in zip(revenus_cumules, depenses_cumulees)]
        sol_arr = np.array(soldes, dtype=float)
        x_s2, sol_s = lisser_courbe(dates_num, sol_arr)

        ax2.fill_between(x_s2, sol_s, 0,
                        where=sol_s >= 0,
                        alpha=0.25, color=COULEUR_VERT,
                        label="Solde positif")
        ax2.fill_between(x_s2, sol_s, 0,
                        where=sol_s < 0,
                        alpha=0.25, color=COULEUR_ROUGE,
                        label="Solde négatif")

        ax2.plot(x_s2, sol_s,
                color=COULEUR_ACCENT, linewidth=3,
                path_effects=[
                    pe.SimpleLineShadow(shadow_color="#7C3AED66", linewidth=10),
                    pe.Normal()])

        couleurs_pts = [COULEUR_VERT if s >= 0
                        else COULEUR_ROUGE for s in soldes]
        ax2.scatter(dates_num, soldes,
                    color=couleurs_pts, s=60, zorder=5,
                    edgecolors="white", linewidths=0.8)

        ax2.axhline(y=0, color="white",
                    linestyle="--", linewidth=1.2, alpha=0.4)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        ax2.xaxis_date()
        ax2.set_title("💰 Évolution du solde net",
                    color="white", fontsize=13, fontweight="bold", pad=15)
        ax2.tick_params(colors="white", rotation=45, labelsize=9)
        ax2.legend(facecolor="#1E1E2E", labelcolor="white",
                fontsize=10, framealpha=0.8)
        for spine in ax2.spines.values():
            spine.set_color("#ffffff20")

        plt.tight_layout()
        plt.show()


    def afficher_budget_vs_reel(self):
        """
        Graphique budget prévu vs dépenses réelles par carégorie.
        Barres rouges si dépassé, vertes sinon.
        """

        import matplotlib.pyplot as plt
        import numpy as np

        if not self.g.budgets:
            messagebox.showinfo("Info", "Aucun budget défini.")
            return
        
        categories = [b.categorie for b in self.g.budgets]
        plafonds = [b.plafond for b in self.g.budgets]
        depenses = [b.depenses for b in self.g.budgets]
        couleurs_dep = [COULEUR_ROUGE if b.est_depasse()
                        else COULEUR_VERT for b in self.g.budgets]
        
        x = range(len(categories))
        largeur = 0.35

        fig, ax = plt.subplots(figsize=(10, 6))
        fig.patch.set_facecolor("#1E1E2E")
        ax.set_facecolor("#2A2A3E")

        barres_plafond = ax.bar(
            [i - largeur/2 for i in x], plafonds,
            width=largeur, color=COULEUR_ACCENT,
            label="Budget prévu", alpha=0.85,
            edgecolor="#1E1E2E")
        barres_dep = ax.bar(
            [i + largeur/2 for i in x], depenses,
            width=largeur, color=couleurs_dep,
            label="Dépenses réelles", alpha=0.85,
            edgecolor="#1E1E2E")

        # Ligne de plafond
        for i, (p, b) in enumerate(zip(plafonds, self.g.budgets)):
            if b.est_depasse():
                ax.annotate("⚠ DÉPASSÉ", xy=(i, b.depenses), 
                            xytext=(i, b.depenses * 1.05),
                            color=COULEUR_ROUGE,
                            fontsize=9,
                            ha="center",
                            fontweight="bold")
        ax.set_xticks(list(x))
        ax.set_xticklabels(categories,
                            color="white",
                            fontsize=10)
        ax.set_title("Budget prévu vs Dépenses réelles",
                    color="white",
                    fontsize=14)
        ax.tick_params(colors="white")
        ax.legend(facecolor="#2A2A3E",
                  labelcolor="white", fontsize=10)
        ax.spines["bottom"].set_color("#94A3B8")
        ax.spines["left"].set_color("#94A3B8")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        plt.tight_layout()
        plt.show()

    def filtrer_periode(self):
        """ Filtre les transactions par période."""
        date_debut = self.entry_date_debut.get().strip()
        date_fin = self.entry_date_fin.get().strip()

        if not date_debut or not date_fin:
            messagebox.showwarning("Attention", "Entrez une date de début et de fin.")
            return

        for item in self.tree_recherche.get_children():
            self.tree_recherche.delete(item)

        resultats = self.g.filtrer_par_periode(date_debut, date_fin)
        for t in resultats:
            montant = f"{t.montant:,.0f} FCFA".replace(",","")
            tag = t.type_transaction()
            self.tree_recherche.insert(
                    "", "end",
                    values=(t.id, t.date, t.description,
                                t.categorie,
                                montant,
                                t.type_transaction()),
                                tags=(tag,))
        if not resultats:
            messagebox.showinfo(
                "Résultat",
                f"Aucune transaction entre {date_debut} et {date_fin}." )
    def exporter_rapport(self):
        """Exporte le rapport mensuel en CSV."""
        mois = Date.today().strftime("%m")
        annee = Date.today().strftime("%Y")
        chemin = self.g.exporter_rapport_mensuel(mois, annee)
        if chemin:
            messagebox.showinfo(
                "Exporter réussi",
                f"✓ Rapport exporté :\n{chemin}")
        else:
            messagebox.showerror(
                "Erreur",
                "Impossible d'exporter le rapport."
            )
           
# =================================================================================================
# Point d'entrée
# ===============================================================================================
def main():
    """Lance l'interface graphique FinTrack."""
    root = tk.Tk()
    app = FinTrackApp(root)
    root.mainloop()


if __name__ =="__main__":
    main()