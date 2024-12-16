from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, text

db = SQLAlchemy()


class Department(db.Model):
    __tablename__ = 'department'
    
    dno = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    dname = db.Column(db.String(50), unique=True, nullable=False)
    dtype = db.Column(db.String(20), nullable=False)
    labincluded = db.Column(db.Boolean, nullable=False)
    annual_labfees = db.Column(db.BigInteger)
    labfees_year = db.Column(db.BigInteger)
    
    guides = db.relationship('Guide', back_populates='department', lazy=True)
    scholars = db.relationship('Details', back_populates='department', lazy=True)

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
    dno = db.Column(db.BigInteger, db.ForeignKey('department.dno'), nullable=False)
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
    annual_fee = db.Column(db.BigInteger, nullable=True)
    #Auto Calculation
    total_tution_fees = db.Column(db.BigInteger, nullable=True)
    total_lab_fees = db.Column(db.BigInteger, nullable=True)
    total_center_fees = db.Column(db.BigInteger, nullable=True) # Automatic Calculation

    last_fee_date = db.Column(db.Date, nullable=True)
    tution_fees_paid = db.Column(db.BigInteger, nullable=True) 
    labfees_paid = db.Column(db.BigInteger, nullable=True)
    
    #Auto Calculation
    tution_fees_unpaid = db.Column(db.BigInteger)
    labfees_unpaid = db.Column(db.BigInteger, nullable=True) 
    total_fees_unpaid = db.Column(db.BigInteger, nullable=True) 
    
    no_due_date = db.Column(db.Date, nullable=True)
    viva_date = db.Column(db.Date, nullable=True)
    thesis_title = db.Column(db.Text, nullable=True)
    statusno = db.Column(db.BigInteger, db.ForeignKey('status_.statusno'), nullable=False)
    first_dc_meet = db.Column(db.Date, nullable=True)
    first_dc_fee = db.Column(db.BigInteger, nullable=True)

    second_dc_meet = db.Column(db.Date, nullable=True)
    second_dc_fee = db.Column(db.BigInteger, nullable=True)

    third_dc_meet = db.Column(db.Date, nullable=True)
    third_dc_fee = db.Column(db.BigInteger, nullable=True)
    
    department = db.relationship('Department', back_populates='scholars')
    guide = db.relationship('Guide', back_populates='scholars')
    status = db.relationship('Status', back_populates='scholars')
    



# @event.listens_for(Details, 'after_insert')
# @event.listens_for(Details, 'after_update')
# def calculate_fees_unpaid(mapper, connection, target):
#     # Query to get labincluded from department using scholar_id
#     fetch_sql = text("""
#     SELECT d.labincluded 
#     FROM department d
#     JOIN details dt ON dt.dno = d.dno
#     WHERE dt.scholar_id = :scholar_id
#     """)

#     result = connection.execute(fetch_sql, {'scholar_id': target.scholar_id}).fetchone()
#     is_labincluded = result[0] if result[0] == 1 else False  # Default to False if not found

#     # Update the details table with the calculated total fees
#     annual_labfees  = 2000 if is_labincluded else 0
#     update_sql = text("""
#     UPDATE details
#     SET total_tution_fees = total_tution_fees(:join_date, :annual_fee),
#         total_lab_fees = total_labfees(:join_date, :annual_labfees)
#     WHERE scholar_id = :scholar_id
#     """)

#     connection.execute(update_sql, {
#         'join_date': target.join_date,
#         'annual_fee': target.annual_fee,
#         'annual_labfees': annual_labfees,
#         'scholar_id': target.scholar_id  
#     })


#     refresh_sql = text("""
#     SELECT total_tution_fees, total_lab_fees, tution_fees_paid, labfees_paid
#     FROM details 
#     WHERE scholar_id = :scholar_id
#     """)

#     updated_values = connection.execute(refresh_sql, {'scholar_id': target.scholar_id}).fetchone()

#     if updated_values:
#         tutionfees, labfees, tutionfeespaid, labfeespaid = updated_values
#         print("tutionfees: " , tutionfees)

