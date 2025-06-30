import sqlite3
from flask import Blueprint, current_app, g, jsonify, redirect, render_template, request, url_for, flash
from flask_bcrypt import Bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from app.models.user import User

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()

DATABASE = './dist/northwind.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.validate(username, password)
        if user:
            login_user(user)
            return redirect(url_for('main.index'))
        
        flash('Invalid username or password')
    
    return render_template('auth/login.html')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        customer_id = request.form.get('customer_id')

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template('auth/register.html')

        db = get_db()
        try:

            if not customer_id:
                customer_id = None

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            db.execute(
                'INSERT INTO Users (customer_id, username, hashed_password) VALUES (?, ?, ?)',
                (customer_id, username.lower(), hashed_password)
            )
            db.commit()
            
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('auth.login'))

        except sqlite3.IntegrityError:
            flash("Username already exists", "error")
            return render_template('auth/register.html')

    return render_template('auth/register.html')


@auth_bp.route("/profile")
@login_required 
def profile():
    db = get_db()
    customer = db.execute(
        'SELECT * FROM Customers WHERE CustomerID = ?',
        [current_user.customer_id]
    ).fetchone()
    
    return render_template("auth/profile.html", customer=customer)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
