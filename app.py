# librerie
from flask import Flask, url_for, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

# inizializzazione
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.secret_key = 'super_secret_key'
db = SQLAlchemy(app)

# definizione di un account all'interno del database
class Account(db.Model):
    __tablename__ = 'users_collection'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.id

# inizializzazione database
with app.app_context():
    db.create_all()

# funzione bool che verifica se l'utente è registrato
def is_authenticated():
    return 'user_id' in session

# funzione che non consente all'utente di accedere a una pagina se non registrato
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            flash('You must be logged in to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# endpoint iniziale  
@app.route('/')
def dashboard():
    if not is_authenticated():
        return render_template('index.html',user=None)
    else:
        user = Account.query.get(session['user_id'])
        return render_template('index.html',user=user)
    
# endpoint del signup
@app.route('/signup', methods=['POST', 'GET']) # in realtà serve solo 'POST', ma per sicurezza metto sempre anche l'altro
def signup():
    if request.method == 'POST':
        new_email = request.form.get('email')
        new_password = request.form.get('password')
        new_password2 = request.form.get('password2')
        
        if not new_email or not new_password or not new_password2:
            flash('All fields are required!', 'danger')
            return redirect(url_for('signup'))
        if new_password != new_password2:
            flash('Passwords don\'t match!', 'danger')
            return redirect(url_for('signup'))
        if Account.query.filter_by(email=new_email).first() is not None:
            flash('E-Mail already registered! Please log in.', 'danger')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(new_password)
        new_user = Account(email=new_email, password=hashed_password)
        flash('Account created successfully!', 'success')
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = new_user.id
        return redirect('/')
    else:
        return render_template('signup.html')

# endpoint del login
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        new_email = request.form.get('email')
        new_password = request.form.get('password')   

        if not new_email or not new_password:
            flash('All fields are required!', 'danger')
            return redirect(url_for('login'))
        
        user = Account.query.filter_by(email=new_email).first()

        if user and check_password_hash(user.password, new_password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid e-mail or password!', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template('login.html')
    
# endpoint del logout
@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect('/')

# endpoint per cancellare un account
@app.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    user = Account.query.get(session['user_id'])
    if not user:
        flash('User not found.', 'danger')
        return redirect('/')
    db.session.delete(user)
    session.clear()
    db.session.commit()
    return redirect('/')

@app.route('/test-db')
def test_db():
    from sqlalchemy import text
    result = db.session.execute(text("SELECT COUNT(*) FROM users_collection"))
    count = result.fetchone()[0]
    path = db.engine.url.database
    return f"Righe nel database: {count}, Path: {path}"

if __name__ == "__main__":
    app.run(debug=True)