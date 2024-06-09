from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, get_role_id
from .models import Students, Internship, Announcements

admin = Blueprint('admin', __name__)

@admin.before_request
def check_user():
    if 'role' not in session:
        return redirect(url_for('auth.admin_login'))
    if session['role'] != get_role_id('admin'):
        return redirect(url_for('auth.admin_login'))

@admin.route('/reports', methods=['GET'])
def reports():
    total_internships = Internship.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    return render_template("admin/reports.html", 
                           total_internships=total_internships, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)
    
@admin.route('/dashboard')
def dashboard():
    total_internships = Internship.query.count()
    total_students = Students.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    return render_template('admin/dashboard.html', 
                           total_internships=total_internships, 
                           total_students=total_students, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)

@admin.route('/create/announcement', methods=['GET', 'POST'])
def create_announcement():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        
        announcement = Announcements(title=title, content=content)
        db.session.add(announcement)
        db.session.commit()
        
        return render_template('admin/announcement.html', msg=True)
    return render_template('admin/announcement.html', msg=False)

@admin.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.admin_login'))
