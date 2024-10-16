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
    
# Méthode appelée à la création de l'objet pour définir ses attributs
    def __init__(self,login,nom,prenom,passwd,inscription):
        self.login = login
        self.nom = nom
        self.prenom = prenom
        self.passwd = passwd
        self.inscription = inscription
        self.ListeBouteilles = []
        self.ListeArchives = []

# Méthode utilisée pour enregistrer l'objet sur la BDD
    def registerBDD(self):
        db = sql_conn()
        c = db.cursor()
        c.execute("insert into users values (DEFAULT,'"+self.login+"','"+self.nom+"','"+self.prenom+"','"+self.passwd+"','"+self.inscription+"');")
        db.commit()
        c.close()
        db.close()

# Méthode pour retourner les attributs de l'objet
    def getInfo(self):
        return self.login, self.nom, self.prenom, self.passwd, self.inscription, self.ListeBouteilles, self.ListeArchives

# Méthode pour retourner le nom d'un utilisateur
    def getName(self):
        return self.login

# Méthode pour rajouter une bouteille liée à l'utilisateur
    def appendBouteille(self,bouteille):
        self.ListeBouteilles.append(bouteille)

# Classe d'une cave
class Cave:

# Méthode appelée à la création de l'objet pour définir ses attributs
    def __init__(self,nom,nombrebouteilles):
        self.nom = nom
        self.nombrebouteilles = nombrebouteilles
        self.ListeEtageres = []

# Méthode pour retourner les attributs de l'objet
    def getInfo(self):
        return self.nom, self.nombrebouteilles

# Méthode pour récupérer seulement le nom
    def getName(self):
        return self.nom

# Méthode pour récupérer seulement la liste d'étagères
    def getEtageres(self):
        return self.ListeEtageres

# Méthode pour rajouter une étagère à la liste
    def appendEtagere(self,etagere):
        self.ListeEtageres.append(etagere)

# Méthode pour augmenter le compteur de bouteilles
    def appendBouteille(self):
        self.nombrebouteilles = self.nombrebouteilles+1

# Méthode pour remettre à zéro la liste d'étagères
    def clearEtagere(self):
        self.ListeEtageres = []

# Méthode pour retourner la liste de bouteilles
    def getBouteilles(self):
        liste = []
        for i in self.ListeEtageres:
            if isinstance(i,Etagere):
                print("C'est une étagère")
                liste.append(i.getBouteille())
        return liste
            

# Méthode utilisée pour enregistrer l'objet sur la BDD
    def registerBDD(self):
        db = sql_conn()
        c = db.cursor()
        c.execute("insert into caves values (DEFAULT,'"+self.nom+"',"+str(self.nombrebouteilles)+");")
        db.commit()
        c.close()
        db.close()

# Classe des étagères
class Etagere:

# Méthode appelée à la création de l'objet pour définir ses attributs
    def __init__(self,numero,emplacements,nombreBouteilles):
        self.numero = numero
        self.emplacements = emplacements
        self.nombreBouteilles = nombreBouteilles
        self.ListeBouteilles = []

# Méthode pour retourner les attributs de l'objet
    def getInfo(self):
        return self.numero,self.emplacements,self.nombreBouteilles,self.ListeBouteilles

    def getNumero(self):
        return self.numero

# Méthode pour rajouter une bouteille à l'étagère
    def appendBouteille(self,bouteille):
        self.nombreBouteilles = self.nombreBouteilles+1
        self.ListeBouteilles.append(bouteille)

# Méthode pour retourner la liste de bouteilles d'une étagère
    def getBouteille(self):
        return self.ListeBouteilles

# Méthode utilisée pour enregistrer l'objet sur la BDD
    def registerBDD(self,cave):
        db = sql_conn()
        c = db.cursor()
        c.execute("insert into etageres values (DEFAULT,"+str(cave)+","+str(self.numero)+","+str(self.emplacements)+","+str(self.nombreBouteilles)+");")
        db.commit()
        c.close()
        db.close()

class Bouteille:

# Méthode de départ pour les attributs
    def __init__(self,nom,domaine,type,annee,region,prix,commentaires):
        self.nom = nom
        self.domaine = domaine
        self.type = type
        self.annee = annee
        self.region = region
        self.prix = prix
        self.commentaires = commentaires
        self.notePerso = 0
        self.noteCommu = 0
        self.photo = ""

# Méthode pour définir la note perso
    def setNotePerso(self,note):
        self.notePerso = note

