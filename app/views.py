from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Students, Internship, Announcements, OnDuty, Faculty
from datetime import datetime
import os, re
from .extensions import db, upload_path, get_random_filename, get_uploads, get_role_id

views = Blueprint('views', __name__)

@views.before_request
def check_user():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    if session['role'] != get_role_id('user'):
        return redirect(url_for('auth.login'))

@views.route('/')
def home():
    student = Students.query.filter_by(id=session['user']).first()
    query = Announcements.query.all()
    anc_list = [{'title': anc.title, 'content': anc.content} for anc in query]
    return render_template('index.html', announce=anc_list, student=student)

@views.route('/internship/add', methods=['GET', 'POST'])
def intern_add():
    student = Students.query.filter_by(id=session['user']).first()

    if request.method == 'POST':
      
        # Handling file uploads
        if 'offer_letter' in request.files:
            file = request.files['offer_letter']
            if file and file.filename:
                filename = get_random_filename(file.filename)
                file_path = os.path.join(upload_path, filename)
                file.save(file_path)
            else:
                filename = None
        
        form_data = {
            "digital_id": session['digital_id'],
            "org_name": request.form.get("org_name"),
            "org_address": request.form.get("org_address"),
            "org_website": request.form.get("org_website"),
            "nature_of_work": request.form.get("nature_of_work"),
            "reporting_authority": request.form.get("reporting_authority"),
            "start_date": datetime.strptime(request.form.get("start_date"), '%Y-%m-%d'),
            "end_date": datetime.strptime(request.form.get("end_date"), '%Y-%m-%d'),
            "internship_mode": request.form.get("internship_mode"),
            "stipend": request.form.get("stipend"),
            "stipend_amount": request.form.get("stipend_amount") or None,
            "ppo": request.form.get("ppo"),
            "internship_status": request.form.get("internship_status"),
            "offer_letter": filename
        }
        
        internship = Internship(**form_data)

        db.session.add(internship)
        db.session.commit()
        flash('Internship added successfully!', 'success')
        return redirect(request.url)

    return render_template('add_intern.html', student=student)

@views.route('/internship/update', defaults={'intern_id': None})
@views.route('/internship/update/<int:intern_id>', methods=['GET', 'POST'])
def update_intern(intern_id):
    if intern_id is not None:
        intern = Internship.query.filter_by(digital_id=session['digital_id'], id=intern_id).first_or_404()
        if request.method == 'POST':
            # Handling file uploads
            filenames = {}
            for file_type in ['completion_letter', 'offer_letter']:
                if file_type in request.files:
                    file = request.files[file_type]
                    if file and file.filename:
                        filename = get_random_filename(file.filename)
                        file_path = os.path.join(upload_path, filename)
                        file.save(file_path)
                        filenames[file_type] = filename

            intern = Internship.query.get(intern_id)

            if intern:
                # Update fields conditionally
                intern.ppo = request.form.get("ppo") or intern.org_name
                intern.internship_status = request.form.get("internship_status") or intern.internship_status
                if filenames.get('completion_letter'):
                    if intern.completion_letter is not None:
                        path = os.path.join(upload_path, intern.completion_letter)
                        if os.path.exists(path):
                            os.remove(path)
                    intern.completion_letter = filenames.get('completion_letter')
                if filenames.get('offer_letter'):
                    if intern.offer_letter is not None:
                        path = os.path.join(upload_path, intern.offer_letter)
                        if os.path.exists(path):
                            os.remove(path)
                    intern.offer_letter = filenames.get('offer_letter')

                db.session.commit()
                flash('Internship updated successfully!', 'success')
            else:
                flash('Internship not found.', 'danger')

            return redirect(request.url)
        return render_template('update_single_intern.html', intern_id=intern_id, data=intern)
    else:
        interns = Internship.query.filter_by(digital_id=session['digital_id']).all()
        return render_template('update_intern.html', internships=interns)

@views.route('/od/select_intern', methods=['GET'])
def select_intern():
    interns = Internship.query.filter_by(digital_id=session['digital_id']).all()
    return render_template('apply_od.html', internships=interns)

@views.route('/od/apply/<int:intern_id>', methods=['GET', 'POST'])
def apply_od(intern_id):
    if request.method == 'POST':
        form_data = {
            "internship_id": intern_id,
            "source_of_referral": request.form.get("referral_source"),
            "start_date": request.form.get("start_date"),
            "end_date": request.form.get("end_date"),
            "current_cgpa": float(request.form.get("current_cgpa")),
            "reason": request.form.get("reason"),
            "status": "Pending"
        }

        od = OnDuty(**form_data)
        db.session.add(od)
        db.session.commit()
        flash('OD submitted successfully!','success')
        
    intern = Internship.query.filter_by(digital_id=session['digital_id'], id=intern_id).first_or_404()
    return render_template('apply_od2.html', intern_id=intern_id, data=intern)

@views.route('/od/status', methods=['GET'])
def od_status():
    data = OnDuty.query.all()
    return render_template('od_status.html', od_applications=data)

@views.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return get_uploads(filename)

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

@views.route("/add_message", methods=["POST"])
def add_message():
    message = request.form["message"]
    flash("OD details added successfully!")
    return redirect(url_for("index"))

@views.route('/profile')
def profile():
    student = Students.query.filter_by(id=session['user']).first()
    return render_template('profile.html', student=student)

@views.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


