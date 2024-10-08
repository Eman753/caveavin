#!/usr/bin/python3

# Main script of caveavin

# On importe les modules et bibliothèques utiles au programme
import pymysql
import flask
import csv
import hashlib
import getpass
from tabulate import tabulate
from datetime import date

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

# Fonction permettant de recréer les objets Python à partir des objets dans la BDD
def recreateUsers():
    error = 0
    ListeUtilisateurs.clear()
    try:
        db = sql_conn()
        c = db.cursor()
        c.execute("select login,nom,prenom,passwd,inscription from users")
        result = c.fetchall()
        if result:
            for row in result:
                # Crée un objet Utilisateur pour chaque ligne et l'ajoute à la liste
                new_user = Utilisateur(login=row[0], nom=row[1], prenom=row[2], passwd=row[3], inscription=row[4])
                ListeUtilisateurs.append(new_user)
            c.close()
            db.close()
            return ListeUtilisateurs
        else:
            error = 2
            return error
    except TypeError as e:
        error = 1
        return error

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

# Fonction similaire à celle du dessus, mais va chercher dans la BDD
def getAndTabulateFromBDD(objet):
    db = sql_conn()
    c = db.cursor()
    tableau = []
    error = 0
    if objet == "user":
        c.execute("select login,nom,prenom,passwd,inscription from users")
        result = c.fetchall()
        if result:
            tableau = [list(row) for row in result]
            headers = ["Login", "Nom", "Prénom", "Mot de passe hashé", "Date d'inscription"]
            c.close()
            db.close()
            return tabulate(tableau, headers=headers, tablefmt="grid")
        else:
            error = 2
            return error
    else:
        error = 1
        return error

# Second CLI interactif pour les interactions avec la BDD
# De cette manière, on différencie la gestion des objets Python, qui ne durent que le temps de fonctionnement du programme
# Et on différencie les objets stockés en BDD
def bdd():
    z = True
    while z:
        print("")
        print("Bienvenue en mode BDD")
        print("")
        print("Voici les actions disponibles")
        print("")
        print("exit - Sortir du mode BDD")
        print("showuser - Liste les utilisateurs présents dans la BDD")
        try:
            print("")
            command = str(input("BDD# -> "))
            print("")
            if command == "exit" or command == "EXIT":
                print("Sortie du mode BDD")
                z = False
            elif command == "showuser" or command == "SHOWUSER":
                result = getAndTabulateFromBDD("user")
                if result == 1:
                    print("Une erreur a eu lieu pendant le traitement de la demande")
                elif result == 2:
                    print("Aucun objet n'a été trouvé dans la BDD")
                else:
                    print(result)
            else:
                print("Commande inconnue")
        except TypeError as e:
            print("Erreur lors du traitement de la commande (TypeError)")

# CLI interactif. Peut être utilisé en même temps que Flask.
# Servira aussi pour journaliser les actions
def cli():
    z = True
    print("")
    print("Bienvenue sur l'interface en ligne de commandes de caveavin !")
    print("")
    print("Connecté en tant qu'utilisateur console. Toutes les permissions accordées")
    while z:
        print("")
        print("Voici les actions disponibles")
        print("")
        print("exit - Quitter le programme")
        print("bdd - Entrer en mode BDD pour intéragir avec la BDD")
        print("recreateuser - Recréer les utilisateurs Python à partir de la BDD")
        print("clearuser - Vider la liste d'utilisateurs locaux (n'agit pas sur la BDD)")
        print("register - Enregistrer un utilisateur dans le système")
        print("showuser - Voir la liste d'utilisateurs")
        print("")
        try:
            command = str(input("MainCLI# -> "))
            print("")
            if command == "exit" or command == "EXIT":
                print("Déconnexion !")
                z = False
            elif command == "register" or command == "REGISTER":
                login = str(input("Login -> "))
                nom = str(input("Nom -> "))
                prenom = str(input("Prénom -> "))
                passwd = getpass.getpass(prompt='Mot de passe -> ', stream=None)
                passwd = hash(passwd)
                inscription = str(date.today())
                new_user = Utilisateur(login,nom,prenom,passwd,inscription)
                ListeUtilisateurs.append(new_user)
                new_user.registerBDD()
            elif command == "showuser" or command == "SHOWUSER":
                if ListeUtilisateurs is None:
                    print("Aucun utilisateur n'existe dans la mémoire")
                    print("")
                    print("S'ils existent dans la BDD, lancez 'recreateuser'")
                else:
                    print(getAndTabulate(ListeUtilisateurs,Utilisateur))
            elif command == "bdd" or command == "BDD":
                bdd()
            elif command == "recreateuser" or command == "RECREATEUSER":
                result = recreateUsers()
                if result == 1:
                    print("Erreur lors du traitement de la commande (TypeError)")
                elif result == 2:
                    print("Aucun utilisateur présent dans la BDD")
                else:
                    recreateUsers()
            elif command == "clearuser" or command == "CLEARUSER":
                try:
                    ListeUtilisateurs.clear()
                    print("Liste d'utilisateurs locaux vidée !")
                    print("")
                    print("Pour ré-actualiser la liste d'utilisateurs locaux à partir de la BDD, lancez recreateuser")
                except TypeError as e:
                    print("Erreur lors de la vidange de la liste d'utilisateurs locaux")
            else:
                print("Commande inconnue")
        except TypeError as e:
            print("Erreur lors du traitement de la commande (TypeError)")
    print("Sortie du CLI")

recreateUsers()
cli()
exit(0)