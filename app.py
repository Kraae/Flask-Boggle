from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
app.debug = True

toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Show board."""

    board = boggle_game.make_board()
    session['board'] = board
    hscore = session.get("hscore", 0)
    count = session.get("count", 0)

    return render_template("index.html", board=board,
                           hscore=hscore,
                           count=count)


@app.route("/check-word")
def check_word():
    """Check if word is in dictionary."""

    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})


@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update count, update high score if appropriate."""

    score = request.json["score"]
    hscore = session.get("hscore", 0)
    count = session.get("count", 0)

    session['count'] = count + 1
    session['hscore'] = max(score, hscore)

    return jsonify(brokeRecord=score > hscore)