# Méthode pour renvoyer les informations
    def getInfo(self):
        return self.nom,self.domaine,self.type,self.annee,self.notePerso,self.noteCommu,self.region,self.prix,self.commentaires

    def registerBDD(self,cave,etagere,user):
        db = sql_conn()
        c = db.cursor()
        c.execute("insert into bouteilles values (DEFAULT,"+str(cave)+","+str(etagere)+","+str(user)+",DEFAULT,'"+self.nom+"','"+self.domaine+"','"+self.type+"',"+str(self.annee)+",'"+self.region+"',NULL,NULL,NULL,'"+self.prix+"','"+self.commentaires+"');")
        db.commit()
        c.close()
        db.close()

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
            print("Chargement utilisateurs OK !")
            return ListeUtilisateurs
        else:
            error = 2
            return error
    except TypeError as e:
        error = 1
        return error

# Fonction permettant de recréer les objets Python à partir des objets dans la BDD
def recreateCaves():
    error = 0
    ListeCaves.clear()
    try:
        db = sql_conn()
        c = db.cursor()
        c.execute("select nom,nombresBouteilles from caves;")
        result = c.fetchall()
        if result:
            for row in result:
                new_cave = Cave(row[0],row[1])
                ListeCaves.append(new_cave)
            c.close()
            db.close()
            print("Chargement caves OK !")
            return ListeCaves
        else:
            error = 2
            return error
    except Exception as e:
        error = 1
        return error

# Fonction permettant de recréer les objets Python à partir des objets dans la BDD
def recreateEtageres():
    error = 0
    try:
        db = sql_conn()
        c = db.cursor()
        c.execute("select cave,numero,emplacements,nombreBouteilles from etageres;")
        result = c.fetchall()
        if result:
            for i in result:
                c.execute("select nom from caves where id = "+str(i[0]))
                cave_nom = c.fetchone()[0]
                new_etagere = Etagere(i[1],i[2],i[3])
                for j in ListeCaves:
                    if isinstance(j,Cave):
                        if j.getName() == cave_nom:
                            j.appendEtagere(new_etagere)
            c.close()
            db.close()
            print("Chargement étagères OK !")
            return error
        else:
            error = 2
            c.close()
            db.close()
            return error
    except Exception as e:
        error = 1
        c.close()
        db.close()
        return error

def recreateBouteilles():
    error = 0
    try:
        db = sql_conn()
        c = db.cursor()
        c.execute("select cave,etagere,proprietaire,nom,domaine,type,annee,region,notePerso,noteCommu,prix,commentaires from bouteilles;")
        result = c.fetchall()
        if result:
            for i in result:
                c.execute("select nom from caves where id = "+str(i[0])+";")
                cave_nom = c.fetchone()[0]
                c.execute("select numero from etageres where id = "+str(i[1])+";")
                etagere = c.fetchone()[0]
                c.execute("select login from users where id = "+str(i[2])+";")
                user = c.fetchone()[0]
                new_bouteille = Bouteille(i[3],i[4],i[5],i[6],i[7],i[10],i[11])
                new_bouteille.setNotePerso(i[8])
                for search_cave in ListeCaves:
                    if isinstance(search_cave,Cave):
                        if search_cave.getName() == cave_nom:
                            liste_etagere = search_cave.getEtageres()
                            for search_etagere in liste_etagere:
                                if isinstance(search_etagere,Etagere):
                                    if search_etagere.getNumero() == etagere:
                                        if isinstance(new_bouteille,Bouteille):
                                            search_etagere.appendBouteille(new_bouteille)
                for search_user in ListeUtilisateurs:
                    if isinstance(search_user,Utilisateur):
                        if search_user.getName() == user:
                            search_user.appendBouteille(new_bouteille)
            print("Chargement bouteilles OK !")
            c.close()
            db.close()
            return error
    except Exception as e:
        print("Une erreur est survenue lors de la récupération des bouteilles depuis la BDD")
        error = 1
        c.close()
        db.close()
        return error

