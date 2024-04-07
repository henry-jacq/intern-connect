from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/internship/add')
def intern_add():
    return render_template('add_intern.html')

@app.route('/od/apply')
def apply_od():
    return render_template('apply_od.html')

@app.route('/od/select_intern')
def od_status():
    return render_template('apply_od2.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/internship/update')
def update_intern():
    return render_template('update_intern.html')

if __name__ == '__main__':
    app.run(debug=True)