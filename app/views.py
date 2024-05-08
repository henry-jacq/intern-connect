from flask import render_template, request, Blueprint, redirect, url_for, session
from .models import Internship, Announcements
from datetime import datetime
from .extensions import db
import os


views = Blueprint('views', __name__)
UPLOAD_PATH = os.path.join(os.path.abspath(os.path.join(os.getcwd())), 'uploads')

@views.route('/')
def home():
    query = Announcements.query.all()

    anc_list = [{
        'title': anc.title,
        'content': anc.content,
    } for anc in query]
    return render_template('index.html', announce=anc_list)


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
def od_status():
    if request.method == 'POST':
        return render_template('apply_od2.html', msg=True)
    return render_template('apply_od2.html', msg=False)

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('auth.login'))

@views.route('/internship/update')
def update_intern():
    return render_template('update_intern.html')

if __name__ == '__main__':
    views.run(debug=True)
    
    