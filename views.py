from models import *
from flask_admin.contrib.sqla import ModelView
from forms import *
from sqlalchemy.exc import DataError
from flask_admin.form import rules
from sqlalchemy import or_
from flask import request, url_for, flash, render_template, redirect, jsonify
from flask_admin import form
from flask_admin.contrib.sqla.filters import FilterInList
from filters import *
from flask_admin import Admin, BaseView, expose, AdminIndexView
from datetime import date


class DepartmentModelView(ModelView):
    column_list = ('dno', 'dname', 'dtype', 'labincluded', 'labfees_year', 'annual_labfees')
    column_labels = {
        'dno': 'Department Number',
        'dname': 'Department Name',
        'dtype': 'Department Type',
        'labincluded': 'Lab Included',
        'labfees_year': "Lab Fees Year",
        'annual_labfees': "Annual Lab Fees"
    }
    form = DepartmentForm


class GuideModelView(ModelView):
    column_list = ('gno', 'guide_name', 'department')
    form_columns = ('guide_name', 'department')
    column_searchable_list = ('guide_name',)  # Only search by guide_name
    can_export = True
    export_types = ['xlsx']

    column_labels = {
        'gno': 'Guide ID',
        'guide_name': 'Guide Name',
        'department': 'Department'
    }

    def __init__(self, session, **kwargs):
        super(GuideModelView, self).__init__(Guide, session, **kwargs)

    def scaffold_list(self, *args, **kwargs):
        return ['gno', 'guide_name', 'department']

    def scaffold_form(self):
        form_class = super(GuideModelView, self).scaffold_form()
        return form_class

    def create_model(self, form):
        try:
            department = form.department.data
            new_guide = Guide(
                guide_name=form.guide_name.data,
                dno=department.dno
            )
            self.session.add(new_guide)
            self.session.commit()
            return new_guide
        except Exception as e:
            self.session.rollback()
            raise e

    def edit_model(self, form):
        try:
            guide = self.session.get(Guide, form.gno.data)
            if not guide:
                raise ValueError("Guide not found")

            guide.guide_name = form.guide_name.data
            department = form.department.data
            if department:
                guide.dno = department.dno
            else:
                raise ValueError("Department not found or invalid")

            self.session.commit()
            return guide
        except Exception as e:
            self.session.rollback()
            raise e

class StatusModelView(ModelView):
    form = StatusForm



