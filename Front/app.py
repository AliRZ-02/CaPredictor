# Import Statements
import math

import sqlalchemy
from Predictor import interactions
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///requests.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    photo = db.Column(db.String(200))
    nationality = db.Column(db.String(200))
    nationality_2 = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            player_name = request.form['player_name']
            contract_length = round(float(request.form['length']))
            resign_statement = request.form['resign']
        except:
            return redirect('/')
        if resign_statement == 'Re-sign':
            resign_statement = True
        else:
            resign_statement = False
        player_name = player_name.lower()
        if contract_length <= 1:
            contract_length = 1
        elif contract_length >= 8 and resign_statement is True:
            contract_length = 8
        elif contract_length >= 7 and resign_statement is False:
            contract_length = 7
        else:
            pass
        money = interactions.GetInfo(player_name, contract_length)
        value = money.automatic(resign_statement)
        if value != "No Player Found. Please try again using manual mode" \
                and value != "Such a player was not found. Try using manual mode":
            try:
                link = "http://nhl.bamcontent.com/images/headshots/current/168x168/" \
                       + value.split(":")[4] + ".jpg"
                nations = {"CAN": "CA", "USA": "US", "SWE": "SE", "RUS": "RU",
                           "FIN": "FI", "CZE": "CZ", "CHE": "CH", "DNK": "DK",
                           "DEU": "DE", "SVK": "SK", "AUT": "AT", "SVN": "SI",
                           "FRA": "FR", "NOR": "NO", "LVA": "LV", "AUS": "AU",
                           "NLD": "NL"}
                nation = nations[money.flag()].lower()
                flag = "https://flagcdn.com/w160/" + nation + ".png"
                flag2 = "https://flagcdn.com/w320/" + nation + ".png 2x"
                new_player = Todo(name=value, photo=link, nationality=flag, nationality_2=flag2)
                reduce_db()
                check_duplicates(new_player)
                db.session.add(new_player)
                db.session.commit()
                return redirect('/results')
            except:
                return "There was an error in searching the player. Please try again later"
        else:
            return redirect('/error')

    else:
        players = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('index.html', players= players)

@app.route('/results', methods=['POST', 'GET'])
def results():
    return index()

@app.route('/error', methods=['POST', 'GET'])
def error():
    return index()

@app.route('/manual', methods=['GET'])
def manual():
    return render_template('manual.html')

@app.route('/manual/forward', methods=['POST', 'GET'])
def forward():
    if request.method == 'POST':
        try:
            position = request.form['position']
            contract_length = round(float(request.form['length']))
            age = int(request.form['age'])
            resign_statement = request.form['resign']
            g82 = float(request.form['g82'])
            a82 = float(request.form['a82'])
            p82 = float(request.form['p82'])
        except:
            return redirect('/manual/forward')

        if position == 'RW':
            position = 'R'
        elif position == 'LW':
            position = 'L'
        else:
            pass

        if resign_statement == 'Re-sign':
            resign_statement = True
        else:
            resign_statement = False

        if contract_length <= 1:
            contract_length = 1
        elif contract_length >= 8 and resign_statement is True:
            contract_length = 8
        elif contract_length >= 7 and resign_statement is False:
            contract_length = 7
        else:
            pass

        money = interactions.GetInfo(player_name="User-Generated-F", length= contract_length)
        value = money.forward(position, age, g82, a82, p82, ppg=(p82/82))
        new_player = Todo(name=value)
        reduce_db()
        check_duplicates(new_player)
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/manual/forward/results')
        except:
            return "There was an error in searching the player. Please try again later"
    else:
        players = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('forward.html', players= players)

@app.route('/manual/forward/results', methods=['POST', 'GET'])
def f_seen():
    return forward()

@app.route('/manual/defence', methods=['POST', 'GET'])
def defence():
    if request.method == 'POST':
        try:
            gp = int(request.form['gp'])
            contract_length = round(float(request.form['length']))
            age = int(request.form['age'])
            resign_statement = request.form['resign']
            g82 = float(request.form['g82'])
            a82 = float(request.form['a82'])
            p82 = float(request.form['p82'])
            toi = float(request.form['toi'])
            toi_min = math.floor(toi)
            toi_sec = toi - toi_min
            toi = toi_min + ((toi_sec*100)/60)
            b82 = float(request.form['b82'])
            h82 = float(request.form['h82'])
            spct = float(request.form['spct'])
            spct = spct/100
        except:
            return redirect('/manual/defence')

        if resign_statement == 'Re-sign':
            resign_statement = True
        else:
            resign_statement = False

        if contract_length <= 1:
            contract_length = 1
        elif contract_length >= 8 and resign_statement is True:
            contract_length = 8
        elif contract_length >= 7 and resign_statement is False:
            contract_length = 7
        else:
            pass

        money = interactions.GetInfo("User-Generated-D", contract_length)
        value = money.defence(age, g82, a82, p82, (p82/82), b82, h82,
                              gp, toi, spct, resign_statement)
        new_player = Todo(name=value)
        reduce_db()
        check_duplicates(new_player)
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/manual/defence/results')
        except:
            return "There was an error in searching the player. Please try again later"
    else:
        players = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('defence.html', players= players)

@app.route('/manual/defence/results', methods=['POST', 'GET'])
def d_seen():
    return defence()

@app.route('/manual/goalie', methods=['POST', 'GET'])
def goalie():
    if request.method == 'POST':
        try:
            gp = int(request.form['gp'])
            contract_length = round(float(request.form['length']))
            age = int(request.form['age'])
            resign_statement = request.form['resign']
            gaa = float(request.form['gaa'])
            svpct = float(request.form['svpct'])
            winpct = float(request.form['winpct'])
        except:
            return redirect('/manual/defence')

        if resign_statement == 'Re-sign':
            resign_statement = True
        else:
            resign_statement = False

        if contract_length <= 1:
            contract_length = 1
        elif contract_length >= 8 and resign_statement is True:
            contract_length = 8
        elif contract_length >= 7 and resign_statement is False:
            contract_length = 7
        else:
            pass

        money = interactions.GetInfo("User-Generated-G", contract_length)
        value = money.goalie(age, gp, gaa, svpct, winpct, resign_statement)
        new_player = Todo(name=value)
        reduce_db()
        check_duplicates(new_player)
        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/manual/goalie/results')
        except:
            return "There was an error in searching the player. Please try again later"
    else:
        players = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('goalie.html', players= players)

@app.route('/manual/goalie/results', methods=['POST', 'GET'])
def g_seen():
    return goalie()

def reduce_db():
    players = Todo.query.order_by(Todo.date_created).all()
    if len(players) > 5:
        for player in players:
            if player.name == "User-Generated-F" or \
                player.name == "User-Generated-D" or \
                player.name == "User-Generated-G":
                    db.session.delete(player)
                    db.session.commit()
                    break
            else:
                pass
        players = Todo.query.order_by(Todo.date_created).all()
        if len(players) > 5:
            db.session.delete(players[0])
            db.session.commit()
    else:
        pass

def check_duplicates(content):
    players = Todo.query.order_by(Todo.date_created).all()
    for player in players:
        if content.name == player.name:
            db.session.delete(player)
            break
        else:
            pass

if __name__ == "__main__":
    app.run(debug=True)
