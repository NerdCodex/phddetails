use phddetails;

/* Department table */

create table department(
	dno bigint auto_increment,
    dname varchar(50),
    dtype varchar(20),
    labincluded boolean,
    constraint dno_pk primary key (dno),
    constraint dname_uk unique (dname)    
);

SET SQL_SAFE_UPDATES = 0;

/* Guide Table*/
create table guide(
	gno bigint auto_increment,
    guide_name varchar(100),
    dno bigint,
    constraint gno_pk primary key (gno),
    constraint guide_name_uk unique (guide_name),
    constraint dno_fk foreign key (dno) references department(dno)
);
truncate table guide;


/* Status Table */
create table status_(
	statusno bigint auto_increment,
	current_status varchar(100),
    constraint statusno_pk primary key (statusno),
    constraint current_status_unique unique (current_status)
);

create table details(
    scholar_id bigint auto_increment,
    gno bigint,
    guide_role varchar(10),
    scholar_name varchar(100),
    gender varchar(10),
    regno varchar(100),
    dob date,
    timing varchar(10),
    caste varchar(100),
    subcaste varchar(100),
    religion varchar(100),
    email varchar(100),
    phno varchar(15),
    optionalphno varchar(15),
    address varchar(100),
    commencement_date date,
    join_date date,
    last_fee_date date,
    total_center_fees BIGINT,
    annual_fee BIGINT,  
    fees_paid BIGINT,
    no_due_date date,
    viva_date date,
    thesis_title mediumtext,
    statusno bigint,
    dc_meeting_date date,
    dc_meeting int,
    dc_meeting_fee BIGINT,
    constraint scholar_id_pk primary key (scholar_id),
    constraint gno_fk foreign key (gno) references guide(gno),
    constraint statusno_fk foreign key (statusno) references status_(statusno)
);



/* Views */

create view department_table_view as
SELECT dname, dtype FROM
department;



create view guide_table_view as 
SELECT guide.guide_name, department.dname FROM
guide, department WHERE guide.dno = department.dno;

create view details_table_view as 
SELECT details.scholar_id, department.dname, guide.guide_name, details.guide_role, details.scholar_name, details.gender, details.regno, details.dob,
details.timing, details.caste, details.subcaste, details.religion, details.email, details.address, details.commencement_date, 
details.join_date, details.last_fee_date, details.total_center_fees, details.annual_fee, details.labfees, details.fees_paid, details.no_due_date,
details.viva_date, details.thesis_title , status_.current_status, details.dc_meeting_date, details.dc_meeting, details.dc_meeting_fee
FROM guide, status_, details, department where guide.gno = details.gno and status_.statusno = details.statusno and guide.dno = department.dno;


