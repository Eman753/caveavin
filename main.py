#!/usr/bin/python3

# Main script of caveavin

# On importe les modules et bibliothèques utiles au programme
import pymysql
import flask
import csv
import hashlib
import getpass
from tabulate import tabulate

# On déclare les listes contenant les objets, afin de pouvoir les stocker en RAM et facilement intéragir avec les objets.
ListeUtilisateurs = []
ListeBouteilles = []
ListeEtageres = []
ListeCaves = []
ListeArchives = []

# Fonction pour se connecter à la base de données MariaDB à partir d'un fichier CSV. On utilise pymysql comme module.
# Le fichier ne sera pas rajouté dans le dépôt (.gitignore). On utilise des ; comme délimiteurs, sous la forme
# [IP DU SERVEUR];[LOGIN BDD];[PASSWD BDD];[BDD]
def sql_conn():
    donnees = []
    with open('db.csv', newline='') as csvfile:
        lecteur_csv = csv.reader(csvfile, delimiter=';')
        for row in lecteur_csv:
            donnees.append(row)
    db=pymysql.connect(host=donnees[0][0], charset="utf8",user=donnees[0][1], passwd=donnees[0][2],db=donnees[0][3])
    return db

# Fonction permettant le hashage en SHA256. Sera utilisé principalement pour le stockage de mots de passe
def hash(message):
    m = hashlib.sha256()
    m.update(message.encode())
    return m.hexdigest()

# Classe d'un utilisateur
class Utilisateur:
    
    def __init__(self,login,nom,prenom,passwd,inscription):
        self.login = login
        self.nom = nom
        self.prenom = prenom
        self.passwd = passwd
        self.inscription = inscription

    def registerBDD(self):
        db = sql_conn()
        c = db.cursor()
        c.execute("insert into users values (DEFAULT,'"+self.login+"','"+self.nom+"','"+self.prenom+"','"+self.passwd+"','"+self.inscription+"');")
        db.commit()
        c.close()
        db.close()

    def getInfo(self):
        return self.login, self.nom, self.prenom, self.passwd, self.inscription

# Fonction générique pour afficher la liste des objets d'une classe
# Toutes les classes auront la même méthode getInfo permettant d'extraire les infos
def getAndTabulate(liste,objet):
    tableau = []
    for i in liste:
        if isinstance(i, objet):
            tableau.append(i.getInfo())  # Récupère les infos sous forme de tuple
        if objet == Utilisateur:
            headers = ["Login", "Nom", "Prénom", "Mot de passe hashé", "Date d'inscription"]
        return tabulate(tableau, headers=headers, tablefmt="grid")

# CLI interactif. Peut être utilisé en même temps que Flask.
# Servira aussi pour journaliser les actions
def cli():
    c = True
    print("")
    print("Bienvenue sur l'interface en ligne de commandes de caveavin !")
    while c:
        print("")
        print("Voici les actions disponibles")
        print("")
        print("exit - Quitter le programme")
        print("register - Enregistrer un utilisateur dans le système")
        print("showuser - Voir la liste d'utilisateurs")
        print("")
        try:
            command = str(input("Commande -> "))
            print("")
            if command == "exit" or command == "EXIT":
                print("Déconnexion !")
                c = False
            elif command == "register" or command == "REGISTER":
                login = str(input("Login -> "))
                nom = str(input("Nom -> "))
                prenom = str(input("Prénom -> "))
                passwd = getpass.getpass(prompt='Mot de passe -> ', stream=None)
                passwd = hash(passwd)
                inscription = str(input("Date d'inscription (DD-MM-YYYY) -> "))
                new_user = Utilisateur(login,nom,prenom,passwd,inscription)
                ListeUtilisateurs.append(new_user)
                new_user.registerBDD()
            elif command == "showuser" or command == "SHOWUSER":
                print(getAndTabulate(ListeUtilisateurs,Utilisateur))
            else:
                print("Commande inconnue")
        except TypeError as e:
            print("Erreur lors du traitement de la commande (TypeError)")
    print("Sortie du CLI")

cli()
exit(0)