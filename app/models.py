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

class OnDuty(db.Model):
    __tablename__ = 'on_duty'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'))
    source_of_referral = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(255))
    current_cgpa = db.Column(db.Float)
    status = db.Column(db.String(255), default="Pending")
    student = db.relationship('Students', backref=db.backref('on_duty', lazy=True))
    internship = db.relationship('Internship', backref=db.backref('on_duty', lazy=True))

class Announcements(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.String(255))

class Faculty(db.Model):
    __tablename__ = 'faculties'

    id = db.Column(db.Integer, primary_key=True)
    digital_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_no = db.Column(db.String(20), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)


faculty_students = db.Table('faculty_students',
    db.Column('faculty_id', db.Integer, db.ForeignKey('faculties.id'), primary_key=True),
    db.Column('students_id', db.Integer, db.ForeignKey('students.id'), primary_key=True)
)

# Establish relationships
Faculty.students = db.relationship('Students', secondary=faculty_students, backref=db.backref('faculties', lazy='dynamic'))


class OdRequest(db.Model):
    __tablename__ = 'od_requests'

    id = db.Column(db.Integer, primary_key=True)
    on_duty_id = db.Column(db.Integer, db.ForeignKey('on_duty.id'))
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'))
    status = db.Column(db.String(255), default='Pending')  # 'Pending', 'Accepted', 'Rejected'

    on_duty = db.relationship('OnDuty', backref=db.backref('od_requests', lazy=True))
    faculty = db.relationship('Faculty', backref=db.backref('od_requests', lazy=True))


