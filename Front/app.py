# Import Statements

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
        new_player = Todo(name=value)

        if value != "No Player Found. Please try again using manual mode" \
                and value != "Such a player was not found. Try using manual mode":
            try:
                db.session.add(new_player)
                db.session.commit()
                return redirect('/')
            except:
                return "There was an error in searching the player. Please try again later"
        else:
            return redirect('/')


    else:
        players = Todo.query.order_by(Todo.date_created.desc()).all()
        return render_template('index.html', players= players)

@app.route('/manual', methods=['POST', 'GET'])
def manual():
    if request.method == 'POST':
        player_name = request.form['player_name']
        new_player = Todo(name_manual="User Generated")

        try:
            db.session.add(new_player)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error in searching the player. Please try again later"
    else:
        players = Todo.query.order_by(Todo.date_created).all()
        return render_template('manual.html', players= players)

if __name__ == "__main__":
    app.run(debug=True)
