from flask import Flask, render_template, url_for, redirect, flash, request, \
    session  # url_for lets us see the pages without having to change the url each time
# by using the url_for we now have two "buttons" that let us choose if we want ot login or register

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
# we will use SQL to have a database and use SQLAlchemy to connect to this and we will have a table where the user data will be stored
# (their username and password)
# we will check if they have a username and then check for their password

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
# Bcrypt will check the password

import pandas as pd
from datetime import datetime

from flask_migrate import Migrate

from flask import Flask, render_template, url_for, redirect, flash, request, session, abort

db = SQLAlchemy()  # creating the database
app = Flask(__name__)  # http://127.0.0.1:8000/ <- use this to see the website
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # connects our app file to the database
app.config['SECRET_KEY'] = 'thisisasecretkey'  # secret key to secure the session cookie

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'




@login_manager.user_loader  # used to reload the user object
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):  # the table for our database with three columns
    id = db.Column(db.Integer, primary_key=True)  # id column
    username = db.Column(db.String(20), nullable=False,
                         unique=True)  # user's name has max 20 characters, and it should be unique
    password = db.Column(db.String(80),
                         nullable=False)  # username has max 20 characters, nullable=False means that it can't be empty


class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})  # storing the username

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})  # storing the password
    # max number of characters for our password is 20
    submit = SubmitField('Register')

    def validate_username(self, username):  # checks if the username already exists
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')


# Database initialization code
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('home.html')  # returns content in the home file


# Created dictionaries from which we will choose which message to display based on the user and password typed
login_messages = {
    'success': "Welcome back, {}!",  # if the username matches the password (username inside the curly brackets)
    'wrong_password': "Incorrect password, please try again.",  # if the password is wrong
    'unregistered_username': "That username is not registered."  # if the username doesn't exist
}

# Greeting based on the time of day
time_based_greetings = {
    'morning': "Rise and shine, {}!",  # if it is in the morning
    'afternoon': "Hello there, {}!",  # if it is in the afternoon
    'evening': "Good evening, {}!",  # if it is in the evening
    'night': "Hey, night owl {}!"  # if it is in the night
}


@app.route('/login', methods=['GET', 'POST'])  # linking the page to our app
def login():
    form = LoginForm()  # an instance of our flask class LoginForm
    if form.validate_on_submit():  # if the form has been submitted
        user = User.query.filter_by(
            username=form.username.data).first()  # searches in our database for the username and password and returns it if found,or None if not found
        if user:  # if the username inputted actually exists
            if bcrypt.check_password_hash(user.password,
                                          form.password.data):  # if the password inputted and the one we have stored match
                login_user(user)  # then we login the user

                # Getting the current time
                current_hour = datetime.now().hour  # current hour
                greeting = "Hello"  # this will change depending on the time of day

                # Choosing the greeting depending on the time of day using the previously defined dictionary
                if 5 <= current_hour < 12:
                    greeting = time_based_greetings['morning']
                elif 12 <= current_hour < 17:
                    greeting = time_based_greetings['afternoon']
                elif 17 <= current_hour < 21:
                    greeting = time_based_greetings['evening']
                else:
                    greeting = time_based_greetings['night']

                flash(greeting.format(
                    user.username))  # Use flash to display the message and user.username to put the user's name in our greeting
                return redirect(url_for('start'))  # after the login, the user is sent to the index file
            else:
                flash(login_messages[
                          'wrong_password'])  # if the password is not corect then a warning message is displayed
        else:
            flash(login_messages[
                      'unregistered_username'])  # if the username inputted does not exist a warning message is displayed

    return render_template('login.html', form=form)  # returns the login page


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():  # whenever we submit this form a hashed version of that password will be created
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        print(f"Form data: {form.data}")
        db.session.add(new_user)
        print(f"Before commit: {db.session.query(User).all()}")
        db.session.commit()  # Commit the changes to the database
        print(f"After commit: {db.session.query(User).all()}")
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

def load_questions_by_difficulty(file_path, selected_year, selected_subject):
    try:
        df = pd.read_excel(file_path)
        filtered_df = df[(df['Year'] == int(selected_year)) & (df['Subject'] == selected_subject)]
        questions_by_difficulty = {}
        for difficulty in ['Easy', 'Medium', 'Hard']:
            questions = filtered_df[filtered_df['Difficulty'] == difficulty][['Question', 'Answer']].values.tolist()
            questions_by_difficulty[difficulty] = questions
        return questions_by_difficulty
    except Exception as e:
        print(f"Error loading questions from Excel: {e}")
        return {}


