from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db, get_role_id
from .models import Students, Internship, Announcements,OdRequest,OnDuty

admin = Blueprint('admin', __name__)

@admin.before_request
def check_user():
    if 'role' not in session:
        return redirect(url_for('auth.admin_login'))
    if session['role'] != get_role_id('admin'):
        return redirect(url_for('auth.admin_login'))
"""
@admin.route('/reports', methods=['GET'])
def reports():
    total_internships = Internship.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    return render_template("admin/reports.html", 
                           total_internships=total_internships, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)"""

@admin.route('/admin/reports')
def generate_reports():
    # Example data fetching from the database
    total_internships = db.session.query(Internship).count()
    active_internships = db.session.query(Internship).filter_by(internship_status='Active').count()
    completed_internships = db.session.query(Internship).filter_by(internship_status='Completed').count()
    
    online_internships = db.session.query(Internship).filter_by(internship_mode='Online').count()
    offline_internships = db.session.query(Internship).filter_by(internship_mode='Offline').count()
    hybrid_internships = db.session.query(Internship).filter_by(internship_mode='Hybrid').count()
    
    paid_internships = db.session.query(Internship).filter(Internship.stipend_amount.isnot(None)).count()
    unpaid_internships = db.session.query(Internship).filter(Internship.stipend_amount.is_(None)).count()
    
    pending_requests = db.session.query(OdRequest).filter_by(status='Pending').count()
    accepted_requests = db.session.query(OdRequest).filter_by(status='Accepted').count()
    rejected_requests = db.session.query(OdRequest).filter_by(status='Rejected').count()

    department_counts = db.session.query(Students.department, db.func.count(Students.id)).group_by(Students.department).all()
    departments, department_counts = zip(*department_counts)
    
    batch_counts = db.session.query(Students.batch, db.func.count(Students.id)).group_by(Students.batch).all()
    batches, batch_counts = zip(*batch_counts)

    org_counts = db.session.query(Internship.org_name, db.func.count(Internship.id)).group_by(Internship.org_name).all()
    organizations, org_counts = zip(*org_counts)
    
    
    return render_template('admin/reports.html', 
        total_internships=total_internships,
        active_internships=active_internships,
        completed_internships=completed_internships,
        online_internships=online_internships,
        offline_internships=offline_internships,
        hybrid_internships=hybrid_internships,
        paid_internships=paid_internships,
        unpaid_internships=unpaid_internships,
        pending_requests=pending_requests,
        accepted_requests=accepted_requests,
        rejected_requests=rejected_requests,
        departments=departments,
        department_counts=department_counts,
        batches=batches,
        batch_counts=batch_counts,
        organizations=organizations,
        org_counts=org_counts,
        
    )


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
