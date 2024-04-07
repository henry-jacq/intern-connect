from flask import Blueprint,Flask, render_template, request, redirect, url_for, session,flash
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash

auth=Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template("login.html")
