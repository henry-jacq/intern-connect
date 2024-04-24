from .extensions import db


class Admin:
    def __init__(self,username,password):
        self.username=username
        self.password=password

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

    def __repr__(self):
        return f"Internship(id={self.id}, digital_id={self.digital_id}, organization_name={self.org_name})"

    @classmethod
    def create(cls, **kwargs):
        internship = cls(**kwargs)
        db.session.add(internship)
        db.session.commit()
        return internship

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class ODApplication(db.Model):
    __tablename__ = 'od_applications'

    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer)
    od_days_required = db.Column(db.Integer)
    od_dates = db.Column(db.String(100))
    od_details = db.Column(db.String(255))
    current_cgpa = db.Column(db.Float)
