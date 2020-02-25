import csv
import logging
import time
import utils
import pandas as pd

"""
Parcours les liens récupérés par le script Crawler_page_TripAdvisor
Le fichier links_waitinglist.csv est utilisé comme file d'attente est ne doit pas être vide. 
Les liens ainsi parcouru seront transférés dans LinksDone.csv qui est un fichier csv immuable

Dans les liens des restaurants, on récupère les informations suivantes : 
- Nom du restaurant - Adresse postale - Numéro de téléphone - E-mail

"""

list_linksDone = []
list_LinksNotDone = []
list_linkToDelete = []
# Chemin des deux fichiers CSV de liens
path_LinksNotDone = "/home/snourry/Documents/drive-download-20200106T103458Z-001/links_waitinglist.csv"
path_linksDone = "/home/snourry/Documents/drive-download-20200106T103458Z-001/linksDone.csv"


# path_LinksNotDone = "/home/snourry/Documents/drive-download-20200106T103458Z-001/CsvToulouse/links_waitinglist.csv"
# path_linksDone = "/home/snourry/Documents/drive-download-20200106T103458Z-001/CsvToulouse/linksDone.csv"

# path_AllData = "/home/snourry/Documents/drive-download-20200106T103458Z-001/Bordeaux_TripAdvisor.csv"
path_AllData = "/home/snourry/Documents/drive-download-20200106T103458Z-001/CsvParis/Paris_TripAdvisor.csv"
# path_AllData = "/home/snourry/Documents/drive-download-20200106T103458Z-001/CsvToulouse/Toulouse_TripAdvisor.csv"
# Converti le fichier CSV des liens non parcourus en une liste
with open(path_LinksNotDone, 'r') as f:
    # next(f)
    for line in f:
        line = line.replace("\n", "")
        list_LinksNotDone.append(line)

try:
    # Récupère le contenu du fichier CSV parcourus en une liste
    with open(path_linksDone, 'r') as f:
        # next(f)
        for line in f:
            line = line.replace("\n", "")
            list_linksDone.append(line)

except FileNotFoundError:
    print("Le fichier LinksDone n'existe pas, donc aucun lien déjà parcouru.")

print("Il y a " + str(len(list_LinksNotDone)) + " lien(s) à parcourir.")
print("Il y a " + str(len(list_linksDone)) + " lien(s) déjà parcourus. \n ")

# Si la taille de la liste du fichier CSV est vide, renvoi une exception
if len(list_LinksNotDone) == 0:
    raise Exception("Le fichier CSV LinksNotDone ne doit pas être vide. Programme interrompu.")

# Récupère que les liens présents uniquement dans la liste "list_LinksNotDone"
# Ne prend donc pas en compte les liens dans les deux listes
# list_LinksToDo = set(list_LinksNotDone) - set(list_linksDone)

list_all_data = []  # Liste qui va contenir toutes les données finales

# Récupération du driver
# Récupère la configuration du browser (Chrome headless)
browser = utils.setUp()

print("Début du parcours des liens... \n")

nblink = 0
try:
    # Parcours des liens non parcouru
    for link in list_LinksNotDone:
        if link not in list_linksDone:

            print("Executer, le lien " + str(link) + " n'a jamais été parcouru")

            nblink = nblink + 1
            browser.get(link)
            time.sleep(1)
            print("Execution du lien N° " + str(nblink))

            with open(path_AllData, 'a') as file_1:
                print("Ecriture des données du restaurant dans le fichier CSV...")
                writer = csv.writer(file_1)
                # Recupère directement les données et les écrit dans l'immédiat
                # Lien par lien
                writer.writerow(utils.scrap_data(browser))

            # Lien marqué comme lien effectué
            # Ajoute dans le fichier CSV des liens faits le liens courant
            with open(path_linksDone, 'a') as file_2:
                writer = csv.writer(file_2)
                # Ecrit directement le lien courant dans les liens effectués
                writer.writerow([link])
                # Lien à retirer dans la liste des liens non parcouru
                # list_LinksNotDone.remove(link)
                # A voir quelle ligne garder entre celle au dessus et celle en dessous
                # list_linksDone.append(link)
                list_linkToDelete.append(link)

            print("Le lien a été marqué comme effectué. \n")

        else:
            print("Ne pas executer, le lien se trouve déjà dans les liens parcourus validés.")
            nblink = nblink + 1
            print("Execution du lien N° " + str(nblink))
            # list_LinksNotDone.remove(link)
            list_linkToDelete.append(link)

except KeyboardInterrupt:
    print("Interruption volontaire du script.")
# Il faut convertir la liste des liens fait en CSV (LinkDone)
except Exception as e:
    logging.exception(e)
finally:

    for item in list_linkToDelete:
        list_LinksNotDone.remove(item)

    print("Conversion en fichier CSV de lien non effectué (NotDone)")
    df = pd.DataFrame(list_LinksNotDone)
    if df.to_csv(path_LinksNotDone, header=False, index=False, mode='w'):
        print('Ecriture dans le fichier CSV : ' + path_LinksNotDone)

print("Tâche terminée avec succès.")
