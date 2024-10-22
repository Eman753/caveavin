# caveavin
Projet étudiant pour mettre en place un programme orienté objet, en Python, permettant d'enregistrer, consulter et gérer un stock de bouteilles de vins virtuel.

L'utilisation de ce programme se fait en CLI
Deux méthodes d'authentification peuvent s'utiliser :

-> console / pas de mot de passe -> accès "console" avec toutes les permissions.

-> utilisateur / mot de passe -> accès utilisateur (avec caves, étagères et bouteilles respectives).

En mode console, l'administrateur peut intéragir avec tous les objets, créer, supprimer, et lister les objets.
Le mode console met aussi à disposition un second CLI permettant d'intéragir directement avec la BDD.

Le mode utilisateur permet de créer, modifier et supprimer des objets dans des caves appartenant à l'utilisateur. L'accès direct au CLI BDD n'est pas disponible.

Au démarrage, le script récupère les objets enregistrés dans la BDD, et les sauvegarde sous forme d'objet. Les manipulations se font uniquement avec les objets Python.

L'authentification se réalise une fois la liste des utilisateurs avec leurs mots de passes respectifs hashés en SHA256, et une simple comparaison hash enregistré / hash du mot de passe entré.

Voici le schéma UML utilisé pour réaliser ce programme :

![UML](https://github.com/user-attachments/assets/f11d67d0-edf2-444b-b0e3-037e6e159f2b)

Voici le schéma de BDD employé dans la mise en place de ce programme :

![BDD](https://github.com/user-attachments/assets/071b7f87-aa07-46b6-8f3c-94ad4fa65abe)
