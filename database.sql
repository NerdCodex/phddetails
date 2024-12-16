use phddetails;

/* Department table */

create table department(
	dno bigint auto_increment,
    dname varchar(50),
    dtype varchar(20),
    labincluded boolean,
    annual_labfees bigint,
    labfees_year bigint,
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
    dno bigint,
    gno bigint,
    guide_role varchar(10),
    scholar_name varchar(100),
    gender varchar(10),
    regno varchar(100),
    dob date,
    timing varchar(10),
    caste varchar(10),
    subcaste varchar(100),
    religion varchar(100),
    email varchar(100),
    phno varchar(15),
    optionalphno varchar(15),
    address varchar(100),
    commencement_date date,
    join_date date,
    annual_fee BIGINT,
    
    total_tution_fees BIGINT,
    total_lab_fees BIGINT,
    total_center_fees BIGINT,
    
    last_fee_date date,
    
    tution_fees_paid BIGINT,
    labfees_paid bigint,
    tution_fees_unpaid BIGINT,
    labfees_unpaid BIGINT,
    total_fees_unpaid BIGINT,
    no_due_date date,
    viva_date date,
    thesis_title mediumtext,
    statusno bigint,
    first_dc_meet date,
    first_dc_fee bigint,
    second_dc_meet date,
    second_dc_fee bigint,
	third_dc_meet date,
    third_dc_fee bigint,
    constraint scholar_id_pk primary key (scholar_id),
    constraint dno_pk foreign key (dno) references department(dno),
    constraint gno_fk foreign key (gno) references guide(gno),
    constraint statusno_fk foreign key (statusno) references status_(statusno)
);

drop table details;

/* Functions */

-- Compare Dates

CREATE DEFINER=`root`@`localhost` FUNCTION `compare_dates`(day INT, month INT) RETURNS tinyint(1)
    DETERMINISTIC
BEGIN
    DECLARE current_day INT;
    DECLARE current_month INT;

    -- Get today's day and month from CURDATE()
    SET current_day = DAY(CURDATE());
    SET current_month = MONTH(CURDATE());

    -- Compare the given date (day, month) with today's date
    RETURN (month > current_month) OR (month = current_month AND day > current_day);
END

-- Labfees
CREATE DEFINER=`root`@`localhost` FUNCTION `total_labfees`(
    enrollment_date DATE, 
    annual_lab_fees BIGINT,
    labfees_year BIGINT
) RETURNS bigint
    DETERMINISTIC
BEGIN
    DECLARE enrollment_year INT;
    DECLARE year_diff INT;
    DECLARE enrollment_day INT;
    DECLARE enrollment_month INT;
    DECLARE total_labfees BIGINT;
    
    -- Extract enrollment year, month, and day
    SET enrollment_year = YEAR(enrollment_date);
    SET enrollment_day = DAY(enrollment_date);
    SET enrollment_month = MONTH(enrollment_date);
    
    -- Calculate the year difference based on current date
    IF enrollment_year <= labfees_year THEN
        IF compare_dates(enrollment_day, enrollment_month) = 1 THEN
            SET year_diff = YEAR(CURDATE()) - labfees_year;
        ELSE
            SET year_diff = YEAR(CURDATE()) - labfees_year + 1;
        END IF;
    ELSE
        IF compare_dates(enrollment_day, enrollment_month) = 1 THEN
            SET year_diff = YEAR(CURDATE()) - enrollment_year;
        ELSE
            SET year_diff = YEAR(CURDATE()) - enrollment_year + 1;
        END IF;
    END IF;

    -- Calculate total lab fees
    SET total_labfees = ABS(year_diff * annual_lab_fees);
    
    RETURN total_labfees;
END

-- Tuition Fees
CREATE DEFINER=`root`@`localhost` FUNCTION `total_tution_fees`(
    enrollment_date DATE, 
    annual_fees BIGINT
) RETURNS bigint
    DETERMINISTIC
BEGIN
    DECLARE enrollment_year INT;
    DECLARE year_diff INT;
    DECLARE enrollment_day INT;
    DECLARE enrollment_month INT;
    DECLARE total_fees BIGINT;
    
    -- Extract enrollment year, month, and day
    SET enrollment_year = YEAR(enrollment_date) - 1;
    SET enrollment_day = DAY(enrollment_date);
    SET enrollment_month = MONTH(enrollment_date);
    
    -- Calculate the difference in years
    SET year_diff = YEAR(CURDATE()) - enrollment_year;
    
    -- Adjust the year difference if current date is before enrollment date in the current year
    IF compare_dates(enrollment_day, enrollment_month) = 1 THEN
        SET year_diff = year_diff - 1;
    END IF;
    
    -- Direct Lab Fees Calculation
    
    -- Calculate Total Fees
    SET total_fees = (annual_fees * year_diff);
    
    RETURN total_fees;
END
