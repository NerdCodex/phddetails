from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, IntegerField, TextAreaField, SelectField, DateField, BooleanField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Optional
from models import *
from flask import url_for


class DepartmentForm(FlaskForm):
    dname = StringField("Department Name",validators=[DataRequired()])
    dtype = SelectField("Department Type", choices=["Arts", "Science"])
    labincluded = BooleanField("Lab Included")
    labfees_year = IntegerField("Lab Fees Year")
    annual_labfees = IntegerField("Annual Lab Fees")
    


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


class DetailsForm(FlaskForm):
    department = QuerySelectField(
        'Department',
        query_factory=lambda: Department.query.all(),
        allow_blank=False,
        get_label='dname',
        render_kw={
            "class": "form-control",
            "id": "department-select",
            "hx-get": '/api/get_guides_opt',  
            "hx-target": "#guide-select",
            "hx-trigger": "change"
        }
    )

    guide = SelectField(
        'Guide',
        choices=[],  # Initially empty, populated dynamically by HTMX
        render_kw={"id": "guide-select", "class": "form-control"}
    )

    status = QuerySelectField(
        'Current Status',
        query_factory=lambda: Status.query.all(),
        allow_blank=False,
        get_label='current_status',
        validators=[DataRequired()]
    )
    
    guide_role = SelectField("Guide Role", choices=[("Guide", "Guide"), ("Co-Guide", "Co-Guide")])
    scholar_name = StringField("Scholar Name", validators=[DataRequired()])
    gender = StringField("Gender", validators=[DataRequired()])
    regno = StringField("Registration Number", validators=[Optional()])
    dob = DateField("Date of Birth", validators=[Optional()])
    timing = SelectField("Timing", choices=[("Part-Time", "Part-Time"), ("Full-Time", "Full-Time")])
    caste = StringField("Caste", validators=[Optional()])
    subcaste = StringField("Sub Caste", validators=[Optional()])
    religion = StringField("Religion", validators=[Optional()])
    email = StringField("Email", validators=[Optional()])
    phno = StringField("Phone No.", validators=[Optional()])
    optionalphno = StringField("Optional Phone No.", validators=[Optional()])
    address = TextAreaField("Residential Address", validators=[Optional()])
    commencement_date = DateField("Commencement Date", validators=[Optional()])
    join_date = DateField("Date of Joining", validators=[Optional()])
    last_fee_date = DateField("Last Fee Date", validators=[Optional()])
    annual_fee = IntegerField("Annual Fees", validators=[Optional()])
    tution_fees_paid = IntegerField("Tuition Fees Paid", validators=[Optional()])
    labfees_paid = IntegerField("Lab Fees Paid", validators=[Optional()])
    no_due_date = DateField("No Due Issued Date", validators=[Optional()])
    viva_date = DateField("Viva Date", validators=[Optional()])
    thesis_title = TextAreaField("Thesis Title", validators=[Optional()])
    first_dc_meet = DateField("1st DC Meeting Date", validators=[Optional()])
    first_dc_fee = IntegerField("1st DC Meeting Fees", validators=[Optional()])
    second_dc_meet = DateField("2nd DC Meeting Date", validators=[Optional()])
    second_dc_fee = IntegerField("2nd DC Meeting Fees", validators=[Optional()])
    third_dc_meet = DateField("3rd DC Meeting Date", validators=[Optional()])
    third_dc_fee = IntegerField("3rd DC Meeting Fees", validators=[Optional()])


class FeesUpdateForm(FlaskForm):
    department = QuerySelectField(
        'Department',
        query_factory=lambda: Department.query.all(),
        allow_blank=False,
        get_label='dname',
        render_kw={
            "class": "form-control",
            "id": "department-select",
            "hx-get": '/api/get_guides_scholar',  
            "hx-target": "#scholar-select",
            "hx-trigger": "change"
        }
    )


    scholar_name = SelectField(
        'Scholar Name',
        choices=[],
        render_kw={"id": "scholar-select", "class": "form-control"}
    )

    tution_fees_paid = IntegerField("Tuition Fees Paid", validators=[Optional()])

    labfees_paid = IntegerField("Lab Fees Paid", validators=[Optional()])
 