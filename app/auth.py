from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,flash
import json
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash
from .extensions import db
from .models import Admin
from .models import ODApplication
import pymysql
import os
from .models import Internship
from datetime import datetime
from .models import Announcements


auth=Blueprint('auth',__name__)

@auth.route('/')
def index():
    return render_template('index.html')
@auth.route("/add_message", methods=["POST"])
def add_message():
    message = request.form["message"]
    message.append(message)
    flash("OD details added successfully!")
    return redirect(url_for("index"))

@auth.route('/login')
def login():
    return render_template("login.html")

def load_admin_data():
    try:
        # Read the JSON file and load the data back
        with open("admin_credentials.json", "r") as json_file:
            loaded_admin_list = json.load(json_file)

        # Retrieve the singleton instance of ClinicAdminSingleton
        admin_instance = Admin(None, None)

        # Update the singleton instance with the loaded data
        admin_instance.username = loaded_admin_list[0]['username']
        admin_instance.password = loaded_admin_list[0]['password']

        # Now you can work with the admin_instance

        return [admin_instance]
    except FileNotFoundError:
        return None  # Return None or handle the absence of the file accordingly



@auth.route('/admin_reports', methods=['GET'])
def admin_reports():
    # Query the database to retrieve necessary data
    total_internships = Internship.query.count()
    active_internships = Internship.query.filter_by(internship_status='Active').count()
    completed_internships = Internship.query.filter_by(internship_status='Completed').count()

    # Pass the data to the template for rendering
    return render_template("admin/admin_reports.html", 
                           total_internships=total_internships, 
                           active_internships=active_internships, 
                           completed_internships=completed_internships)

@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    global adminlist
    #adminlist = load_admin_data()

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        user=os.getenv("ADMIN_USER")
        passwd=os.getenv("ADMIN_PASSWORD")
        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        
        if user == username:
            if passwd == password:
                flash("Login successful.")
                session['admin_username'] = user
                session['admin_password'] = passwd
                return redirect(url_for('auth.admin_dashboard'))
            else:
                flash("Invalid credentials. Please try again.")
                return render_template("admin/admin_login.html")
        
        flash('You are not a recognized admin user')
        return redirect(url_for('auth.login'))

    else:
        return render_template("admin/admin_login.html")


@auth.route('/admin/create/announcement', methods=['GET', 'POST'])
def create_announcement():
    if request.method == 'POST':
        title = request.form.get("title")
        content = request.form.get("content")
        
        announcements = Announcements(
            title=title, content=content
        )
        db.session.add(announcements)
        db.session.commit()
        
        return render_template('admin/announcement.html', msg=True)
    return render_template('admin/announcement.html', msg=False)

@auth.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
         
    # Connect to MySQL database
    connection = pymysql.connect(
        host='localhost',
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        database=os.getenv('DB_NAME'),
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            # Total Internships Query
            total_internships_query = "SELECT COUNT(*) AS total_internships FROM internships"
            cursor.execute(total_internships_query)
            total_internships_result = cursor.fetchone()
            total_internships = total_internships_result['total_internships']
            
            # Total Students Query
            total_students_query = "SELECT COUNT(*) AS total_students FROM internships"
            cursor.execute(total_students_query)
            total_students_result = cursor.fetchone()
            total_students = total_students_result['total_students']
            
            # Active Internships Query
            active_internships_query = "SELECT COUNT(*) AS active_internships FROM internships WHERE internship_status = 'Active'"
            cursor.execute(active_internships_query)
            active_internships_result = cursor.fetchone()
            active_internships = active_internships_result['active_internships']
            
            # Completed Internships Query
            completed_internships_query = "SELECT COUNT(*) AS completed_internships FROM internships WHERE internship_status = 'Completed'"
            cursor.execute(completed_internships_query)
            completed_internships_result = cursor.fetchone()
            completed_internships = completed_internships_result['completed_internships']
            
    finally:
        # Close the connection
        connection.close()

    
    return render_template('admin/admin_dash.html', total_internships=total_internships, 
                           total_students=total_students, active_internships=active_internships, 
                           completed_internships=completed_internships)


@auth.route('/save_od', methods=['POST'])
def save_od():
    duration = request.form['duration']
    od_days_required = request.form['od_days_required']
    od_date_range = request.form['od_dates']
    od_details = request.form['od_details']
    current_cgpa = request.form['current_cgpa']
    try:
        # Attempt to convert the date range string into a datetime object
        od_dates = datetime.strptime(od_date_range, '%m/%d/%Y-%m/%d/%Y')
    except ValueError:
        # Handle the case where the date range string cannot be converted
        flash('Invalid date format. Please use MM/DD/YYYY - MM/DD/YYYY format.', 'danger')
        return redirect(url_for('views.home'))
    
    # Create a new OD application object and save it to the database
    od_application = ODApplication(duration=duration, od_days_required=od_days_required, od_dates=od_dates, 
                                   od_details=od_details, current_cgpa=current_cgpa)
    db.session.add(od_application)
    db.session.commit()
    
    # Display a flash message confirming that the OD details have been added
    flash('OD details added successfully!', 'success')
    return redirect(url_for('views.home'))  # Redirect to the index page after form submission


@auth.route('/od_status', methods=['GET', 'POST'])
def od_status():
    try:
        # Connect to MySQL database
        connection = pymysql.connect(
            host='localhost',
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )

        with connection.cursor() as cursor:
            # Query to fetch all fields from od_applications table
            query = "SELECT duration, od_days_required, od_dates, od_details, current_cgpa FROM od_applications"
            cursor.execute(query)
            od_applications = cursor.fetchall()

        # Close the connection
        connection.close()

        # Render template with od_applications data
        return render_template('od_status.html', od_applications=od_applications)

    except Exception as e:
        # Handle exceptions here
        print("An error occurred:", str(e))
        return f"<h1>Error</h1><p>{str(e)}</p>", 500
    
@auth.route('/faculty_approvals')
def faculty_approvals():
    # Query database to fetch faculty approvals data
    # For example:
    # approvals = FacultyApproval.query.all()
    # Pass the approvals data to the template
    return render_template('faculty_approvals.html')