@app.route('/startt', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        session.clear()  # Clearing any existing session data
        flash("Session data cleared.")  # Optional: flash a message when session is cleared
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_questions():
    year = request.form.get('year')
    starting_level = request.form.get('level')
    subject = request.form.get('subject')
    all_questions = load_questions_by_difficulty(
        r"C:\Users\saxod\OneDrive\Bureau\algorithms project\algorithm questions.xlsx", year, subject)

    session['all_questions'] = all_questions
    session['current_level'] = starting_level
    session['current_index'] = 0  # Index for the current level
    session['user_performance'] = {'correct_streak': 0, 'incorrect_streak': 0}
    return redirect('/question')


@app.route('/question', methods=['GET', 'POST'])
def question():
    if 'current_index' not in session:
        return redirect('/startt')

    current_level = session['current_level']
    questions_and_answers = session['all_questions'][current_level]
    current_index = session['current_index']

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        correct_answer = questions_and_answers[current_index][1]
        is_correct = str(correct_answer).strip().lower() == str(user_answer).strip().lower()


        # Update user performance
        if is_correct:
            session['user_performance']['correct_streak'] += 1
            session['user_performance']['incorrect_streak'] = 0
        else:
            session['user_performance']['correct_streak'] = 0
            session['user_performance']['incorrect_streak'] += 1

        # Check if level needs to be changed
        if session['user_performance']['correct_streak'] == 2:
            # Increase difficulty
            current_level = increase_level(current_level)
            session['current_level'] = current_level
            session['current_index'] = 0
            session['user_performance']['correct_streak'] = 0
        elif session['user_performance']['incorrect_streak'] == 5:
            # Decrease difficulty
            current_level = decrease_level(current_level)
            session['current_level'] = current_level
            session['current_index'] = 0
            session['user_performance']['incorrect_streak'] = 0
        else:
            # Move to the next question in the current level
            session['current_index'] += 1
            result = render_template('answer.html', question=questions_and_answers[current_index][0],
                                     user_answer=user_answer, correct_answer=correct_answer, is_correct=is_correct,
                                     correct_streak=session['user_performance']['correct_streak'])
            return result
        return redirect('/question')



    # Display the question
    if current_index < len(questions_and_answers):
        return render_template('question.html', question=questions_and_answers[current_index][0], index=current_index,
                               current_level=current_level, correct_streak=session['user_performance']['correct_streak'])
    else:
        # No more questions in the current level
        return render_template('level_complete.html', current_level=current_level)


def increase_level(current_level):
    levels = ['Easy', 'Medium', 'Hard']
    current_index = levels.index(current_level)
    return levels[min(current_index + 1, len(levels) - 1)]

def decrease_level(current_level):
    levels = ['Easy', 'Medium', 'Hard']
    current_index = levels.index(current_level)
    return levels[max(current_index - 1, 0)]


if __name__ == "__main__":  # Errors will show immediately
    app.run(debug=True, port=8000)

class User(db.Model, UserMixin):
    # ... existing fields ...
    lives = db.Column(db.Integer, default=3)  # New field for tracking lives

def decrement_lives(user_id):
    user = User.query.get(user_id)
    if user.lives > 0:
        user.lives -= 1
        db.session.commit()
        if user.lives == 0:
            # Add logic to enforce 15-minute wait
            pass

def can_continue(user_id):
    user = User.query.get(user_id)
    if user.lives > 0:
        return True
    else:
        # Add logic to check if 15 minutes have passed
        # Return True if the user can continue, False otherwise
        pass




app = Flask(_name_)


# ... other configurations and imports

# Assuming a User model exists; Adding a 'lives' attribute as a placeholder
class User(UserMixin, db.Model):
    # ... other fields
    lives = db.Column(db.Integer, default=3)  # Default lives set to 3


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    user = User.query.get(current_user.id)
    if user.lives <= 0:
        flash('No more lives left. Try again later!', 'danger')
        return redirect(url_for('dashboard'))  # Redirecting to dashboard when lives are exhausted

    if request.method == 'POST':
        # Process the user's answer
        # Placeholder for answer checking logic
        is_correct = check_answer(request.form['answer'])

        if is_correct:
            flash('Correct!', 'success')
            # Logic for correct answer (e.g., proceed to next question, increase score)
        else:
            user.lives -= 1
            db.session.commit()
            flash('Incorrect. Lives left: {}'.format(user.lives), 'danger')

        return redirect(url_for('next_question'))  # Redirect to the next question

    # If GET request, render the game page
    return render_template('game.html', user=user)


# Placeholder function for checking answers
def check_answer(answer):
    # Implement the logic to check the answer
    return True  # Placeholder return

@app.route('/results', methods=['GET', 'POST'])
@login_required
def show_results():
    user = User.query.get(current_user.id)
    score = get_user_score(user.id)  # Placeholder for getting the user's score

    if request.method == 'POST':
        choice = request.form.get('choice')
        if choice == 'continue':
            return redirect(url_for('game'))  # Redirecting to game page to continue playing
        elif choice == 'exit':
            return redirect(url_for('dashboard'))  # Redirecting to dashboard or any other page for exit

    return render_template('results.html', score=score)

# Placeholder function to get user's score
def get_user_score(user_id):
    # Implement the logic to calculate and return the user's score
    return 100  # Placeholder return
# credits: https://youtu.be/71EU8gnZqZQ?si=Fi7LpJfuiMqHsvbI



