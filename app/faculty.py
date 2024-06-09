from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Announcements, Faculty
from .extensions import get_role_id

faculty = Blueprint('faculty', __name__)

@faculty.before_request
def check_user():
    if 'user' not in session:
        return redirect(url_for('auth.faculty_login'))
    if session['role'] != get_role_id('faculty'):
        return redirect(url_for('auth.faculty_login'))

@faculty.route('/home')
def home():
    teacher = Faculty.query.filter_by(id=session['user']).first()
    query = Announcements.query.all()
    anc_list = [{'title': anc.title, 'content': anc.content} for anc in query]
    return render_template('faculty/index.html', announce=anc_list, teacher=teacher)

@faculty.route('/add/student')
def add_student():
    pass

@faculty.route('/od/requests')
def od_requests():
    pass

@faculty.route('/profile')
def profile():
    pass

@faculty.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.faculty_login'))
