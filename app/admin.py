from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import Students, ODApplication, Internship, Announcements

admin = Blueprint('admin', __name__)

@admin.before_request
def check_auth():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

@admin.route("/add_message", methods=["POST"])
def add_message():
    message = request.form["message"]
    flash("OD details added successfully!")
    return redirect(url_for("index"))

@admin.route('/admin_reports', methods=['GET'])
def admin_reports():
    total_internships = Internship.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    return render_template("admin/admin_reports.html", 
                           total_internships=total_internships, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)
    
@admin.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    total_internships = Internship.query.count()
    total_students = Students.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    return render_template('admin/admin_dash.html', 
                           total_internships=total_internships, 
                           total_students=total_students, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)

@admin.route('/admin/create/announcement', methods=['GET', 'POST'])
def create_announcement():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        
        announcement = Announcements(title=title, content=content)
        db.session.add(announcement)
        db.session.commit()
        
        return render_template('admin/announcement.html', msg=True)
    return render_template('admin/announcement.html', msg=False)
