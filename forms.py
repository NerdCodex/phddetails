from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SelectField, DateField, BooleanField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Optional
from models import *


class DepartmentForm(FlaskForm):
    dname = StringField("Department Name",validators=[DataRequired()])
    dtype = SelectField("Department Type", choices=["Arts", "Science"])
    labincluded = BooleanField("Lab Included")


class GuideForm(FlaskForm):
    guide_name = StringField('Guide Name', validators=[DataRequired()])
    department = QuerySelectField(
        'Department',
        query_factory=lambda: Department.query.all(),
        allow_blank=False,
        get_label='dname'  # Display department name in the form
    )

class StatusForm(FlaskForm):
    current_status = StringField("Current Status",validators=[DataRequired()])

class CasteForm(FlaskForm):
    caste_name = StringField("Caste Name",validators=[DataRequired()])

class DetailsForm(FlaskForm):
        
    guide = QuerySelectField(
        'Guide Name',
        query_factory=lambda: Guide.query.all(),
        allow_blank=False,
        get_label='guide_name',
    )
    status = QuerySelectField(
        'Current Status',
        query_factory=lambda: Status.query.all(),
        allow_blank=False,
        get_label='current_status'
    )
    guide_role = SelectField("Guide Role", choices=[("Guide", "Guide"), ("Co-Guide", "Co-Guide")])
    scholar_name = StringField("Scholar Name", validators=[DataRequired()])
    gender = StringField("Gender", validators=[DataRequired()])
    regno = StringField("Registration Number", validators=[Optional()])
    dob = DateField("Date of Birth", validators=[Optional()])
    timing = SelectField("Timing", choices=[("Part-Time", "Part-Time"), ("Full-Time", "Full-Time")])
    casteno = StringField("Caste", validators=[Optional()])
    subcaste = StringField("Sub Caste", validators=[Optional()])
    religion = StringField("Religion", validators=[Optional()])
    email = StringField("Email", validators=[Optional()])
    phno = StringField("Phone No. ", validators=[Optional()])
    optionalphno = StringField("Optional Phone No. ", validators=[Optional()])
    address = TextAreaField("Residential Address", validators=[Optional()])
    commencement_date = DateField("Commencement Date", validators=[Optional()])
    join_date = DateField("Date of Joining", validators=[Optional()])
    last_fee_date = DateField("Last Fee Date", validators=[Optional()])
    total_center_fees = IntegerField("Total Center Fees", validators=[Optional()])
    annual_fee = IntegerField("Annual Fees", validators=[Optional()])
    fees_paid = IntegerField("Fees Paid", validators=[Optional()])
    labfees = IntegerField("Lab Fees", validators=[Optional()])
    no_due_date = DateField("No Due Issued Date", validators=[Optional()])
    viva_date = DateField("Viva Date", validators=[Optional()])
    thesis_title = TextAreaField("Thesis Title", validators=[Optional()])
    dc_meeting_date = DateField("DC Meeting Date", validators=[Optional()])
    dc_meeting = IntegerField("DC Meeting Sequence", validators=[Optional()])
    dc_meeting_fee = IntegerField("DC Meeting Fees", validators=[Optional()])
