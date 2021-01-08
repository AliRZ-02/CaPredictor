import requests
import csv

reader = csv.reader(open('../Data/Players/idList.csv', 'r', encoding="ISO-8859-1"))
players = {}
name_list = []
for name, id in reader:
    if name != 'Names':
        players[name] = id
        name_list.append(name)

for player in players:
    image = requests.get("http://nhl.bamcontent.com/images/headshots/current/168x168/"
                         + str(players[player]) + ".jpg")
    download = open(str(players[player])+".jpg", "wb")
    download.write(image.content)
    download.close()