#         # Calculation of values
#         if is_labincluded:
#             total_center_fees = tutionfees + labfees
#             tutionfees_unpaid = tutionfees - tutionfeespaid
#             labfees_unpaid = labfees - labfeespaid
#             total_fees_unpaid = tutionfees_unpaid + labfees_unpaid
#         else:
#             total_center_fees = tutionfees
#             tutionfees_unpaid = tutionfees - tutionfeespaid
#             labfees_unpaid =   0
#             total_fees_unpaid = tutionfees_unpaid
        
#         print(total_center_fees, tutionfees_unpaid, labfees_unpaid, total_fees_unpaid)

#         print(total_center_fees, tutionfees_unpaid, labfees_unpaid, total_fees_unpaid)
#         print(total_center_fees, tutionfees_unpaid, labfees_unpaid, total_fees_unpaid)
#         print(total_center_fees, tutionfees_unpaid, labfees_unpaid, total_fees_unpaid)
#         print(total_center_fees, tutionfees_unpaid, labfees_unpaid, total_fees_unpaid) 

#         # Update unpaid fees
#         update_fees_sql = text("""
#         UPDATE details
#         SET total_center_fees = :total_center_fees,
#             tution_fees_unpaid = :tutionfees_unpaid,
#             labfees_unpaid = :labfees_unpaid,
#             total_fees_unpaid = :total_fees_unpaid
#         WHERE scholar_id = :scholar_id
#         """)

#         connection.execute(update_fees_sql, {
#             'total_center_fees': total_center_fees,
#             'tutionfees_unpaid': tutionfees_unpaid,
#             'labfees_unpaid': labfees_unpaid,
#             'total_fees_unpaid': total_fees_unpaid,
#             'scholar_id': target.scholar_id
#         })


# @event.listens_for(Guide, 'after_update')
# def update_for_guide_department_change(mapper, connection, target):
#     # labincluded_fetch_sql = text("""
#     # SELECT d.labincluded 
#     # FROM department d
#     # JOIN guide gt ON gt.dno = d.dno
#     # WHERE gt.gno = :guide_no
#     # """)

#     # result = connection.execute(labincluded_fetch_sql, {'guide_no': target.gno}).fetchone()
#     # is_labincluded = result[0] if result[0] == 1 else False

#     scholars_fetch_sql = text("""
#     SELECT scholar_id, join_date, total_center_fees,
#     labfees_unpaid, total_fees_unpaid from
#     details WHERE gno=:guide_no
#     """)
#     scholars = connection.execute(scholars_fetch_sql, {'guide_no': target.gno}).all()
    
#     for scholar in scholars:
#         # if is_labincluded:
#         #     annual_labfees  = 2000 if is_labincluded else 0

#         #     labfees_sql = text("""
#         #         SELECT total_labfees(:join_date, :annual_labfees)
#         #     """)

#         #     total_labfees = int(connection.execute(labfees_sql, {
#         #         'join_date': scholar[1],
#         #         'annual_labfees': annual_labfees,
#         #     }).fetchone()[0])

#         #     total_center_fees = int(scholar[2]) + total_labfees
#         #     labfees_unpaid = int(scholar[3]) + total_labfees
#         #     total_fees_unpaid = int(scholar[4]) + total_labfees

#         #     update_sql = text("""
#         #     UPDATE details
#         #     SET total_lab_fees = :total_labfees,
#         #         total_center_fees = :total_center_fees,
#         #         labfees_unpaid = :labfees_unpaid,
#         #         total_fees_unpaid = :total_fees_unpaid,
#         #         dno = :dno
#         #     WHERE scholar_id = :scholar_id
#         #     """)

#         #     connection.execute(update_sql, {
#         #     'join_date': scholar[1],
#         #     'total_labfees':total_labfees,
#         #     'total_center_fees' :total_center_fees,
#         #     'labfees_unpaid' :labfees_unpaid,
#         #     'total_fees_unpaid' : total_fees_unpaid,
#         #     'annual_labfees': annual_labfees,
#         #     'scholar_id': scholar[0],
#         #     'dno' : target.dno
#         #     })
        
