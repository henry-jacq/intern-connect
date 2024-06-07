from .extensions import db

class Students(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    digital_id = db.Column(db.Integer, unique=True)
    name = db.Column(db.String(255))
    reg_no = db.Column(db.String(255))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    secondary_email = db.Column(db.String(255), nullable=True)
    phone_no = db.Column(db.String(255))
    whatsapp_no = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255))
    batch = db.Column(db.String(32))
    mentor = db.Column(db.String(32))


class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    digital_id = db.Column(db.String(50))
    org_name = db.Column(db.String(255), nullable=False)
    org_address = db.Column(db.String(255), nullable=False)
    org_website = db.Column(db.String(255))
    nature_of_work = db.Column(db.Text)
    reporting_authority = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    internship_mode = db.Column(db.String(20), nullable=False)
    stipend = db.Column(db.String(8), nullable=False)
    stipend_amount = db.Column(db.String(8))
    ppo = db.Column(db.String(16), nullable=False)
    internship_status = db.Column(db.String(20), nullable=False)
    offer_letter = db.Column(db.String(255))
    completion_letter = db.Column(db.String(255))

class ODApplication(db.Model):
    __tablename__ = 'od_applications'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    od_days_required = db.Column(db.Integer)
    od_dates = db.Column(db.String(100))
    od_details = db.Column(db.String(255))
    current_cgpa = db.Column(db.Float)

class Announcements(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))
