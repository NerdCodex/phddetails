from models import *
from flask_admin.contrib.sqla import ModelView
from forms import *
from sqlalchemy.exc import DataError
from flask_admin.form import rules
from sqlalchemy import or_
from flask import request
from flask_admin import form
from flask_admin.contrib.sqla.filters import FilterInList
from filters import *
from flask_admin import Admin, BaseView, expose, AdminIndexView


class DepartmentModelView(ModelView):
    column_list = ('dno', 'dname', 'dtype', 'labincluded')
    column_labels = {
        'dno': 'Department Number',
        'dname': 'Department Name',
        'dtype': 'Department Type',
        'labincluded': 'Lab Included'
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
                   'caste', 'subcaste', 'religion', 'email', 'phno', 'optionalphno' , 'address', 'commencement_date', 'join_date', 'last_fee_date', 
                   'total_center_fees', 'annual_fee','fees_paid','labfees', 'no_due_date', 'viva_date', 'thesis_title', 'status.current_status',
                   'dc_meeting_date', 'dc_meeting', 'dc_meeting_fee')
    
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
        'last_fee_date': 'Last Fee Date',
        'total_center_fees': 'Total Center Fees',
        'annual_fee': 'Annual Fee',
        'fees_paid': 'Fees Paid',
        'labfees': 'Lab Fees',
        'no_due_date': 'No Due Date',
        'viva_date': 'Viva Date',
        'thesis_title': 'Thesis Title',
        'status.current_status': 'Current Status',
        'dc_meeting_date': 'DC Meeting Date',
        'dc_meeting': 'DC Meeting',
        'dc_meeting_fee': 'DC Meeting Fee'
    }


    column_searchable_list = ('scholar_name',)
    can_export = True
    export_types = ['xlsx']
    column_filters = [
        FilterByDepartment(column='guide.department.dname', name='Department'),
        FilterByCurrentStatus(column='details.status.current_status', name='Current Status'),
        FilterByTiming(column='details.timing', name="Timing")
    ]

    def __init__(self, session, **kwargs):
        super(DetailsModelView, self).__init__(Details, session, **kwargs)

class CustomAdminModelView(AdminIndexView):
    @expose("/")
    def index(self):
        return self.render("admin/model/master.html")