#         # else:
#             update_sql = text("""
#             UPDATE details
#             SET dno = :dno
#             WHERE scholar_id = :scholar_id
#             """)
#             connection.execute(update_sql, {
#             'scholar_id': scholar[0],
#             'dno' : target.dno
#             })




# @event.listens_for(Department, 'after_update')
# def update_for_department_lab_change(mapper, connection, target):
#     labincluded_fetch_sql = text("""
#         SELECT labincluded FROM department WHERE dno = :dno
#     """)

#     result = connection.execute(labincluded_fetch_sql, {
#         'dno': target.dno
#     }).fetchone()

#     labincluded = result[0] if result[0] == 1 else False

#     if labincluded:
#         scholars_fetch_sql = text("""
#         SELECT scholar_id, join_date, total_center_fees,
#         labfees_unpaid, total_fees_unpaid from
#         details WHERE dno=:dno
#         """)
#         scholars = connection.execute(scholars_fetch_sql, {'dno': target.dno}).all()

#         for scholar in scholars:
#             annual_labfees  = 2000 if labincluded else 0

#             labfees_sql = text("""
#                 SELECT total_labfees(:join_date, :annual_labfees)
#             """)

#             total_labfees = int(connection.execute(labfees_sql, {
#                 'join_date': scholar[1],
#                 'annual_labfees': annual_labfees,
#             }).fetchone()[0])

#             total_center_fees = int(scholar[2]) + total_labfees
#             labfees_unpaid = int(scholar[3]) + total_labfees
#             total_fees_unpaid = int(scholar[4]) + total_labfees

#             update_sql = text("""
#             UPDATE details
#             SET total_lab_fees = :total_labfees,
#                 total_center_fees = :total_center_fees,
#                 labfees_unpaid = :labfees_unpaid,
#                 total_fees_unpaid = :total_fees_unpaid
#             WHERE scholar_id = :scholar_id
#             """)

#             connection.execute(update_sql, {
#             'join_date': scholar[1],
#             'total_labfees':total_labfees,
#             'total_center_fees' :total_center_fees,
#             'labfees_unpaid' :labfees_unpaid,
#             'total_fees_unpaid' : total_fees_unpaid,
#             'annual_labfees': annual_labfees,
#             'scholar_id': scholar[0] 
#             })



@event.listens_for(Details, 'after_insert')
@event.listens_for(Details, 'after_update')
def calculate_fees_unpaid(mapper, connection, target):
    # Fetch lab-included status
    fetch_sql = text("""
    SELECT d.labincluded, d.labfees_year, d.annual_labfees
    FROM department d
    JOIN details dt ON dt.dno = d.dno
    WHERE dt.scholar_id = :scholar_id
    """)

    result = connection.execute(fetch_sql, {'scholar_id': target.scholar_id}).fetchone()
    is_labincluded = result and result[0] == 1
    labfees_year = result[1] if is_labincluded else 0
    

    # Calculate fees
    annual_labfees = result[2] if is_labincluded else 0
    update_fees_sql = text("""
    UPDATE details
    SET total_tution_fees = total_tution_fees(:join_date, :annual_fee),
        total_lab_fees = total_labfees(:join_date, :annual_labfees, :labfees_year)
    WHERE scholar_id = :scholar_id
    """)

    connection.execute(update_fees_sql, {
        'join_date': target.join_date,
        'annual_fee': target.annual_fee,
        'annual_labfees': annual_labfees,
        'labfees_year': labfees_year,
        'scholar_id': target.scholar_id
    })

    # Refresh updated values
    refresh_sql = text("""
    SELECT total_tution_fees, total_lab_fees, tution_fees_paid, labfees_paid
    FROM details 
    WHERE scholar_id = :scholar_id
    """)

    updated_values = connection.execute(refresh_sql, {'scholar_id': target.scholar_id}).fetchone()

    if updated_values:
        tutionfees, labfees, tutionfeespaid, labfeespaid = updated_values

        # Calculate unpaid fees
        total_center_fees = tutionfees + (labfees if is_labincluded else 0)
        tutionfees_unpaid = tutionfees - tutionfeespaid
        labfees_unpaid = labfees - labfeespaid if is_labincluded else 0
        total_fees_unpaid = tutionfees_unpaid + labfees_unpaid

        # Update unpaid fees
        update_fees_unpaid_sql = text("""
        UPDATE details
        SET total_center_fees = :total_center_fees,
            tution_fees_unpaid = :tutionfees_unpaid,
            labfees_unpaid = :labfees_unpaid,
            total_fees_unpaid = :total_fees_unpaid
        WHERE scholar_id = :scholar_id
        """)

        connection.execute(update_fees_unpaid_sql, {
            'total_center_fees': total_center_fees,
            'tutionfees_unpaid': tutionfees_unpaid,
            'labfees_unpaid': labfees_unpaid,
            'total_fees_unpaid': total_fees_unpaid,
            'scholar_id': target.scholar_id
        })



