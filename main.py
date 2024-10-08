#!/usr/bin/python3

# Main script of caveavin

import pymysql
import flask
import csv


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
        print("")
        try:
            command = str(input("Commande -> "))
            print("")
            if command == "exit" or command == "EXIT":
                print("Déconnexion !")
                c = False
            else:
                print("Commande inconnue")
        except TypeError as e:
            print("Erreur lors du traitement de la commande (TypeError)")
    print("Sortie du CLI")

cli()
exit(0)