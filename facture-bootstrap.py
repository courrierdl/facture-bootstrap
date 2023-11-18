#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as sd
from ttkbootstrap.constants import *
import ttkbootstrap as tb
from ttkbootstrap import Style, Window
from tabulate import tabulate
from datetime import datetime
from tkinter import messagebox
import random
from tkinter import filedialog
from tkcalendar import Calendar
from PIL import Image
from PIL.ImageTk import PhotoImage
from tkinter import font as tkFont

root = tb.Window(themename="superhero")

root.title("DLC")

largeur_fenetre = 1900
hauteur_fenetre = 1000

# Obtenir les dimensions de l'écran
largeur_ecran = root.winfo_screenwidth()
hauteur_ecran = root.winfo_screenheight()

# Calculer la position x et y pour centrer la fenêtre
x = (largeur_ecran - largeur_fenetre) // 2
y = (hauteur_ecran - hauteur_fenetre) // 2

# Définir la géométrie pour centrer la fenêtre
root.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x}+{y}")

# Créez une police monospace
monospace_font = tkFont.Font(family="Courier", size=16)  # Vous pouvez ajuster la taille de la police selon vos préférences

# Ajout du style en gras (bold)
#monospace_font.configure(weight="bold")

# Liste pour stocker les numéros de facture existants
numeros_de_facture_existant = []

current_date = datetime.now().strftime("%Y-%m-%d")

client_label = tb.Label(text="Client:",font=("Helvetica",20),bootstyle="success")
client_label.place(x=55,y=50)
client_entry = tb.Entry(bootstyle="success",font=("Helvetica",14),width=25,foreground="#E9B824")
client_entry.place(x=150,y=50)

date_combobox_label = tb.Label(text="Date:", font=("Helvetica",20),bootstyle="success")
date_combobox_label.place(x=55,y=100)
date_combobox = tb.Combobox(root)
date_combobox['values'] = [" ",current_date]
date_combobox.set(" ")
date_combobox.place(x=150,y=100)

def set_focus_on_combobox(event):
    client = client_entry.get().title()
    client_entry.delete(0,"end")

    client_entry.insert(0,client)


    date_combobox.focus_set()

client_entry.bind("<Return>", set_focus_on_combobox)
client_entry.bind("<Tab>", set_focus_on_combobox)


texte_facture = tb.Text(width=63,height=35)
texte_facture.place(x=970,y=50)
texte_facture.insert(tk.END,"")
texte_facture.config(font=monospace_font,state=tk.DISABLED, foreground="#ECE3CE")  # Empêche la modification du texte

style = tb.Style()
style.configure("Treeview.Heading", font=("Helvetica", 16))

columns = ("Article", "Quantité", "Prix $")

table = tb.Treeview(root, columns=columns, show="headings")
# Définissez l'ancrage du texte des en-têtes de colonne à gauche
for col in columns:
    table.heading(col, text=col, anchor='w')  # 'w' signifie "west" (à gauche)

# Définissez une police personnalisée en utilisant tag_configure
table.tag_configure("custom_font", font=("Helvetica", 12),background="#111d41",foreground="#E9B824")  # Spécifiez la police et la taille de police souhaitées

for col in columns:
    table.heading(col, text=col)

table.place(x=250,y=200,height=630,width=660)

client_entry.focus()


def ajouter_article():
    client = client_entry.get().strip()  # Obtenez le contenu du champ client
    date = date_combobox.get()
    if not client:
        # Le champ client est vide, affichez une erreur ou effectuez une action appropriée
        messagebox.showerror("Erreur", "Veuillez saisir le nom du client.")
        return  # Quittez la fonction
    if date == " ":
        messagebox.showerror("Erreur", "Veuillez saisir la date.")
        return
    article = sd.askstring("Article", "Entrez l'article :").title()
    quantite = sd.askinteger("Quantité", "Entrez la quantité :")
    prix = sd.askfloat("Prix", "Entrez le prix :")
    if article and quantite is not None and prix is not None:
        # Insérez des données avec la police personnalisée
        table.insert("", "end", values=(article, quantite, prix), tags=("custom_font"))
    else:
        messagebox.showerror("Erreur", "Entrer tout les champs")
        return

