#!/usr/bin/python3

from cli import *
from web import *

# Main script of caveavin

if __name__ == "__main__":
    choice = str(input("Dans quel mode lancer l'application ? web/console -> "))
    if choice == "console":
        cli()
    elif choice == web:
        webapp()
    else:
        cli()

exit(0)