class DetailsModelView(ModelView):
    form = DetailsForm    
    
    column_list = ('scholar_id', 'guide.department.dname', 'guide', 'scholar_name', 'gender', 'regno', 'dob', 'timing',
                   'caste', 'subcaste', 'religion', 'email', 'phno', 'optionalphno' , 'address', 'commencement_date', 'join_date', 'annual_fee', 
                   'total_tution_fees', 'total_lab_fees','total_center_fees', 'last_fee_date' ,'tution_fees_paid', 'labfees_paid',
                   'tution_fees_unpaid', 'labfees_unpaid', 'total_fees_unpaid' ,'no_due_date', 'viva_date', 'thesis_title', 'status.current_status',
                   'first_dc_meet', 'first_dc_fee', 'second_dc_meet', 'second_dc_fee', 'third_dc_meet', 'third_dc_fee')
    
    column_labels = {
        'scholar_id': 'Scholar ID',
        'guide.department.dname': 'Department',
        'guide': 'Guide',
        'scholar_name': 'Scholar Name',
        'gender': 'Gender',
        'regno': 'Registration Number',
        'dob': 'Date of Birth',
        'timing': 'Timing',
        'caste': 'Caste',
        'subcaste': 'Subcaste',
        'religion': 'Religion',
        'email': 'Email',
        'phno' : 'Phone No. ',
        'optionalphno' : 'Optional Phone No. ',
        'address': 'Address',
        'commencement_date': 'Commencement Date',
        'join_date': 'Join Date',
        'annual_fee': 'Annual Fee',
        'total_center_fees': 'Total Center Fees',
        'tution_fees_paid': 'Tuition Fees Paid',
        'tution_fees_unpaid': 'Tuition Fees Unpaid',
        'labfees_unpaid': 'Lab Fees Unpaid',
        'total_fees_unpaid': 'Total Fees Unpaid',
        'labfees_paid': 'Lab Fees Paid',
        'last_fee_date': 'Last Fee Date',
        'total_tution_fees': 'Total Tuition Fees',
        'total_lab_fees': 'Total Lab Fees',
        'no_due_date': 'No Due Date',
        'viva_date': 'Viva Date',
        'thesis_title': 'Thesis Title',
        'status.current_status': 'Current Status',
        'first_dc_meet': '1st DC Date',
        'first_dc_fee': '1st DC Fee',
        'second_dc_meet': '2nd DC Date',
        'second_dc_fee': '2nd DC Fee',
        'third_dc_meet': '3rd DC Date',
        'third_dc_fee': '3rd DC Fee',
    }


    column_searchable_list = ('scholar_name',)
    can_export = True
    export_types = ['xlsx']
    column_filters = [
        FilterByDepartment(column='guide.department.dname', name='Department'),
        FilterByCurrentStatus(column='details.status.current_status', name='Current Status'),
        FilterByTiming(column='details.timing', name="Timing")
    ]
    
   
    def __init__(self, session, category="Tables", **kwargs):
        super(DetailsModelView, self).__init__(Details, session, category=category, **kwargs)
    
    def create_form(self):
        form = super(DetailsModelView, self).create_form()
        return form
    
    @expose('/create/', methods=['GET', 'POST'])
    def create_view(self):
        form = self.create_form()
        if form.is_submitted():
            # Process the form data and save the new record
            form = request.form

            obj = Details(
                dno=form["department"],  # Remove int() if 'dno' is already an integer or can be converted later
                gno=form["guide"],       # Remove int() if 'gno' is already an integer or can be converted later
                guide_role=form["guide_role"],
                scholar_name=form["scholar_name"] if form["scholar_name"] != "" else "" ,
                gender=form["gender"] if form["gender"] != "" else "",
                regno=form["regno"] if form["regno"] != "" else "",
                dob=form["dob"] if form["dob"] != "" else None,  # Ensure 'dob' is passed in the correct date format
                timing=form["timing"],
                caste=form["caste"] if form["caste"] != "" else "",
                subcaste=form["subcaste"] if form["subcaste"] != "" else "",
                religion=form["religion"] if form["religion"] != "" else "",
                email=form["email"] if form["email"] != "" else "",
                phno=form["phno"] if form["phno"] != "" else "",
                optionalphno=form["optionalphno"] if form["optionalphno"] != "" else "",  # Fixed typo: should be form["optionalphno"]
                address=form["address"] if form["address"] != "" else "",
                commencement_date=form["commencement_date"] if form["commencement_date"] != "" else None,  # Ensure date format is correct
                join_date=form["join_date"] if form["join_date"] != "" else None,                  # Ensure date format is correct
                last_fee_date=form["last_fee_date"] if form["last_fee_date"] != "" else None,          # Ensure date format is correct
                annual_fee=form["annual_fee"] if form["annual_fee"] != "" else 0,                 # Remove int() if not required
                labfees_paid=form["labfees_paid"] if form["labfees_paid"] != "" else 0,                       # Remove int() if not required
                tution_fees_paid=form["tution_fees_paid"] if form["tution_fees_paid"] != "" else 0,                   # Remove int() if not required
                no_due_date=form["no_due_date"] if form["no_due_date"] != "" else None,               # Ensure date format is correct
                viva_date=form["viva_date"] if form["viva_date"] != "" else None,                   # Ensure date format is correct
                thesis_title=form["thesis_title"] if form["thesis_title"] != "" else "",
                statusno=form["status"],                     # Remove int() if not required
                first_dc_meet=form["first_dc_meet"] if form["first_dc_meet"] != "" else None,       # Ensure date format is correct
                first_dc_fee=form["first_dc_fee"] if form["first_dc_fee"] != "" else 0,
                second_dc_meet=form["second_dc_meet"] if form["second_dc_meet"] != "" else None,       # Ensure date format is correct
                second_dc_fee=form["second_dc_fee"] if form["second_dc_fee"] != "" else 0,
                third_dc_meet=form["third_dc_meet"] if form["third_dc_meet"] != "" else None,       # Ensure date format is correct
                third_dc_fee=form["third_dc_fee"] if form["third_dc_fee"] != "" else 0,
            )

            self.session().add(obj)
            self.session().commit()
            return redirect("/admin/details/")
        
          # Redirect to index after successful creation

        return self.render('admin/details_create.html', form=form)
    
    @expose("/edit/", methods=['GET', 'POST'])
    def edit_view(self):
        if request.method == "GET":
            scholar_id = request.args.get("id")
            obj = self.session.query(Details).get(scholar_id)
            guide_name = Guide.query.filter_by(gno=obj.gno).one()
            print(guide_name)
            # Check if the object is found
            if not obj:
                flash('Record not found!', 'error')
                return redirect("/admin/details/")
            
            # Populate the form with existing object data
            form = self.edit_form(obj)
            
            
            return self.render('admin/details_edit.html', form=form, obj=obj, guide_name=guide_name)

    
    @expose("/update/", methods=["POST"])
    def update_view(self):
        if request.method == 'POST':
            scholar_id = request.form.get("scholar_id")  # Ensure scholar_id is passed in the form
            obj = self.session.query(Details).get(scholar_id)
            if not obj:
                flash('Record not found!', 'error')
                return redirect("/admin/details/")
            
            print(request.form["dob"])

            # Update the fields with the form data
            obj.dno = request.form["department"]
            obj.gno = request.form["guide"]
            obj.guide_role = request.form["guide_role"]
            obj.scholar_name = request.form["scholar_name"] if request.form["scholar_name"] != "" else ""
            obj.gender = request.form["gender"] if request.form["gender"] != "" else ""
            obj.regno = request.form["regno"] if request.form["regno"] != "" else ""
            obj.dob = request.form["dob"] if request.form["dob"] != "" else None  # Set to None if empty
            obj.timing = request.form["timing"]
            obj.caste = request.form["caste"] if request.form["caste"] != "" else ""
            obj.subcaste = request.form["subcaste"] if request.form["subcaste"] != "" else ""
            obj.religion = request.form["religion"] if request.form["religion"] != "" else ""
            obj.email = request.form["email"] if request.form["email"] != "" else ""
            obj.phno = request.form["phno"] if request.form["phno"] != "" else ""
            obj.optionalphno = request.form["optionalphno"] if request.form["optionalphno"] != "" else ""  # Handle empty optional phone number
            obj.address = request.form["address"] if request.form["address"] != "" else ""
            obj.commencement_date = request.form["commencement_date"] if request.form["commencement_date"] != "" else None  # Set to None if empty
            obj.join_date = request.form["join_date"] if request.form["join_date"] != "" else None  # Set to None if empty
            obj.last_fee_date = request.form["last_fee_date"] if request.form["last_fee_date"] != "" else None  # Set to None if empty
            obj.annual_fee = int(request.form["annual_fee"]) if request.form["annual_fee"] != "" else 0
            obj.labfees_paid = int(request.form["labfees_paid"]) if request.form["labfees_paid"] != "" else 0
            obj.tution_fees_paid = int(request.form["tution_fees_paid"]) if request.form["tution_fees_paid"] != "" else 0
            obj.no_due_date = request.form["no_due_date"] if request.form["no_due_date"] != "" else None  # Set to None if empty
            obj.viva_date = request.form["viva_date"] if request.form["viva_date"] != "" else None  # Set to None if empty
            obj.thesis_title = request.form["thesis_title"] if request.form["thesis_title"] != "" else ""
            obj.statusno = request.form["status"]
            obj.first_dc_meet = request.form["first_dc_meet"] if request.form["first_dc_meet"] != "" else None  # Set to None if empty
            obj.first_dc_fee = int(request.form["first_dc_fee"]) if request.form["first_dc_fee"] != "" else 0
            obj.second_dc_meet = request.form["second_dc_meet"] if request.form["second_dc_meet"] != "" else None  # Set to None if empty
            obj.second_dc_fee = int(request.form["second_dc_fee"]) if request.form["second_dc_fee"] != "" else 0
            
            obj.third_dc_meet = request.form["third_dc_meet"] if request.form["third_dc_meet"] != "" else None  # Set to None if empty
            obj.third_dc_fee = int(request.form["third_dc_fee"]) if request.form["third_dc_fee"] != "" else 0


            # Commit changes to the database
            self.session.commit()

            flash('Record updated successfully!', 'success')
            return redirect("/admin/details/")

class FeesUpdateView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def update(self):
        print("Update view called")
        form = FeesUpdateForm()
        
        if form.is_submitted():
            print(form.data)
            # Fetch the data from the form
            department_id = form.department.data
            scholar_id = form.scholar_name.data
            tuition_fees_paid = form.tution_fees_paid.data
            labfees_paid = form.labfees_paid.data

            # Query for the scholar to update
            scholar = Details.query.get(scholar_id)
            if not scholar:
                flash('Scholar not found', 'danger')
                return redirect(url_for('feesupdateview.update'))

            # Update the fees
            scholar.tution_fees_paid = scholar.tution_fees_paid + tuition_fees_paid
            scholar.labfees_paid = scholar.labfees_paid + labfees_paid
            scholar.last_fee_date = date.today()

            # Commit the changes to the database
            db.session.commit()
            flash('Fees updated successfully!', 'success')
            return redirect(url_for('feesupdateview.update'))

        # Render the template with the form
        return self.render('admin/fees_update.html', form=form)
            
class CustomAdminModelView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/model/master.html")
