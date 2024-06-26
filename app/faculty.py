from flask import Blueprint, render_template, request, redirect, url_for, session, flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Announcements, Faculty,OdRequest,OnDuty,Internship
from .extensions import get_role_id, get_uploads
from .models import db, Students, Faculty, faculty_students

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



@faculty.route('/students/add', methods=['GET', 'POST'])
def add_students():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    faculty_id = session['user']
    faculty = Faculty.query.filter_by(id=faculty_id).first()

    if request.method == 'POST':
        student_ids = request.form.getlist('students')
        for student_id in student_ids:
            student = Students.query.get(student_id)
            if student:
                faculty.students.append(student)
        db.session.commit()
        flash('Students added successfully!', 'success')
    students = Students.query.all()
    return render_template("faculty/add_students.html", faculty=faculty, students=students)



@faculty.route('/students', methods=['GET'])
def view_students():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    faculty_id = session['user']
    
    # Query to get all students related to the logged-in faculty
    students = (db.session.query(Students)
                .join(faculty_students, faculty_students.c.students_id == Students.id)
                .filter(faculty_students.c.faculty_id == faculty_id)
                .all())
    
    return render_template('faculty/students.html', students=students)


@faculty.route('/od_requests', methods=['GET'])
def od_requests_page():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    faculty_id = session['user']
    
    requests = (db.session.query(OdRequest)
            .join(OnDuty, OnDuty.id == OdRequest.on_duty_id)
            .join(Internship, Internship.id == OnDuty.internship_id)  # Join with Internship model
            .join(faculty_students, faculty_students.c.students_id == Internship.id)
            .filter(faculty_students.c.faculty_id == faculty_id)
            .all())


    return render_template('faculty/od_requests.html', requests=requests)


@faculty.route('/api/od_requests', methods=['POST'])
def get_od_requests():
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    faculty_id = session['user']
    
    # Fetch all requests for this faculty member
    requests = (db.session.query(OdRequest)
                .join(OnDuty, OnDuty.id == OdRequest.on_duty_id)
                .join(Students, Students.id == OnDuty.student_id)
                .join(faculty_students, faculty_students.c.students_id == Students.id)
                .filter(faculty_students.c.faculty_id == faculty_id).all())

    # Extract the search term and status from the request body if it's a POST request
    if request.method == 'POST':
        data = request.get_json()
        search_term = data.get('searchTerm', '')
        status_filter = data.get('status', 'all')

        # Filter the requests
        filtered_requests = [
            {
                'id': req.id,
                'student_name': req.on_duty.student.name,
                'internship_title': req.on_duty.internship.nature_of_work,
                'company': req.on_duty.internship.org_name,
                'status': req.status,
                'offer_letter': req.on_duty.internship.offer_letter,
                'completion_letter': req.on_duty.internship.completion_letter
            }
            for req in requests
            if (search_term in req.on_duty.student.name.lower() or
                search_term in req.on_duty.internship.org_name.lower()) and
               (status_filter == 'all' or req.status.lower() == status_filter.lower()) and
               (req.faculty_id == session['user'])
        ]
    
    return jsonify(filtered_requests)

@faculty.route('/api/approve_od_request/<int:request_id>', methods=['POST'])
def approve_od_request(request_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    request = OdRequest.query.get(request_id)
    if request:
        request.status = 'Approved'
        check_and_update_on_duty_status(request.on_duty_id)
        # db.session.commit()
        return jsonify({'success': True, 'status': 'Approved'}), 200
    
    return jsonify({'success': False, 'message': 'Request not found'}), 404

@faculty.route('/api/reject_od_request/<int:request_id>', methods=['POST'])
def reject_od_request(request_id):
    if 'user' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    request = OdRequest.query.get(request_id)
    
    if request:
        request.status = 'Rejected'
        check_and_update_on_duty_status(request.on_duty_id)
        # db.session.commit()
        return jsonify({'success': True, 'status': 'Rejected'}), 200
    
    return jsonify({'success': False, 'message': 'Request not found'}), 404

def check_and_update_on_duty_status(on_duty_id):
    on_duty = OnDuty.query.get(on_duty_id)
    od_requests = OdRequest.query.filter_by(on_duty_id=on_duty_id).all()
    for req in od_requests:
        print(f"From check and update on_duty {req.status}")

    if all(req.status.lower() == 'approved' for req in od_requests):
        on_duty.status = 'Approved'
    elif all(req.status.lower() == 'rejected' for req in od_requests):
        on_duty.status = 'Rejected'
    else:
        on_duty.status = 'Pending'
    db.session.commit()

@faculty.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return get_uploads(filename)

@faculty.route('/profile', methods=['GET'])
def faculty_profile():
    if 'user' not in session:
        return redirect(url_for('auth.faculty_login'))

    faculty_id = session['user']
    
    # Query to get the logged-in faculty's details
    faculty = Faculty.query.filter_by(id=faculty_id).first()
    
    return render_template('faculty/profile.html', faculty=faculty)


@faculty.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.faculty_login'))

