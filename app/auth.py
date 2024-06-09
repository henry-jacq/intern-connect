from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Students, Faculty
from .extensions import get_role_id

auth = Blueprint('auth', __name__)

@auth.before_request
def check_user():
    if 'role' in session:
        if session['role'] == get_role_id('user'):
            return redirect(url_for('views.home'))
        if session['role'] == get_role_id('faculty'):
            return redirect(url_for('faculty.home'))
        if session['role'] == get_role_id('admin'):
            return redirect(url_for('admin.dashboard'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        digital_id = request.form.get("digital_id")
        password = request.form.get("password")
        student = Students.query.filter_by(digital_id=digital_id).first()
        
        if student and student.password == password:
            session['user'] = student.id
            session['role'] = get_role_id('user')
            session['digital_id'] = int(digital_id)
            return redirect(url_for('views.home'))
            
        flash('Invalid credentials', 'danger')
    return render_template("login.html")

@auth.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        
        if email == 'admin@gmail.com' and password == '123':
            session['admin'] = True
            session['user'] = True
            session['role'] = get_role_id('admin')
            return redirect(url_for('admin.dashboard'))
    return render_template("admin/login.html")

@auth.route('/faculty/login', methods=['GET', 'POST'])
def faculty_login():
    if request.method == 'POST':
        digital_id = request.form.get("digital_id")
        password = request.form.get("password")
        teacher = Faculty.query.filter_by(digital_id=digital_id).first()
        
        if teacher and teacher.password == password:
            session['user'] = teacher.id
            session['role'] = get_role_id('faculty')
            session['digital_id'] = int(digital_id)
            return redirect(url_for('faculty.home'))
        flash('Invalid credentials', 'danger')
    return render_template("faculty/login.html")

