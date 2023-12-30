from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG'] = True


boggle_game = Boggle()

@app.route('/')
def index():
    """Redirect to gameboard"""

    return redirect('/gameboard')

@app.route('/gameboard')
def load_game():
    gameboard = boggle_game.make_board()
    return render_template('gameboard.html', gameboard = gameboard)