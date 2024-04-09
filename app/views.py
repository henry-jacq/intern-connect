from flask import render_template,Blueprint

views=Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('index.html')

@views.route('/login')
def login():
    return render_template('login.html')

@views.route('/internship/add')
def intern_add():
    return render_template('add_intern.html')

@views.route('/od/apply')
def apply_od():
    return render_template('apply_od.html')

@views.route('/od/select_intern')
def od_status():
    return render_template('apply_od2.html')

@views.route('/profile')
def profile():
    return render_template('profile.html')

@views.route('/internship/update')
def update_intern():
    return render_template('update_intern.html')

if __name__ == '__main__':
    views.run(debug=True)