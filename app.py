from flask import Flask, request, render_template, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG'] = True
app.debug = True
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()
print("")
@app.route('/')
def index():
    """Redirect to gameboard"""

    return redirect('/gameboard')

@app.route('/gameboard')
def load_game():
    """Set up game board and reset score and words_found list"""

    session['gameboard'] = boggle_game.make_board()
    session['score'] = 0
    session['words_found'] = []
    return render_template('gameboard.html', gameboard = session['gameboard'])

@app.route('/check', methods=['POST'])
def handle_check_request():
    """Handle the processing of a users guess to see if it's valid. If it is then
    increment the score and add the valid word to the words_found list so it can't be
    guessed again"""

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
    """This is run after the timer runs out in the game so that the session data
    can be updated. The number of games played and potentially the high score are updated."""

    if 'hi_score' not in session:
        session['hi_score'] = session['score']

    if session['hi_score'] < session['score']:
        session['hi_score'] = session['score']
        print(f"New high score reached!: {session['hi_score']}")
    
    if 'games_played' not in session:
        session['games_played'] = 0

    session['games_played'] += 1

    for key, value in session.items():
        print(f'{key}: {value}')

    return f"Number of games played: {session['games_played']}"

def check_dup_words(guess):
    """check to see if the user has already guessed the word in the same round."""
    
    if guess in session['words_found']:
        return True
    else:
        session['words_found'].append(guess)
        return False