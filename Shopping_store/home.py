
from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash,check_password_hash

from FLASKER.hello import Users

app = Flask(__name__)
app.secret_key = " "
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///shop.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True,nullable=False)
    password = db.Column(db.String(200), nullable = False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float, nullable = False)


@app.route('/')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)

@app.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method="sha256")
        new_user = Users(username=username,password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! you can now log in')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Login successful!')
            return redirect(url_for("home")) #added successful login
        flash('Invalid username or password') #message failure
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id',None)
    flash('You have been logged out..')
    return redirect(url_for('home'))

@app.route('/error')
def error():
    return render_template("404.html"),404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
