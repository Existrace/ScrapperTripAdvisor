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
list_formatLinksDone = []
# Chemin des deux fichiers CSV de liens
path_LinksNotDone = "/home/snourry/Documents/drive-download-20200106T103458Z-001/links_waitinglist.csv"
path_linksDone = "/home/snourry/Documents/drive-download-20200106T103458Z-001/linksDone.csv"
path_AllData = "/home/snourry/Documents/drive-download-20200106T103458Z-001/mailTripAdvisor_Paris.csv"

# Converti le fichier CSV des liens non parcourus en une liste
with open(path_LinksNotDone, 'r') as f:
    # Dans ce csv, on ne doit pas ignorer la première ligne
    reader = csv.reader(f)
    list_LinksNotDone = list(reader)

"""
for item in list_LinksNotDone:
    list_formatLinksDone.append(item)
"""
# CE CODE SEMBLE FONCTIONNER
for i in range(len(list_LinksNotDone)):
    for j in range(len(list_LinksNotDone[i])):
        list_formatLinksDone.append(list_LinksNotDone[i][j])

# Récupère le contenu du fichier CSV parcourus en une liste
with open(path_linksDone, 'r') as f:
    # Dans ce csv, on doit ignorer la première ligne
    next(f)
    for line in f:
        list_linksDone.append(line)

for item in list_linksDone:
    item.replace('\n', '')
    print("Le lien : " + item)

print("Il y a " + str(len(list_LinksNotDone)) + " liens à parcourir.")
print("Il y a " + str(len(list_linksDone)) + " liens déjà parcourus. \n")
print(list_formatLinksDone)

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
# MALGRER LE NOUVEAU TABLEAU FORMAT LINK DONE IL PARCOURS QUAND MEME LES LIENS DEJA FAIT? A VERIFIER ET CORRIGER
# CHANGER LA LECTURE DANS LIST LINK DONE EN REMPLACANT PAR FORMAT ???
print("Début du parcours des liens... (Chargement) \n")
nblink = 0
try:
    # Parcours des liens non parcouru
    for link in list_LinksNotDone:
        # Vérifier ici si link fait déjà parti des liens de list_LinksDone ?
        if link not in list_formatLinksDone:
            nblink = nblink + 1
            browser.get(link[0])
            time.sleep(3)
            print("Lien jamais exécuté. Execution du lien : " + str(link) + " \n")

            with open(path_AllData, 'a') as f:
                print("Ecriture des données du restaurant dans le fichier CSV...")
                writer = csv.writer(f)
                # Recupère directement les données et les écrit dans l'immédiat
                # Lien par lien
                writer.writerow(utils.scrap_data(browser))

            # Lien marqué comme lien effectué
            # Ajoute dans le fichier CSV des liens faits le liens courant
            with open(path_linksDone, 'a') as f:
                writer = csv.writer(f)
                # Ecrit directement le lien courant dans les liens effectués
                writer.writerow(link)
                # Lien à retirer dans la liste des liens non parcouru
                list_LinksNotDone.remove(link)
                # A voir quelle ligne garder entre celle au dessus et celle en dessous
            # list_linksDone.append(link)

            print("Le lien a été marqué comme effectué. \n")

        else:
            print("Le lien " + str(link) + " existe déjà dans le fichier linksDone.csv")


except KeyboardInterrupt:
    print("Interruption volontaire du script.")
    # Il faut convertir la liste des liens fait en CSV (LinkDone)
except Exception as e:
    logging.exception(e)
finally:

    print("Mise à jour du fichier des liens parcourus.)")
    df = pd.DataFrame(list_LinksNotDone)
    if df.to_csv(path_LinksNotDone, index=False, header=False, mode='w'):
        print('Ecriture dans le fichier CSV : ' + path_LinksNotDone)

print("Tâche terminée avec succès.")
