from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,flash
import json
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash
from .extensions import db
from .models import Admin
from .models import ODApplication


auth=Blueprint('auth',__name__)

@auth.route('/')
def index():
    return render_template('index.html')

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


@auth.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    global adminlist
    adminlist = load_admin_data()

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        hash_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        for admin in adminlist:
            if admin.username == username:
                if admin.password == password:
                    flash("Login successful.")
                    session['admin_username'] = admin.username
                    session['admin_password'] = admin.password
                    return redirect(url_for('auth.admin_dashboard'))
                else:
                    flash("Invalid credentials. Please try again.")
                    return render_template("admin/admin_login.html")
        
        flash('You are not a recognized admin user')
        return redirect(url_for('auth.login'))

    else:
        return render_template("admin/admin_login.html")

@auth.route('/apply_od', methods=['POST'])
def apply_od():
    duration = request.form['duration']
    od_days_required = request.form['odDaysRequired']
    od_dates = request.form['odDates']
    od_details = request.form['odDetails']
    current_cgpa = request.form['currentCGPA']
    
    # Create a new OD application object and save it to the database
    od_application = ODApplication(id=id,duration=duration, od_days_required=od_days_required, od_dates=od_dates, 
                                   od_details=od_details, current_cgpa=current_cgpa)
    db.session.add(od_application)
    db.session.commit()
    
    # Redirect to the index page after form submission
    return redirect(url_for('auth.index'))