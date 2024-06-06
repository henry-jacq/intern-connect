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

@views.route('/apply_od', methods=['POST'])
def apply_od():
    duration = request.form['duration']
    od_days_required = request.form['od_days_required']
    od_date_range = request.form['od_dates']
    od_details = request.form['od_details']
    current_cgpa = request.form['current_cgpa']

    pattern = r'(?P<m_start>\d{2})/(?P<d_start>\d{2})/(?P<y_start>\d{4})-(?P<m_end>\d{2})/(?P<d_end>\d{2})/(?P<y_end>\d{4})'
    match = re.match(pattern, od_date_range)
    if match:
        start_date = datetime(int(match.group('y_start')), int(match.group('m_start')), int(match.group('d_start')))
        end_date = datetime(int(match.group('y_end')), int(match.group('m_end')), int(match.group('d_end')))
        od_dates = f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}"
        od_application = ODApplication(duration=duration, od_days_required=od_days_required, od_dates=od_dates, od_details=od_details, current_cgpa=current_cgpa)

        db.session.add(od_application)
        db.session.commit()
        flash('OD details added successfully!', 'success')
        return redirect(url_for('views.home'))
    else:
        flash('Invalid date format. Please use MM/DD/YYYY - MM/DD/YYYY format.', 'danger')
        return redirect(url_for('views.home'))

@views.route('/od/status', methods=['GET'])
def od_status():
    od_applications = ODApplication.query.all()
    return render_template('od_status.html', od_applications=od_applications)

@views.route('/faculty_approvals')
def faculty_approvals():
    # Implement logic to fetch and display faculty approvals
    return render_template('faculty_approvals.html')

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

        return redirect(url_for('index'))