from flask import Flask, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from templates.shota import quotes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'projectkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite'
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(25), nullable=False)

# db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        checking_users_existing = Users.query.filter_by(username=username).first()
        checking_password_existing = Users.query.filter_by(password=password).first()

        if checking_users_existing and checking_password_existing:
            session['username'] = username
            return render_template('user.html')
        elif username == '' or password == '':
            flash('Please fill all required fields', 'error')
        elif not checking_password_existing:
            flash('Incorrect password', 'error')
        else:
            flash('We cant find a user with that username', 'error')

    return render_template('login.html')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['input_username']
        password = request.form['input_password']
        second_password = request.form['input_password_two']
        if username == '' or password == '' or second_password == '':
            flash('Please fill all required fields', 'error')
        elif password != second_password:
            flash("Passwords doesn't match", 'error')
        else:
            db.session.add(Users(username=username, password=password))
            db.session.commit()
            flash("Account is succesfully crated.", 'success')
    return render_template('signup.html')


@app.route('/user')
def user():
    return render_template('user.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')


@app.route('/generator')
def generator():
    quote = quotes()
    return render_template('generator.html', quote=quote)


if __name__ == '__main__':
    app.run(debug=True)