# Fonction générique pour afficher la liste des objets d'une classe
# Toutes les classes auront la même méthode getInfo permettant d'extraire les infos
def getAndTabulate(liste,objet):
    tableau = []
    if objet == "bouteille":
        headers = ["Nom","Domaine","Type","Année","Région","NotePerso","NoteCommu","Prix","Commentaires"]
        for i in liste:
            print("Ok je trouve la liste")
            print(liste)
            for j in i:
                print("Ok je trouve la liste de liste")
                if isinstance(j,Bouteille):
                    print("OK c'est une bouteille !")
                    tableau.append(j.getInfo())
                else:
                    print("Erreur bouteille")
    elif objet == "étagère":
        headers = ["Numéro","Emplacements totaux","Nombre de bouteilles présentes","Bouteilles"]
        for i in liste:
            if isinstance(i,Etagere):
                tableau.append(i.getInfo())
            else:
                print("Erreur étagère")
    else:
        for i in liste:
            if isinstance(i, objet):
                tableau.append(i.getInfo())  # Récupère les infos sous forme de tuple
        if objet == Utilisateur:
            headers = ["Login", "Nom", "Prénom", "Mot de passe hashé", "Date d'inscription"]
        elif objet == Cave:
            headers = ["Nom","Nombre de bouteilles"]
    return tabulate(tableau, headers=headers, tablefmt="grid")

# Fonction similaire à celle du dessus, mais va chercher dans la BDD
def getAndTabulateFromBDD(objet):
    db = sql_conn()
    c = db.cursor()
    tableau = []
    error = 0
    if objet == "user":
        c.execute("select id,login,nom,prenom,passwd,inscription from users")
        result = c.fetchall()
        if result:
            tableau = [list(row) for row in result]
            headers = ["ID","Login", "Nom", "Prénom", "Mot de passe hashé", "Date d'inscription"]
            c.close()
            db.close()
            return tabulate(tableau, headers=headers, tablefmt="grid")
        else:
            error = 2
            return error
    if objet == "cave":
        c.execute("select id,nom,nombresBouteilles from caves")
        result = c.fetchall()
        if result:
            tableau = [list(row) for row in result]
            headers = ["ID","Nom","Nombre de bouteilles"]
            c.close()
            db.close()
            return tabulate(tableau,headers=headers, tablefmt="grid")
    if objet == "étagère":
        c.execute("select id,cave,numero,emplacements,nombreBouteilles from etageres")
        result = c.fetchall()
        if result:
            tableau = [list(row) for row in result]
            headers = ["ID","Cave associée","Numéro d'étagère","Nombre d'emplacements de bouteilles","Nombres de bouteilles présentes"]
            c.close()
            db.close()
            return tabulate(tableau,headers=headers, tablefmt="grid")
    if objet == "bouteille":
        c.execute("select id,cave,etagere,proprietaire,archive,nom,domaine,type,annee,region,notePerso,noteCommu,photo,prix,commentaires from bouteilles")
        result = c.fetchall()
        if result:
            tableau = [list(row) for row in result]
            headers = ["ID","Cave associée","Numéro d'étagère associée","Propriétaire","Archive associée","Nom","Domaine","Type","Millésime","Région","Note du propriétaire","Note communautaire","Photo","Prix","Commentaire"]
            c.close()
            db.close()
            return tabulate(tableau,headers=headers, tablefmt="grid")
    else:
        error = 1
        return error

# Fonction permettant de vider une table de la BDD
def wipe(table):
    error = 0
    db = sql_conn()
    c = db.cursor()
    try:
        c.execute("delete from "+table)
        db.commit()
        c.close()
        db.close()
        return error
    except Exception as e:
        error = 1
        c.close()
        db.close()
        return error

# Fonction pour supprimer un objet de la BDD
def deleteFromBDD(id,table):
    error = 0
    db = sql_conn()
    c = db.cursor()
    try:
        c.execute("delete from "+table+" where id = "+str(id))
        db.commit()
        c.close()
        db.close
        return error
    except Exception as e:
        error = 1
        c.close()
        db.close()
        return error

