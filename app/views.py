from flask import render_template, redirect, url_for, request, flash, session
from app import app, db, models, admin
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import select, update, desc
from .models import Puzzle, User, AttemptsTable
from .forms import LoginForm, RegisterForm, PuzzleForm
import json, os
from flask_login import LoginManager

validWords = {}
guessedWords = []

login_manager = LoginManager()
login_manager.init_app(app)

#<input type="submit" class="submitButton btn btn-outline-primary" value="Log In" formaction="/login">
#from .forms import AssignmentForm

admin.add_view(ModelView(Puzzle, db.session))
admin.add_view(ModelView(User, db.session))

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
def index():
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is not None:
            if User.check_password(user, form.password.data):
                session["userId"] = user.userId
                next = request.args.get('next')
                return redirect(next or url_for('temp'))
        flash("Invalid Username or Password")
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existingUser = User.query.filter_by(username = form.username.data).first()
        if existingUser is None:
            if len(form.password.data) < 6:
                flash("Password must be 6 character or longer")
            else:
                newUser = User(username = form.username.data)
                User.set_password(newUser, form.password.data)
                db.session.add(newUser)
                db.session.commit()
                return redirect(url_for("login"))
        else:
            flash("Username already exists")
    return render_template("register.html", form = form)

@app.route("/logout")
def logout():
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    session.pop("userId", None)
    return redirect(url_for("login"))
        

@app.route('/selector_page', methods=['GET', 'POST'])
def temp():
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    global validWords
    currentDir = os.path.dirname(__file__)
    relPath = "static/words_dictionary.json"
    filePath = os.path.join(currentDir, relPath)
    with open(filePath) as wordFile:
        validWords = json.load(wordFile)
    puzzles = Puzzle.query.all()
    puzzleNum = len(puzzles)
    return (render_template("main.html", puzzleList = puzzles, puzzleNum = puzzleNum))

@app.route('/leaderboard_page/<int:puzzleId>')
def leaderboard(puzzleId):
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    users = []
    scores = []
    query = select(AttemptsTable).where(AttemptsTable.c.puzzleId == puzzleId).order_by(
        desc(AttemptsTable.c.score)).limit(10)
    attempts = db.session.execute(query)
    for i in attempts:
        users.append(User.query.filter_by(userId = i.userId).first().username)
        scores.append(i.score)
    return render_template("leaderboard.html", puzzleId = puzzleId,
                           users = users, scores = scores, num = len(users))

@app.route('/puzzle_page/<int:puzzleId>')
def renderPuzzle(puzzleId):
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    global guessedWords
    guessedWords = []
    puzzleWord = Puzzle.query.get(puzzleId).puzzleLetters
    return (render_template("puzzle.html", puzzleId = puzzleId, puzzleWord = puzzleWord, wordLen = len(puzzleWord)))

@app.route('/create_puzzle', methods = ['GET', 'POST'])
def createPuzzle():
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    session["userId"]
    form = PuzzleForm()
    if form.validate_on_submit():
        letters = form.letters.data.lower()
        if len(letters) > 4 and len(letters) < 11 and letters.isalpha():
            existingPuzzle = Puzzle.query.filter_by(puzzleLetters = letters).first()
            if existingPuzzle is None:
                newPuzzle = Puzzle(puzzleLetters = letters)
                db.session.add(newPuzzle)
                db.session.commit()
                return redirect(url_for("temp"))
            else:
                flash("puzzle already exists")
        else:
            flash("puzzle must be between 5 and 10 letters")
    return (render_template("puzzleform.html", form = form))

@app.route('/word_check', methods = ['POST'])
def checkWord():
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    global validWords
    global guessedWords
    wordData = json.loads(request.data)
    word = wordData.get("word")
    if len(word) > 2 and validWords.get(word) == 1 and word not in guessedWords:
        guessedWords.append(word)
        return json.dumps({'status': 'OK', 'valid': 'true'})
    else:
        guessedWords.append(word)
        return json.dumps({'status': 'OK', 'valid': 'false'})

@app.route("/submit_score", methods = ["POST"])
def submitScore():
    if "userId" not in session:
        flash("not logged in")
        return  redirect(url_for("login"))
    id = json.loads(request.data).get("puzzleId")
    newScore = json.loads(request.data).get("score")
    query = select(AttemptsTable).where((AttemptsTable.c.userId == session["userId"])
                   & (AttemptsTable.c.puzzleId == id))
    existingRecord = db.session.execute(query).first()
    if existingRecord:
        if existingRecord.score < newScore:
            updateQuery = update(AttemptsTable).where((AttemptsTable.c.userId == session["userId"])
                   & (AttemptsTable.c.puzzleId == id)).values(score = newScore)
            db.session.execute(updateQuery)
            db.session.commit()
    else:
        newAttempt = {"puzzleId": id, "userId": session["userId"], "score": newScore}
        db.session.execute(AttemptsTable.insert().values(newAttempt))
        db.session.commit()
    return json.dumps({"status": "OK"})

@app.route("/tester")
def test1():
    temp = User.query.filter_by(userId = session["userId"]).first().username
    return temp