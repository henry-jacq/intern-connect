from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Announcements, Faculty

faculty = Blueprint('faculty', __name__)

# @faculty.before_request
# def check_user():
#     if 'user' in session:
#         return redirect(url_for('views.home'))


@faculty.route('/home')
def home():
    teacher = Faculty.query.filter_by(id=session['user']).first()
    query = Announcements.query.all()
    anc_list = [{'title': anc.title, 'content': anc.content} for anc in query]
    return render_template('faculty/index.html', announce=anc_list, teacher=teacher)

