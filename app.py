from flask import Flask, render_template, jsonify, send_file, redirect, url_for
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from views import *
from export import *
from docx import *
from docx.shared import *
from docx.enum.text import *
import os, json

config = json.loads(open("config.json", "r").read())


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://root:{config["password"]}@localhost/{config["dbname"]}"
app.config['FLASK_ADMIN_FLUID_LAYOUT'] = True
app.config['WORD_FILES'] = os.path.join(os.path.dirname(__file__), 'word')
db.init_app(app)
admin = Admin(app,template_mode='bootstrap4', name="Phd Scholar Archive", index_view=CustomAdminModelView())
app.secret_key = "23i7jkb8734rjh"


admin.add_view(DepartmentModelView(Department, db.session, category="Tables"))
admin.add_view(GuideModelView(db.session, category="Tables"))
admin.add_view(StatusModelView(Status, db.session, category="Tables"))
admin.add_view(DetailsModelView(db.session, category="Tables"))

@app.route("/api/unpaid")
def unpaid_scholars():
    with_lab_departments = [str(dept) for dept in db.session.query(Department).filter(Department.labincluded == 1).all()]
    without_lab_departments = [str(dept) for dept in db.session.query(Department).filter(Department.labincluded == 0).all()]

    exporter = UnpaidExporter()
    exporter.doc = Document()

    for department in without_lab_departments:
        exporter.add_heading(department)
        details = exporter.get_doing_scholars(department, False)
        exporter.insert_without_lab_data(details)
    
    for department in with_lab_departments:
        exporter.add_heading(department)
        details = exporter.get_doing_scholars(department, True)
        exporter.insert_with_lab_data(details)

    file_path = os.path.join(app.config['WORD_FILES'], "fees_unpaid_details.docx")
    exporter.doc.save(file_path)
    return send_file(file_path, as_attachment=True)

@app.route("/api/category_sort")
def category_sort():
    department_list = [str(dept) for dept in Department.query.all()]
    document = Document()
    table_word_file = CatagoryExporter(document)
    
    # Male Data
    table_word_file.add_heading("Male")
    male_table = table_word_file.create_table()
    table_word_file.insert_data(male_table, department_list, "Male")
    
    # Female Data
    table_word_file.add_heading("\nFemale")
    female_table = table_word_file.create_table()
    table_word_file.insert_data(female_table, department_list, "Female")

    file_path = os.path.join(app.config['WORD_FILES'], "caste_category_details.docx")
    document.save(file_path)
    return send_file(os.path.join(app.config['WORD_FILES'], "caste_category_details.docx"), as_attachment=True)


@app.route("/api/awarded_sort")
def awarded_sort():
    department_list = [str(dept) for dept in Department.query.all()]
    exporter = AwardedExporter(db.session)
    document = Document()
    exporter.doc = document

    for department in department_list:
        years = exporter.get_awarded_year(department)
        exporter.add_heading(department)
        table = exporter.create_table()

        for index, year in enumerate(years):
            data = exporter.awarded_sort(year, department)
            exporter.insert_data(data, table, year, index + 1)
        unknown_data = exporter.unknown_awarded_sort(department)
        exporter.insert_data(unknown_data, table, 'Unknown', len(years) + 1)

    file_path = os.path.join(app.config['WORD_FILES'], "awarded_details.docx")
    document.save(file_path)
    return send_file(file_path, as_attachment=True)
    
@app.route("/api/export_all")
def exportall():
    exporter = ExcelDataExport(db.session, os.path.join(app.config['WORD_FILES'], "scholars_details.xlsx"))
    exporter.export()
    return send_file(os.path.join(app.config['WORD_FILES'], "scholars_details.xlsx"), as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)

