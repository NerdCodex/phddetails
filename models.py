
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'department'
    
    dno = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    dname = db.Column(db.String(50), unique=True, nullable=False)
    dtype = db.Column(db.String(20), nullable=False)
    labincluded = db.Column(db.Boolean, nullable=False)
    
    guides = db.relationship('Guide', back_populates='department', lazy=True)

    def __repr__(self):
        return (self.dname)
    
    def __str__(self):
        return self.dname

class Guide(db.Model):
    __tablename__ = 'guide'
    
    gno = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    guide_name = db.Column(db.String(100), unique=True, nullable=False)
    dno = db.Column(db.BigInteger, db.ForeignKey('department.dno'), nullable=False)
    
    department = db.relationship('Department', back_populates='guides', lazy=True)
    scholars = db.relationship('Details', back_populates='guide')

    def __repr__(self):
        return self.guide_name

class Status(db.Model):
    __tablename__ = 'status_'
    
    statusno = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    current_status = db.Column(db.String(100), unique=True, nullable=False)
    
    scholars = db.relationship('Details', back_populates='status', lazy=True)

    def __repr__(self) -> str:
        return self.current_status



class Details(db.Model):
    __tablename__ = 'details'
    
    scholar_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    gno = db.Column(db.BigInteger, db.ForeignKey('guide.gno'), nullable=False)
    guide_role = db.Column(db.String(10), nullable=False)
    scholar_name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    regno = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    timing = db.Column(db.String(10), nullable=False)
    caste = db.Column(db.String(100), nullable=True)
    subcaste = db.Column(db.String(100), nullable=True)
    religion = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    phno = db.Column(db.String(15), nullable=True)
    optionalphno = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    commencement_date = db.Column(db.Date, nullable=True)
    join_date = db.Column(db.Date, nullable=True)
    last_fee_date = db.Column(db.Date, nullable=True)
    total_center_fees = db.Column(db.BigInteger, nullable=True)
    annual_fee = db.Column(db.BigInteger, nullable=True)
    labfees = db.Column(db.BigInteger, nullable=True)
    fees_paid = db.Column(db.BigInteger, nullable=True)
    no_due_date = db.Column(db.Date, nullable=True)
    viva_date = db.Column(db.Date, nullable=True)
    thesis_title = db.Column(db.Text, nullable=True)
    statusno = db.Column(db.BigInteger, db.ForeignKey('status_.statusno'), nullable=False)
    dc_meeting_date = db.Column(db.Date, nullable=True)
    dc_meeting = db.Column(db.BigInteger, nullable=True)
    dc_meeting_fee = db.Column(db.BigInteger, nullable=True)
    
    guide = db.relationship('Guide', back_populates='scholars')
    status = db.relationship('Status', back_populates='scholars')



