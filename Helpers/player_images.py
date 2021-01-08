# Name: Ali Raza Zaidi
# Date: Jan 8 2021
# Purpose: Download all player images from NHL API. Due to issues, with heroku, the player images weren't loading and so
#          I had to download all the player images locally and connect them to index.html that way

# Import Statements
import requests
import csv

# Getting all of the players from the idList CSV file
reader = csv.reader(open('../Data/Players/idList.csv', 'r', encoding="ISO-8859-1"))
players = {}
name_list = []

# Creating a Dictionary with player names and the corresponding player ID's to access the NHL API
for name, id in reader:
    if name != 'Names':
        players[name] = id
        name_list.append(name)

# Downloading the player images locally
for player in players:
    image = requests.get("http://nhl.bamcontent.com/images/headshots/current/168x168/"
                         + str(players[player]) + ".jpg")
    download = open(str(players[player])+".jpg", "wb")
    download.write(image.content)
    download.close()