from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Students

auth = Blueprint('auth', __name__)

@auth.before_request
def check_user():
    if 'user' in session:
        return redirect(url_for('views.home'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        digital_id = int(request.form.get("digital_id"))
        password = request.form.get("password")
        student = Students.query.filter_by(digital_id=digital_id).first()
        
        if student and student.password == password:
            session['user'] = student.id
            return redirect(url_for('views.home'))
        flash('Invalid credentials')
    return render_template("login.html")

@auth.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email == 'admin@gmail.com' and password == '123':
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))
    return render_template("admin/login.html")

