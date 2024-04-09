from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,flash
from .. import db


class Admin:
    def __init__(self,username,password):
        self.username=username
        self.password=password

class Internship(db.Model):
    __tablename__ = 'internships'

    digital_id = db.Column(db.String(50), primary_key=True)
    internship_id = db.Column(db.Integer, unique=True, nullable=False)
    organization_name = db.Column(db.String(255), nullable=False)
    organization_address = db.Column(db.Text, nullable=False)
    organization_website = db.Column(db.String(255))
    nature_of_work = db.Column(db.Text)
    reporting_authority_name = db.Column(db.String(255))
    reporting_authority_designation = db.Column(db.String(100))
    reporting_authority_email = db.Column(db.String(255))
    reporting_authority_mobile = db.Column(db.String(20))
    start_date = db.Column(db.Date, nullable=False)
    completion_date = db.Column(db.Date, nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    mode_of_internship = db.Column(db.String(20), nullable=False)
    stipend = db.Column(db.Boolean, nullable=False)
    stipend_amount = db.Column(db.Float)
    remarks = db.Column(db.Text)
    offer_letter_path = db.Column(db.String(255))
    completion_certificate_path = db.Column(db.String(255))

class ODApplication(db.Model):
    __tablename__ = 'od_applications'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    od_days_required = db.Column(db.Integer)
    od_dates = db.Column(db.String(100))
    od_details = db.Column(db.String(255))
    current_cgpa = db.Column(db.Float)