# Second CLI interactif pour les interactions avec la BDD
# De cette manière, on différencie la gestion des objets Python, qui ne durent que le temps de fonctionnement du programme
# Et on différencie les objets stockés en BDD de manière persistente
def bdd():
    z = True
    print("")
    print("------------------------------------------------------")
    print("Bienvenue en mode BDD")
    print("------------------------------------------------------")
    print("")
    print("######################################################")
    print("Vous avez les pleins droits sur la BDD")
    print("Soyez prudent")
    print("######################################################")
    while z:
        print("")
        print("------------------------------------------------------")
        print("Voici les actions disponibles")
        print("------------------------------------------------------")
        print("")
        print("exit - Sortir du mode BDD")
        print("showuser - Liste les utilisateurs présents dans la BDD")
        print("wipeuser - SUPPRIMER L'ENTIERETE DES UTILISATEURS DE LA BDD")
        print("deleteuser - Supprimer un utilisateur grâce à son ID")
        print("showcave - Liste des caves présentes dans la BDD")
        print("wipecave - SUPPRIMER L'ENTIERETE DES CAVES DANS LA BDD")
        print("deletecave - Supprimer une cave grâce à son ID")
        print("showetagere - Liste des étagères présentes dans la BDD")
        print("wipeetagere - SUPPRIMER L'ENTIERETE DES ETAGERES DANS LA BDD")
        print("deleteetagere - Supprimer une étagère grâce à son ID")
        print("showbouteille - Liste des bouteilles présentes dans la BDD")
        print("wipebouteille - SUPPRIMER L'ENTIERETE DES BOUTEILLES DANS LA BDD")
        print("deletebouteille - Supprimer une bouteille grâce à son ID")
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
            elif command == "wipeuser" or command == "WIPEUSER":
                confirm = str(input("Êtes-vous sûr de votre choix ? y/N -> "))
                print("")
                if confirm == "y":
                    result = wipe("users")
                    if result == 1:
                        print("Une erreur est survenue pendant la remise à zéro de la table des utilisateurs")
                    else:
                        print("Table des utilisateurs vidée")
                else:
                    print("Opération annulée")
            elif command == "deleteuser" or command == "DELETEUSER":
                try:
                    id = int(input("Identifiant de l'utilisateur ? (Taper 0 pour annuler) -> "))
                    print("")
                    if id == 0:
                        print("Manipulation annulée")
                    else:
                        result = deleteFromBDD(id,"users")
                        if result == 1:
                            print("Une erreur est survenue pendant la suppression de l'utilisateur "+str(id))
                        else:
                            print("Suppression effectuée")
                except Exception as e:
                    print("Une erreur est survenue")
            elif command == "showcave" or command == "SHOWCAVE":
                result = getAndTabulateFromBDD("cave")
                if result == 1:
                    print("Une erreur a eu lieu pendant le traitement de la demande")
                elif result == 2:
                    print("Aucun objet n'a été trouvé dans la BDD")
                else:
                    print(result)
            elif command == "wipecave" or command == "WIPECAVE":
                confirm = str(input("Êtes-vous sûr de votre choix ? y/N -> "))
                print("")
                if confirm == "y":
                    result = wipe("caves")
                    if result == 1:
                        print("Une erreur est survenue pendant la remise à zéro de la table des caves")
                    else:
                        print("Table des caves vidée")
                else:
                    print("Opération annulée")
            elif command == "deletecave" or command == "DELETECAVE":
                try:
                    id = int(input("Identifiant de la cave ? (Taper 0 pour annuler) -> "))
                    print("")
                    if id == 0:
                        print("Manipulation annulée")
                    else:
                        result = deleteFromBDD(id,"caves")
                        if result == 1:
                            print("Une erreur est survenue pendant la suppression de la cave "+str(id))
                        else:
                            print("Suppression effectuée")
                except Exception as e:
                    print("Une erreur est survenue")
            elif command == "showetagere" or command == "SHOWETAGERE":
                result = getAndTabulateFromBDD("étagère")
                if result == 1:
                    print("Une erreur a eu lieu pendant le traitement de la demande")
                elif result == 2:
                    print("Aucun objet n'a été trouvé dans la BDD")
                else:
                    print(result)
            elif command == "wipeetagere" or command == "WIPEETAGERE":
                confirm = str(input("Êtes-vous sûr de votre choix ? y/N -> "))
                print("")
                if confirm == "y":
                    result = wipe("etageres")
                    if result == 1:
                        print("Une erreur est survenue pendant la remise à zéro de la table des étagères")
                    else:
                        print("Table des étagères vidée")
                else:
                    print("Opération annulée")
            elif command == "deleteetagere" or command == "DELETEETAGERE":
                try:
                    id = int(input("Identifiant de l'étagère' ? (Taper 0 pour annuler) -> "))
                    print("")
                    if id == 0:
                        print("Manipulation annulée")
                    else:
                        result = deleteFromBDD(id,"etageres")
                        if result == 1:
                            print("Une erreur est survenue pendant la suppression de l'étagère' "+str(id))
                        else:
                            print("Suppression effectuée")
                except Exception as e:
                    print("Une erreur est survenue")
            elif command == "showbouteille" or command == "SHOWBOUTEILLE":
                result = getAndTabulateFromBDD("bouteille")
                if result == 1:
                    print("Une erreur a eu lieu pendant le traitement de la demande")
                elif result == 2:
                    print("Aucun objet n'a été trouvé dans la BDD")
                else:
                    print(result)
            elif command == "wipebouteille" or command == "WIPEBOUTEILLE":
                confirm = str(input("Êtes-vous sûr de votre choix ? y/N -> "))
                print("")
                if confirm == "y":
                    result = wipe("bouteilles")
                    if result == 1:
                        print("Une erreur est survenue pendant la remise à zéro de la table des bouteilles")
                    else:
                        print("Table des bouteilles vidée")
                else:
                    print("Opération annulée")
            else:
                print("Commande inconnue")
        except TypeError as e:
            print("Erreur lors du traitement de la commande (TypeError)")

