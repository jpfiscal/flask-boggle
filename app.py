from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG'] = True

boggle_game = Boggle()

@app.route('/')
def index():
    """Redirect to gameboard"""

    return redirect('/gameboard')

@app.route('/gameboard')
def load_game():
    session['gameboard'] = boggle_game.make_board()
    session['score'] = 0
    session['words_found'] = []
    return render_template('gameboard.html', gameboard = session['gameboard'])

@app.route('/check', methods=['POST'])
def handle_check_request():
    data = request.json
    value = data['guess']
    guess_result = boggle_game.check_valid_word(session['gameboard'],value)
    
    if guess_result == "ok":
        if not check_dup_words(value):
            session['score'] += len(value)
        else:
            guess_result = "duplicate"
            #if the guess is a duplicate in the list of found words then overwrite result to "duplicate"
        
    check_result = {"result": guess_result, "score": session['score']}
    return jsonify(check_result)

@app.route('/finalize_game', methods=['POST'])
def end_game():
    if 'hi_score' not in session:
        session['hi_score'] = session['score']

    if session['hi_score'] < session['score']:
        session['hi_score'] = session['score']
        print(f"New high score reached!: {session['hi_score']}")
    
    if 'games_played' not in session:
        session['games_played'] = 0

    session['games_played'] += 1
    return f"Number of games played: {session['games_played']}"

def check_dup_words(guess):
    if guess in session['words_found']:
        return True
    else:
        session['words_found'].append(guess)
        return False