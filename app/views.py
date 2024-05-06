from flask import render_template, request, Blueprint, redirect, url_for,flash
from .models import Internship,ODApplication
from datetime import datetime
from .extensions import db
import re

views=Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('views.home'))
    return render_template('login.html')

@views.route('/internship/add', methods=['GET', 'POST'])
def intern_add():
    if request.method == 'POST':
        orgName = request.form['org_name']
        orgAddr = request.form['org_addr']
        orgWeb = request.form['org_web']
        natureWork = request.form['nature_work']
        repAuthName = request.form['report_authority']
        startDate = datetime.strptime(request.form['start_date'], '%Y-%m-%d')  # Parse start date
        endDate = datetime.strptime(request.form['end_date'], '%Y-%m-%d')  # Parse end date
        internMode = request.form['intern_mode']
        stipend = request.form['stipend']
        stipendAmount = request.form.get('stipend_amount', None)
        ppo = request.form['ppo']
        # offerLetter = request.form['offer_letter']
        internStatus = request.form['intern_status']
        digital_id = '2212023'  # digital_id seems to be a string based on the model

        internship = Internship(
            digital_id=digital_id,
            org_name=orgName,
            org_address=orgAddr,
            org_website=orgWeb,
            nature_of_work=natureWork,
            reporting_authority=repAuthName,
            start_date=startDate,
            end_date=endDate,
            internship_status=internStatus,
            internship_mode=internMode,
            stipend=stipend,
            stipend_amount=stipendAmount,
            ppo=ppo
        )

        db.session.add(internship)
        db.session.commit()
        
        return render_template('add_intern.html', msg=True)

    return render_template('add_intern.html', msg=False)

@views.route('/od/apply')
def apply_od():
    return render_template('apply_od.html')

@views.route('/od/select_intern', methods=['GET', 'POST'])
def select_intern():
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

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/logout')
def logout():
    return redirect(url_for('auth.login'))

@views.route('/internship/update')
def update_intern():
    return render_template('update_intern.html')

if __name__ == '__main__':
    views.run(debug=True)