from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Internship, Announcements, ODApplication
from datetime import datetime
from .extensions import db
import os, re

views = Blueprint('views', __name__)
UPLOAD_PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd())), 'uploads')

@views.route('/')
def home():
    query = Announcements.query.all()
    anc_list = [{'title': anc.title, 'content': anc.content} for anc in query]
    return render_template('index.html', announce=anc_list)

@views.route('/internship/add', methods=['GET', 'POST'])
def intern_add():
    if request.method == 'POST':
        form_data = {
            "digital_id": request.form.get("digital_id"),
            "org_name": request.form.get("org_name"),
            "org_address": request.form.get("org_address"),
            "org_website": request.form.get("org_website"),
            "nature_of_work": request.form.get("nature_of_work"),
            "reporting_authority": request.form.get("reporting_authority"),
            "start_date": datetime.strptime(request.form.get("start_date"), '%Y-%m-%d'),
            "end_date": datetime.strptime(request.form.get("end_date"), '%Y-%m-%d'),
            "internship_mode": request.form.get("internship_mode"),
            "stipend": request.form.get("stipend"),
            "stipend_amount": request.form.get("stipend_amount"),
            "ppo": request.form.get("ppo"),
            "internship_status": request.form.get("internship_status")
        }

        internship = Internship(**form_data)

        for file_key in ['offer_letter', 'completion_letter']:
            if file_key in request.files:
                file = request.files[file_key]
                if file and file.filename:
                    filename = file.filename
                    file.save(os.path.join(UPLOAD_PATH, filename))
                    setattr(internship, file_key, filename)

        db.session.add(internship)
        db.session.commit()
        flash('Internship added successfully!', 'success')
        return redirect(url_for('views.home'))

    return render_template('internship.html')

@views.route('/admin_dashboard')
def admin_dashboard():
    # This view is duplicated in auth.py and should be removed or merged
    pass

@views.route('/apply_od2', methods=['POST'])
def apply_od2():
    if request.method == 'POST':
        duration = request.form['duration']
        od_days_required = request.form['odDaysRequired']
        od_dates = request.form['odDates']
        od_details = request.form['odDetails']
        current_cgpa = request.form['currentCGPA']

        # Create a new Internship object and add it to the database
        new_internship =Internship(duration=duration, od_days_required=od_days_required,
                                    od_dates=od_dates, od_details=od_details,
                                    current_cgpa=current_cgpa)
        db.session.add(new_internship)
        db.session.commit()

        return redirect(url_for('index')