def supprimer_article():
    global selected_item  # Utilisez la variable globale pour suivre la ligne sélectionnée
    selected_item = table.selection()  # Mise à jour de la ligne sélectionnée

    if not selected_item:
        messagebox.showerror("Erreur", "Aucune ligne sélectionnée.")
        return
    if selected_item:
        if messagebox.askyesno("Confirmation", "Supprimer Article?"):
            # Récupérer les valeurs actuelles de la ligne sélectionnée
            ligne_selectionnee = table.delete(selected_item)
            if len(table.get_children()) == 0:
                texte_facture.config(state=tk.NORMAL)
                texte_facture.delete("1.0", tk.END)
                client_entry.delete(0, "end")
                texte_facture.config(state=tk.DISABLED)
                client_entry.focus()


def modifier_article():
    global selected_item  # Utilisez la variable globale pour suivre la ligne sélectionnée
    selected_item = table.selection()  # Mise à jour de la ligne sélectionnée

    if not selected_item:
        messagebox.showerror("Erreur", "Aucune ligne sélectionnée.")
        return

    # Récupérer les valeurs actuelles de la ligne sélectionnée
    ligne_selectionnee = table.item(selected_item)
    article_actuel = ligne_selectionnee['values'][0]
    quantite_actuelle = ligne_selectionnee['values'][1]
    prix_actuel = ligne_selectionnee['values'][2]

    # Afficher les valeurs actuelles dans les boîtes de dialogue pour modification
    nouvel_article = sd.askstring("Modifier l'article", "Nouvel article :", initialvalue=article_actuel).title()
    nouvelle_quantite = sd.askinteger("Modifier la quantité", "Nouvelle quantité :", initialvalue=quantite_actuelle)
    nouveau_prix = sd.askfloat("Modifier le prix", "Nouveau prix :", initialvalue=prix_actuel)
    prix_signe = nouveau_prix
    prix_signe = f"{prix_signe}$"

    if nouvel_article is not None and nouvelle_quantite is not None and nouveau_prix is not None:
        # Mettre à jour la ligne sélectionnée avec les nouvelles valeurs
        table.item(selected_item, values=(nouvel_article, nouvelle_quantite, nouveau_prix))
    else:
        messagebox.showerror("Erreur", "Entrez toutes les valeurs.")

def calculer_total():
    if len(table.get_children()) == 0:
        messagebox.showerror("Erreur", "Aucuns articles entrée")
        return
        
 #   if numero_facture:
    total = 0
    montant_total_tps = 0
    montant_total_tvq = 0

    total_sans_taxes = 0  # Pour le montant total avant taxes
    taux_tps = 0.05  # Taux de la TPS (5 %)
    taux_tvq = 0.09975  # Taux de la TVQ (9,975 %)

    for item in table.get_children():
        quantite = int(table.item(item, "values")[1])
        prix = float(table.item(item, "values")[2])
        montant_sans_taxes = quantite * prix  # Montant avant taxes pour cet article

        # Ajoutez le montant sans taxes au total avant taxes
        total_sans_taxes += montant_sans_taxes

        # Calculez la TPS et la TVQ pour cet article
        tps = montant_sans_taxes * taux_tps
        tvq = montant_sans_taxes * taux_tvq

        montant_total_tps = montant_total_tps + tps
        montant_total_tvq = montant_total_tvq + tvq

        # Ajoutez la TPS et la TVQ au montant total
        total += montant_sans_taxes + tps + tvq

    if numeros_de_facture_existant == []:
        global numero_facture
        numero_facture = generer_numero_facture()
    
    afficher_formulaire_facture(montant_total_tvq, montant_total_tps)

def afficher_formulaire_facture(tvq, tps):
    global facture_text 

    client = client_entry.get().title()
    date = date_combobox.get()

    total = 0

    facture_text = f"Facture #:{numero_facture}\nClient : {client}\nDate : {date}\n\n"

    facture_data = []  # Stockage des données pour le tableau

    for item in table.get_children():
        nom_article = table.item(item, "values")[0]
        quantite = int(table.item(item, "values")[1])
        prix = float(table.item(item, "values")[2])
        total_article = quantite * prix

        facture_data.append([nom_article, quantite, f"{prix:.2f}$", f"{total_article:.2f}$"])

        total += total_article

    total_taxes = total + tps + tvq

    facture_text += tabulate(facture_data, headers=["Article", "Quantité", "Prix unitaire", "Montant total"], tablefmt="pretty")
    facture_text += f"\n\nAvant Taxes : {round(total,2)}$\n"
    facture_text += f"tps : {round(tps,2)}$\n"
    facture_text += f"tvq : {round(tvq,2)}$\n"
    facture_text += f"Total : {round(total_taxes,2)}$\n\n"

    texte_facture.config(state=tk.NORMAL)

    texte_facture.delete('1.0', tk.END)  # Efface le texte existant dans le widget Text
    texte_facture.insert(tk.END, facture_text)

    # Appliquez la police monospace au widget Text
    texte_facture.config(font=monospace_font,state=tk.DISABLED, foreground="#A7D397")  # Empêche la modification du texte

