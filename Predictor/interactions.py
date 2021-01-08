# Name: Ali Raza Zaidi
# Date: Jan 8 2021
# Purpose: Accesses the prediction models and returns the given prediction based
# on the input information and player position

# Import Statements
import csv
import requests
from Predictor import predictor
from difflib import get_close_matches

# Main Class - Wanted to incorporate OOP Principles to make program more elegant and easier to use


class GetInfo:
    def __init__(self, player_name, length):
        # All Methods will take in the Player Name and The Contract Length for their contract predictions
        self.player_name = player_name
        self.length = length

    def automatic(self, resign=True):
        # Automatic Mode uses the NHL API to find the value of the player's contract. It uses the player name
        # input from the user and finds the closest match amongst the list of 1090 active NHL player and uses
        # said player's id to access the NHL API and find their stats

        # Due to the way the NHL CBA is laid out, Free-Agents can only sign for a maximum of 7 Years with their
        # New teams while Re-signing players can sign for up to 8, hence why the adjustments have to be made
        if resign is False:
            self.length = self.length * (8/7)

        player_id = self.__id()

        # Tries to access the NHL API using the private method that allows for getting the closest ID Match
        # Alerts the user if no valid player ID is found
        try:
            player_stats = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(player_id) +
                                       "/stats?stats=statsSingleSeason&season=20192020")
            player_data = requests.get("https://statsapi.web.nhl.com/api/v1/people/" + str(player_id))
        except:
                return "Such a player was not found. Try using manual mode"

        # Uses the JSON Data from the API to find the stats need to calculate the prediction
        try:
            position = player_data.json()['people'][0]["primaryPosition"]["code"]
            age = player_data.json()['people'][0]['currentAge']
            name = player_data.json()['people'][0]['fullName']
            stats = player_stats.json()['stats'][0]['splits'][0]['stat']
        except:
            return "Such a player was not found. Try using manual mode"

        # Using the Predictor Module, Sets up a GetPrediction object to find the player prediction and
        # calls the required module based on the given position
        get_pred = predictor.GetPrediction(name, self.length, position, age, resign, player_id)

        if position == 'L' or position == 'R' or position == 'C' or position == 'D':
            g82 = (stats['goals'] / stats['games']) * 82
            a82 = (stats['assists'] / stats['games']) * 82
            p82 = (stats['points'] / stats['games']) * 82
            ppg = (stats['points'] / stats['games'])
        else:
            pass

        # Finds GP Stat, which is needed for Goalie and Defence predictions
        gp = (stats['games'])
        if gp < 70:
            gp = (gp / 70) * 82
        else:
            gp = 82

        # Returns valuation for Forwards, Defencemen and Goalies based on Prediction model and stats from the API
        if position == 'L' or position == 'R' or position == 'C':
            valuation = get_pred.forward(g82,a82,p82,ppg)
            return valuation
        elif position == 'D':
            b82 = (stats['blocked'] / stats['games']) * 82
            h82 = (stats['hits'] / stats['games']) * 82
            toi_original = (stats['timeOnIcePerGame'])
            index = 0

            for char in toi_original:
                if char == ':':
                    break
                else:
                    index = index+1

            minutes = int(toi_original[:index])
            seconds = int(toi_original[index+1:]) / 60
            toi = minutes+seconds
            spct = int(stats['shotPct']) / 100
            valuation = get_pred.defence(g82, a82, p82, ppg, b82, h82, gp, toi, spct)
            return valuation
        elif position == 'G':
            gaa = (stats['goalAgainstAverage'])
            svpct = (stats['savePercentage'])
            winpct = (stats['wins'] / stats['games'])
            valuation = get_pred.goalie(gp, gaa, svpct, winpct)
            return valuation
        else:
            return "No player valuation could be found. Try again using manual mode"

    def forward(self, position, age, g82, a82, p82, ppg, resign=True):
        # For Manual Mode, uses input stats to find determine valuation from prediction model
        # Length changes made due to CBA restrictions
        if not resign:
            self.length = self.length * (8/7)

        algorithm = predictor.GetPrediction(self.player_name, self.length, position, age, resign)
        prediction = algorithm.forward(g82, a82, p82, ppg)
        return prediction

    def defence(self, age, g82, a82, p82, ppg, b82, h82, gp, toi, spct, resign=True):
        # For Manual Mode, uses input stats to find determine valuation from prediction model
        # Length changes made due to CBA restrictions
        if not resign:
            self.length = self.length * (8/7)
        algorithm = predictor.GetPrediction(self.player_name, self.length, 'D', age, resign)
        prediction = algorithm.defence(g82, a82, p82, ppg, b82, h82, gp, toi, spct)
        return prediction

    def goalie(self, age, gp, gaa, svpct, winpct, resign=True):
        # For Manual Mode, uses input stats to find determine valuation from prediction model
        # Length changes made due to CBA restrictions
        if not resign:
            self.length = self.length * (8/7)
        algorithm = predictor.GetPrediction(self.player_name, self.length, 'G', age, resign)
        prediction = algorithm.goalie(gp, gaa, svpct, winpct)
        return prediction

    def __id(self):
        # Uses the player's name and finds the corresponding Player ID given a CSV file containing both
        reader = csv.reader(open('Data/Players/idList.csv', 'r', encoding="ISO-8859-1"))
        players = {}
        name_list = []

        for name, id in reader:
            if name != 'Names':
                players[name] = id
                name_list.append(name)

        # Uses the difflib library to find the closest name match to the input name
        try:
            matches = get_close_matches(self.player_name, name_list, n=5)
            return players[matches[0]]
        except:
            return "No Player Found. Please try again using manual mode"

    def flag(self):
        # uses the player ID to find the nationality of the player to add their country's flag to the website
        player_id = self.__id()
        try:
            player_data = requests.get\
                ("https://statsapi.web.nhl.com/api/v1/people/"
                 + str(player_id))
        except:
            return "Such a player was not found. Try using manual mode"
        return player_data.json()['people'][0]['nationality']
