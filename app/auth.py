from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .extensions import db
from .models import Students, ODApplication, Internship, Announcements

auth = Blueprint('auth', __name__)

@auth.before_request
def check_user():
    if 'user' in session:
        return redirect(url_for('views.home'))

@auth.route("/add_message", methods=["POST"])
def add_message():
    message = request.form["message"]
    flash("OD details added successfully!")
    return redirect(url_for("index"))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        digital_id = int(request.form.get("digital_id"))
        password = request.form.get("password")
        student = Students.query.filter_by(digital_id=digital_id).first()
        
        if student and check_password_hash(student.password, password):
            session['user'] = True
            return redirect(url_for('views.home'))
        flash('Invalid credentials')
    return render_template("login.html")

@auth.route('/admin_reports', methods=['GET'])
def admin_reports():
    total_internships = Internship.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    return render_template("admin/admin_reports.html", 
                           total_internships=total_internships, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)

@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        # Add authentication logic
    return render_template("admin/admin_login.html")

@auth.route('/admin/create/announcement', methods=['GET', 'POST'])
def create_announcement():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        
        announcement = Announcements(title=title, content=content)
        db.session.add(announcement)
        db.session.commit()
        
        return render_template('admin/announcement.html', msg=True)
    return render_template('admin/announcement.html', msg=False)

@auth.route('/admin_dashboard', methods=['GET'])
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

@auth.route('/apply_od', methods=['POST'])
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

@auth.route('/od/status', methods=['GET'])
def od_status():
    od_applications = ODApplication.query.all()
    return render_template('od_status.html', od_applications=od_applications)

@auth.route('/faculty_approvals')
def faculty_approvals():
    # Implement logic to fetch and display faculty approvals
    return render_template('faculty_approvals.html')
