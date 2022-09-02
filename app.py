from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from User import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, current_user, logout_user, login_user

app = Flask(__name__)


Users = [];

#user1 = User('zare@yahoo.com','ali',generate_password_hash('123',method='pbkdf2:sha256', salt_length=8))
user1 = User('zare@yahoo.com','ali','123',1)
Users.append(user1)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    for user in Users:
        if user.id == int(user_id):
            return user

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        # password = generate_password_hash(
        #     request.form.get('password'),
        #     method='pbkdf2:sha256',
        #     salt_length=8
        # )

        password = request.form.get('password')
        us = User(request.form["email"],request.form["name"], password)
        Users.append(us)

        login_user(us)

        return render_template("secrets.html", name = request.form["name"])

    else:
        return render_template("register.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        # password = generate_password_hash(
        #     request.form.get('password'),
        #     method='pbkdf2:sha256',
        #     salt_length=8
        # )
        password = request.form.get('password')

        email_found = False
        for user in Users:
            if user.Email == email:
                email_found = True

        if not email_found:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))

        logged_in = False
        for user in Users:
            if user.Email == email and user.Password == password:
                logged_in = True
                login_user(user)
        if logged_in:
            print("logged_in")
            return redirect(url_for('secrets'))
        else:
            flash('Password incorrect, please try again.')
            return render_template("login.html")

    else:
        return render_template("login.html")

@app.route('/secrets')
@login_required
def secrets():
    return render_template("secrets.html", name=current_user.Email, logged_in=True)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/download')
@login_required
def download():
    return send_from_directory(directory='static/files', path="cheat_sheet.pdf")

if __name__ == "__main__":
    app.run(debug=True)
