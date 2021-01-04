# Import Statements
import joblib

class GetPrediction:
    def __init__(self, player, length, mode, age):
        self.player = player
        self.length = length
        self.mode = mode
        self.age = age
        self.error = "An error occurred. Check if all inputs have been entered correctly and please try again"
        if self.mode == 'G':
            self.group = ''
            self.bridge = ''
        elif self.age >= 27:
            self.group = 'O27-'
            self.bridge = ''
        elif self.length >= 4:
            self.group = 'U27-'
            self.bridge = 'L-'
        else:
            self.group = 'U27-'
            self.bridge = 'S-'
    def get_model(self):
        try:
            model = joblib.load('..\Models' + '\\' + self.mode + '-' + self.group + self.bridge + 'Model.joblib')
            return model
        except:
            return FileNotFoundError
    def get_pred(self, valuation):
        current = ""
        for character in valuation:
            if character == '[':
                pass
            elif character == ']':
                pass
            else:
                current = current + character
        value = round((float(current) * 81500000))
        return str(self.player) + " is worth approximately: $" + str(value)

    def forward(self, g82, a82, p82, ppg):
        try:
            model = self.get_model()
            prediction = model.predict([[self.length, self.age, g82, a82, p82, ppg]])
            return self.get_pred(str(prediction))
        except:
            return self.error + 'F'
    def defence(self, g82, a82, p82, ppg, b82, h82, gp, toi, spct):
        try:
            model = self.get_model()
            prediction = model.predict([[self.length, self.age, g82, a82, p82, ppg, b82, h82, gp, toi, spct]])
            return self.get_pred(str(prediction))
        except:
            return self.error + 'D'
    def goalie(self, gp, gaa, svpct, winpct):
        try:
            model = self.get_model()
            prediction = model.predict([[self.length, gp, gaa, svpct, winpct]])
            return self.get_pred(str(prediction))
        except NameError:
            return self.error + 'G'