@event.listens_for(Guide, 'after_update')
def update_for_guide_department_change(mapper, connection, target):
    # Update department only if changed
    scholars_fetch_sql = text("""
    SELECT scholar_id, dno 
    FROM details 
    WHERE gno = :guide_no
    """)

    scholars = connection.execute(scholars_fetch_sql, {'guide_no': target.gno}).all()

    for scholar_id, current_dno in scholars:
        if current_dno != target.dno:
            update_sql = text("""
            UPDATE details
            SET dno = :new_dno
            WHERE scholar_id = :scholar_id
            """)
            connection.execute(update_sql, {
                'scholar_id': scholar_id,
                'new_dno': target.dno
            })


@event.listens_for(Department, 'after_update')
def update_for_department_lab_change(mapper, connection, target):
    # Check if department is lab-included
    labincluded_fetch_sql = text("""
    SELECT labincluded, labfees_year, annual_labfees FROM department WHERE dno = :dno
    """)

    result = connection.execute(labincluded_fetch_sql, {'dno': target.dno}).fetchone()
    labincluded = result and result[0] == 1
    labfees_year = result[1] if labincluded else 0

    # Fetch scholars linked to the department
    scholars_fetch_sql = text("""
    SELECT scholar_id, join_date, total_center_fees, labfees_unpaid, total_fees_unpaid 
    FROM details 
    WHERE dno = :dno
    """)

    scholars = connection.execute(scholars_fetch_sql, {'dno': target.dno}).all()

    for scholar in scholars:
        # If the department includes lab fees, calculate them; otherwise, set them to 0
        annual_labfees = result[2] if labincluded else 0
        total_labfees = 0

        if labincluded:
            labfees_sql = text("""
            SELECT total_labfees(:join_date, :annual_labfees, :labfees_year)
            """)
            total_labfees = int(connection.execute(labfees_sql, {
                'join_date': scholar[1],
                'annual_labfees': annual_labfees,
                'labfees_year': labfees_year
            }).fetchone()[0])

        # Recalculate the total fees without including the old lab fees if no lab is included
        total_center_fees = int(scholar[2]) - int(scholar[3]) + total_labfees  # Subtract old lab fees if present
        labfees_unpaid = total_labfees  # Lab fees unpaid should only include the new lab fees (or 0 if no lab fees)
        total_fees_unpaid = int(scholar[4]) - int(scholar[3]) + labfees_unpaid  # Subtract old unpaid lab fees if present

        update_sql = text("""
        UPDATE details
        SET total_lab_fees = :total_labfees,
            total_center_fees = :total_center_fees,
            labfees_unpaid = :labfees_unpaid,
            total_fees_unpaid = :total_fees_unpaid
        WHERE scholar_id = :scholar_id
        """)

        connection.execute(update_sql, {
            'total_labfees': total_labfees,
            'total_center_fees': total_center_fees,
            'labfees_unpaid': labfees_unpaid,
            'total_fees_unpaid': total_fees_unpaid,
            'scholar_id': scholar[0]
        })
