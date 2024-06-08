from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .models import Students, Internship, Announcements, ODApplication,Teacher
from datetime import datetime
import os, re
from .extensions import db, upload_path, get_random_filename

views = Blueprint('views', __name__)

@views.before_request
def check_auth():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

@views.route('/')
def home():
    student = Students.query.filter_by(id=session['user']).first()
    query = Announcements.query.all()
    anc_list = [{'title': anc.title, 'content': anc.content} for anc in query]
    return render_template('index.html', announce=anc_list, student=student)

@views.route('/teacher')
def teacher_home():
    teacher = Teacher.query.filter_by(id=session['user']).first()
    query = Announcements.query.all()
    anc_list = [{'title': anc.title, 'content': anc.content} for anc in query]
    return render_template('teacher_index.html', announce=anc_list, teacher=teacher)


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
            "offer_letter": filename or None
        }
        
        internship = Internship(**form_data)

        db.session.add(internship)
        db.session.commit()
        flash('Internship added successfully!', 'success')
        return redirect(request.url)

    return render_template('add_intern.html', student=student)

@views.route('/internship/update')
def update_intern():
    return render_template('update_intern.html')


@views.route('/od/select_intern', methods=['GET', 'POST'])
def select_intern():
    if request.method == 'POST':
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

    return render_template('apply_od.html')

@views.route('/od/apply', methods=['GET', 'POST'])
def apply_od():
    duration = None
    od_days_required=None

    if request.method == 'POST':
       duration=request.form['duration']
       od_days_required=request.form['od_days_required']
       od_date_range = request.form['od_dates']
       od_details=request.form['od_details']
       current_cgpa=request.form['current_cgpa']

# Define a regular expression pattern to match the date range format
       pattern = r'(?P<m_start>\d{2})/(?P<d_start>\d{2})/(?P<y_start>\d{4})-(?P<m_end>\d{2})/(?P<d_end>\d{2})/(?P<y_end>\d{4})'

# Use regular expression to extract start and end dates from the date range string
       match = re.match(pattern, od_date_range)
       if match:
           # Extract start and end dates from the match object
           start_date = datetime(int(match.group('y_start')), int(match.group('m_start')), int(match.group('d_start')))
           end_date = datetime(int(match.group('y_end')), int(match.group('m_end')), int(match.group('d_end')))
           od_dates = f"{start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}"
           od_application=ODApplication(duration=duration,
                             od_days_required=od_days_required,
                             od_dates=od_dates,
                             od_details=od_details,
                             current_cgpa=current_cgpa)


           db.session.add(od_application)
           db.session.commit()
           # Display a flash message confirming that the OD details have been added
           flash('OD details added successfully!', 'success')
           return render_template('apply_od2.html', msg=True)
       else:
           # Handle the case where the date range is not in the expected format
           flash('Invalid date range format. Please use the format DD/MM/YYYY-DD/MM/YYYY', 'danger')
           return redirect(url_for('views.select_intern'))
    return render_template('apply_od2.html', msg=False)
    

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
    if session.get('user'):
        session.pop('user')
    return redirect(url_for('auth.login'))