def generer_numero_facture():
    while True:
        numero_facture = random.randint(1000, 9999)  # Par exemple, un numéro aléatoire de 4 chiffres
        if numero_facture not in numeros_de_facture_existant:
            numeros_de_facture_existant.append(numero_facture)
            return numero_facture

def sauvegarder():
    date = datetime.now().strftime("%Y-%m-%d")
    facture = texte_facture.get("1.0", tk.END)
    
    if facture != "\n" and facture != "":
        if messagebox.askyesno("Confirmation", "Sauvegarder?"):
            with open(f"facture_{numero_facture}_{date}.txt", "w") as fichier:
                fichier.write(facture_text)
            
            for item in table.get_children():
                table.delete(item)
            
            numeros_de_facture_existant.clear()
            texte_facture.config(state=tk.NORMAL)
            texte_facture.delete("1.0", tk.END)
            client_entry.delete(0, "end")
            texte_facture.config(state=tk.DISABLED)
            client_entry.focus()
    else:
        return
        
def afficher_facture():
    # Fonction pour sélectionner un fichier à décrypter
    nom_fichier = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Facture", "*.txt")])
    if nom_fichier:
        with open(nom_fichier, "r") as fichier_facture:
            contenu_texte = fichier_facture.read()

            # Créer une nouvelle fenêtre
            affichage_window = tb.Toplevel(root)
            affichage_window.title("Facture")

            # Calculer les dimensions de la fenêtre
            largeur_fenetre = 1000
            hauteur_fenetre = 650

            # Obtenir les dimensions de l'écran
            largeur_ecran = affichage_window.winfo_screenwidth()
            hauteur_ecran = affichage_window.winfo_screenheight()

            # Calculer la position x et y pour centrer la fenêtre
            x = (largeur_ecran - largeur_fenetre) // 2
            y = (hauteur_ecran - hauteur_fenetre) // 2

            # Définir la géométrie pour centrer la fenêtre
            affichage_window.geometry(f"{largeur_fenetre}x{hauteur_fenetre}+{x}+{y}")

            # Créer un widget Text pour afficher le contenu du fichier texte
            text_widget = tb.Text(affichage_window, wrap=tb.WORD, font=("Helvetica", 14))
            text_widget.pack()

            # Insérer le contenu du fichier dans le widget Text
            text_widget.insert(tb.END, contenu_texte)

            text_widget.config(font=monospace_font,state=tk.DISABLED, foreground="#A7D397")  # Empêche la modification du texte

            # Ajouter un bouton pour fermer la fenêtre
            fermer_button = tb.Button(affichage_window,bootstyle="success, outline", text="Fermer", command=affichage_window.destroy)
            fermer_button.place(x=450,y=600)
            client_entry.focus()

def quitter():
    if messagebox.askyesno("Confirmation", "Êtes-vous sûr de\nvouloir quitter ? "):
        root.destroy()

root.protocol("WM_DELETE_WINDOW", quitter)

# Configuration de la police pour les boutons
style = tb.Style(theme="superhero")  # Vous pouvez choisir un autre thème si vous le souhaitez
style.configure("TButton", font=("Helvetica", 14))  # Changer la taille de police ici (16 points)

article_bouton = tb.Button(bootstyle="success, outline",text="Ajouter Article",width=14, command=ajouter_article)
article_bouton.place(x=25,y=200)
modifier_bouton = tb.Button(bootstyle="primary, outline", text="Modifier Article",width=14, command=modifier_article)
modifier_bouton.place(x=25,y=300)
supprimer_bouton = tb.Button(bootstyle="danger, outline", text="Supprimer Article",width=14, command=supprimer_article)
supprimer_bouton.place(x=25,y=350)
total_bouton = tb.Button(bootstyle="success, outline", text="Calculer Total",width=14, command=calculer_total)
total_bouton.place(x=25,y=550)

afficher_facture_bouton = tb.Button(bootstyle="success, outline", text="Afficher Facture",width=14, command=afficher_facture)
afficher_facture_bouton.place(x=1470,y=900)
sauvegarder_bouton = tb.Button(bootstyle="success, outline",text="Sauvegarder",width=14, command=sauvegarder)
sauvegarder_bouton.place(x=1200,y=900)

root.mainloop()
