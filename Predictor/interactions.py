# Import Statements
import csv
import requests
import predictor
from difflib import get_close_matches

class GetInfo:
    def __init__(self, player_name, length):
        self.player_name = player_name
        self.length = length
    def automatic(self, resign=True, attempts=0):
        if resign == False:
            self.length = self.length * (8/7)
        reader = csv.reader(open('..\Data\Players\idList.csv'))
        players={}
        name_list = []
        for name, id in reader:
            if name != 'Names':
                players[name] = id
                name_list.append(name)
        try:
            matches = get_close_matches(self.player_name, name_list, n=5)
            player_id = players[matches[attempts]]
        except:
            return "No Player Found. Please try again using manual mode"
        try:
            player_stats = requests.get("https://statsapi.web.nhl.com/api/v1/people/"
                                       +str(player_id)+
                                       "/stats?stats=statsSingleSeason&season=20192020")
            player_data = requests.get("https://statsapi.web.nhl.com/api/v1/people/" +str(player_id))
        except:
            if attempts <= 3:
                return self.automatic(self.player_name, self.length, attempts=attempts+1)
            else:
                return "Such a player was not found. Try using manual mode"
        position = player_data.json()['people'][0]["primaryPosition"]["code"]
        age = player_data.json()['people'][0]['currentAge']
        stats = player_stats.json()['stats'][0]['splits'][0]['stat']
        get_pred = predictor.GetPrediction(matches[attempts], self.length, position, age)
        if position == 'L' or position == 'R' or position == 'C' or position == 'D':
            g82 = (stats['goals'] / stats['games']) * 82
            a82 = (stats['assists'] / stats['games']) * 82
            p82 = (stats['points'] / stats['games']) * 82
            ppg = (stats['points'] / stats['games'])
        else:
            pass
        gp = (stats['games'])
        if gp < 70:
            gp = (gp / 70) * 82
        else:
            gp = 82
        if position == 'L' or position == 'R' or position == 'C':
            valuation = get_pred.forward(g82,a82,p82,ppg)
            return valuation
        elif position == 'D':
            b82 = (stats['blocked'] / stats['games']) * 82
            h82 = (stats['hits'] / stats['games']) * 82
            toi_original = (stats['timeOnIcePerGame'])
            index=0
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
        if not resign:
            self.length = self.length * (8/7)
        algorithm = predictor.GetPrediction(self.player_name, self.length, position, age)
        prediction = algorithm.forward(g82,a82,p82,ppg)
        return prediction
    def defence(self, age, g82, a82, p82, ppg, b82, h82, gp, toi, spct, resign=True):
        if not resign:
            self.length = self.length * (8/7)
        algorithm = predictor.GetPrediction(self.player_name, self.length, 'D', age)
        prediction = algorithm.defence(g82,a82,p82,ppg,b82,h82,gp,toi,spct)
        return prediction
    def goalie(self, age, gp, gaa, svpct, winpct, resign = True):
        if not resign:
            self.length = self.length * (8/7)
        algorithm = predictor.GetPrediction(self.player_name, self.length, 'G', age)
        prediction = algorithm.goalie(gp, gaa, svpct, winpct)
        return prediction