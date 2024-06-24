from flask import Flask, render_template, redirect, request, session
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'

WINNING_GOLD = 500
MAX_MOVES = 15

@app.route('/')
def index():
    if 'gold' not in session:
        session['gold'] = 0
    if 'activities' not in session:
        session['activities'] = []
    if 'moves' not in session:
        session['moves'] = 0
    if 'game_over' not in session:
        session['game_over'] = False

    return render_template('index.html', gold=session['gold'], activities=session['activities'], moves=session['moves'], game_over=session['game_over'],winning_gold=WINNING_GOLD,max_moves=MAX_MOVES)

@app.route('/process_money', methods=['POST'])
def process_money():
    building = request.form['building']
    gold_earned = 0

    buildings_gold = {
        'farm': random.randint(10, 20),
        'cave': random.randint(5, 10),
        'house': random.randint(2, 5),
        'casino': random.randint(-50, 50)
    }

    gold_earned = buildings_gold.get(building, 0)
    session['gold'] += gold_earned
    session['moves'] += 1

    # Create activity entry
    if gold_earned >= 0:
        activity = f"Earned {gold_earned} gold from the {building}! ({datetime.now().strftime('%m/%d/%Y, %H:%M:%p')})"
        color = "green"
    else:
        activity = f"Lost {abs(gold_earned)} gold at the {building}... Ouch! ({datetime.now().strftime('%m/%d/%Y, %H:%M:%p')})"
        color = "red"

    session['activities'].insert(0, {'activity': activity, 'color': color})

    # Check for win/lose conditions
    if session['gold'] >= WINNING_GOLD or session['moves'] >= MAX_MOVES:
        session['game_over'] = True

    return redirect('/')

@app.route('/reset')
def reset():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
