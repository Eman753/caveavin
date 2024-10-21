#!/usr/bin/python3

from cli import *
from flask import Flask,render_template

# Script principal de caveavin

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("templates/base.html")

if __name__ == "__main__":
    choice = str(input("Dans quel mode lancer l'application ? web/console -> "))
    print("")
    if choice == "console":
        init_cli()
    elif choice == "web":
        ip_address = str(input("Adresse IP du serveur -> "))
        print("")
        print("Activation du serveur web")
        app.run(host=ip_address, port=5001)
    else:
        init_cli()


exit(0)