# CLI interactif. Peut être utilisé en même temps que Flask.
# Il n'y a pas de principe d'authentification en CLI, on est administrateur
# Servira aussi pour journaliser les actions
def cli():
    z = True
    print("")
    print("------------------------------------------------------------------------------------")
    print("Bienvenue sur l'interface en ligne de commandes de caveavin !")
    print("------------------------------------------------------------------------------------")
    print("")
    print("####################################################################################")
    print("Connecté en tant qu'utilisateur console. Toutes les permissions accordées")
    print("####################################################################################")
    while z:
        print("")
        print("Voici les actions disponibles")
        print("")
        print("exit - Quitter le programme")
        print("bdd - Entrer en mode BDD pour intéragir avec la BDD")
        print("recreateuser - Recréer les utilisateurs Python à partir de la BDD")
        print("recreatecave - Recréer les caves Python à partir de la BDD")
        print("recreateetagere - Recréer les étagères Python à partir de la BDD")
        print("clearuser - Vider la liste d'utilisateurs locaux (n'agit pas sur la BDD)")
        print("clearcave - Vider la liste de caves locales (n'agit pas sur la BDD)")
        print("clearetagere - Vider la liste des étagères locales (n'agit pas sur la BDD)")
        print("register - Enregistrer un utilisateur dans le système")
        print("showuser - Voir la liste d'utilisateurs")
        print("createcave - Créer une cave virtuelle")
        print("showcave - Lister les caves Python")
        print("createetagere - Créer une étagère")
        print("showetagere - Afficher les étagères présentes dans une cave")
        print("createbouteille - Rajouter une bouteille au système")
        print("showbouteille - Lister les bouteilles présentes dans une cave")
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
                print("Utilisateur créé !")
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
            elif command == "createcave" or command == "CREATECAVE":
                try:
                    nom = str(input("Nom de la cave -> "))
                    new_cave = Cave(nom,0)
                    ListeCaves.append(new_cave)
                    new_cave.registerBDD()
                    print("Cave créée !")
                except TypeError as e:
                    print("Erreur lors du traitement de la commande (TypeError)")
            elif command == "recreatecave" or command == "RECREATECAVE":
                result = recreateCaves()
                if result == 1:
                    print("Erreur lors du traitement de la commande (TypeError)")
                elif result == 2:
                    print("Aucune cave présent dans la BDD")
                else:
                    recreateCaves()
            elif command == "showcave" or command == "SHOWCAVE":
                if ListeUtilisateurs is None:
                    print("Aucune cave n'existe dans la mémoire")
                    print("")
                    print("S'ils existent dans la BDD, lancez 'recreatecave'")
                else:
                    print(getAndTabulate(ListeCaves,Cave))
            elif command == "clearcave" or command == "CLEARCAVE":
                try:
                    ListeCaves.clear()
                    print("Liste de caves locales vidée !")
                    print("")
                    print("Pour ré-actualiser la liste de caves locales à partir de la BDD, lancez recreatecave")
                except TypeError as e:
                    print("Erreur lors de la vidange de la liste de caves locales")
            elif command == "createetagere" or command == "createetagere":
                try:
                    cave_id = int(input("ID de la cave associée -> "))
                    numero = int(input("Numéro de l'étagère dans la cave -> "))
                    emplacements = int(input("Nombre d'emplacements totaux -> "))
                    db = sql_conn()
                    c = db.cursor()
                    c.execute("select nom from caves where id = "+str(cave_id))
                    cave = c.fetchone()[0]
                    c.close()
                    db.close()
                    new_etagere = Etagere(numero,emplacements,0)
                    new_etagere.registerBDD(cave_id)
                    for i in ListeCaves:
                        if isinstance(i,Cave):
                            if i.getName() == cave:
                                print(i.getName())
                                i.appendEtagere(new_etagere)
                    print("Etagère créée !")
                except Exception as e:
                    print("Erreur lors du traitement de la commande (Exception)")
            elif command == "showetagere" or command == "SHOWETAGERE":
                cave = str(input("Nom de la cave associée -> "))
                for i in ListeCaves:
                    if isinstance(i,Cave):
                        liste = []
                        if i.getName() == cave:
                            for j in i.getEtageres():
                                if isinstance(j,Etagere):
                                    liste.append(j)
                            print(getAndTabulate(liste,"étagère"))
            elif command == "recreateetagere" or command == "RECREATEETAGERE":
                result = recreateCaves()
                if result == 1:
                    print("Erreur lors du traitement de la commande (TypeError)")
                elif result == 2:
                    print("Aucune étagère présente dans la BDD")
                else:
                    recreateEtageres()
            elif command == "clearetagere" or command == "CLEARETAGERE":
                for i in ListeCaves:
                    if isinstance(i,Cave):
                        i.clearEtagere()
                print("Liste des étagères remises à zéro")
                print("")
                print("Pour recréer les objets étagères, vous pouvez lancer recreateetagere")
            elif command == "createbouteille" or command == "CREATEBOUTEILLE":
                try:
                    cave_id = int(input("ID de la cave associée -> "))
                    etagere_id = int(input("ID de l'étagère -> "))
                    user = str(input("Utilisateur propriétaire -> "))
                    nom = str(input("Nom de la bouteille -> "))
                    domaine = str(input("Domaine de la bouteille -> "))
                    type = str(input("Type de vin (rouge/rosé/blanc/gris/pinot/pétillant) -> "))
                    annee = int(input("Millésime -> "))
                    region = str(input("Région d'origine de la bouteille -> "))
                    notePerso = int(input("Note personnelle sur 20 -> "))
                    prix = str(input("Prix de la bouteille -> "))
                    commentaires = str(input("Commentaires (laisser vide pour aucun) -> "))
                    print("")
                    new_bouteille = Bouteille(nom,domaine,type,annee,region,prix,commentaires)
                    db = sql_conn()
                    c = db.cursor()
                    c.execute("select cave,numero,emplacements,nombreBouteilles from etageres;")
                    result = c.fetchall()
                    if result:
                        for i in result:
                            c.execute("select nom from caves where id = "+str(cave_id))
                            cave_nom = c.fetchone()[0]
                    else:
                        print("Erreur lors du traitement des caves")
                    for i in ListeCaves:
                        if isinstance(i,Cave):
                            if i.getName() == cave_nom:
                                liste = i.getEtageres()
                                print(liste)
                                for j in liste:
                                    print(j)
                                    if isinstance(j,Etagere):
                                        print(j.getNumero())
                                        if j.getNumero() == etagere_id:
                                            new_bouteille = Bouteille(nom,domaine,type,annee,region,prix,commentaires)
                                            if isinstance(new_bouteille,Bouteille):
                                                new_bouteille.setNotePerso(notePerso)
                                                j.appendBouteille(new_bouteille)
                                            else:
                                                print("Erreur de manipulation de la bouteille")
                                i.appendBouteille()
                        else:
                            print("Pas de cave trouvée")
                    for i in ListeUtilisateurs:
                        if isinstance(i,Utilisateur):
                            if i.getName() == user:
                                i.appendBouteille(new_bouteille)
                    c.execute("select id from users where login = '"+str(user)+"';")
                    result = c.fetchone()
                    if result:
                        user_id = result[0]
                    else:
                        print("Erreur lors de la récupération de l'ID utilisateur")
                    c.execute("select id from etageres where cave = "+str(cave_id)+";")
                    result = c.fetchone()
                    if result:
                        etagere_id = result[0]
                    else:
                        print("Erreur lors de la récupération de l'ID de l'étagère")
                    new_bouteille.registerBDD(cave_id,etagere_id,user_id)
                except Exception as e:
                    print("Erreur lors de la création de la bouteille")
                c.close()
                db.close()
            elif command == "showbouteille" or command == "SHOWBOUTEILLE":
                cave = str(input("Nom de la cave -> "))
                for i in ListeCaves:
                    if isinstance(i,Cave):
                        liste = []
                        if i.getName() == cave:
                            print(i.getName())
                            liste = i.getBouteilles()
                            print(getAndTabulate(liste,"bouteille"))
            else:
                print("Commande inconnue")
        except TypeError as e:
            print("Erreur lors du traitement de la commande (TypeError)")
    print("Sortie du CLI")

recreateUsers()
recreateCaves()
recreateEtageres()
recreateBouteilles()
cli()
exit(0)