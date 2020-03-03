

CREATE TABLE FACULTY(
faculty_id  INTEGER PRIMARY KEY,
employee_name VARCHAR NOT NULL,
department VARCHAR(50) NOT NULL,
available_leaves INTEGER NOT NULL,
leaves_from_next_year INTEGER NOT NULL
);



CREATE TABLE HOD(
hod_id INTEGER UNIQUE NOT NULL,
faculty_id INTEGER UNIQUE NOT NULL,
department VARCHAR PRIMARY KEY,
appointed_on DATE NOT NULL,
appointed_to DATE NOT NULL,
FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id)
);


CREATE TABLE CROSS_FACULTY(
cross_id INTEGER PRIMARY KEY,
faculty_id INTEGER UNIQUE NOT NULL,
post VARCHAR UNIQUE NOT NULL,
appointed_on DATE NOT NULL,
appointed_to DATE NOT NULL,
FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id)
);


CREATE TABLE FACULTY_LOGIN(
faculty_id INTEGER PRIMARY KEY,
pass VARCHAR NOT NULL,
FOREIGN KEY (faculty_id) REFERENCES FACULTY(faculty_id)
);



CREATE TABLE HOD_LOGIN(
hod_id INTEGER PRIMARY KEY,
pass VARCHAR NOT NULL,
FOREIGN KEY (hod_id) REFERENCES HOD(hod_id)
);


CREATE TABLE CROSS_LOGIN(
cross_id INTEGER PRIMARY KEY,
pass VARCHAR NOT NULL,
FOREIGN KEY (cross_id) REFERENCES CROSS_FACULTY(cross_id)
);

CREATE TABLE APPLICATIONS(
application_number SERIAL UNIQUE NOT NULL,
faculty_id INTEGER NOT NULL,
starting_date DATE NOT NULL,
for_days INTEGER NOT NULL,
type_ VARCHAR NOT NULL,
approvals INTEGER NOT NULL,
PRIMARY KEY(faculty_id)
);

CREATE TABLE ARCHIEVE(
application_number INTEGER PRIMARY KEY,
applicant_id INTEGER NOT NULL,
status_ VARCHAR NOT NULL,
by_ VARCHAR NOT NULL
);

CREATE TABLE route(
r_no integer PRIMARY KEY,
stage1 VARCHAR,
stage2 VARCHAR,
valid_bit integer not null,
max_steps integer not null
);

CREATE TABLE hod_desk(
application_number INTEGER NOT NULL,
FOREIGN KEY (application_number) REFERENCES APPLICATIONS(application_number)
);


CREATE TABLE director_desk(
application_number INTEGER NOT NULL,
FOREIGN KEY (application_number) REFERENCES APPLICATIONS(application_number)
);



CREATE TABLE cross_desk(
application_number INTEGER NOT NULL,
FOREIGN KEY (application_number) REFERENCES APPLICATIONS(application_number)
);


CREATE TABLE COMMENTS(
application_number INTEGER NOT NULL,
applicant_id INTEGER NOT NULL,
by_ VARCHAR NOT NULL,
comment TEXT NOT NULL
);



CREATE TABLE rules(
max_borrow_limit INTEGER NOT NULL,
max_annual_leaves INTEGER NOT NULL
);

CREATE TABLE redirected(
applicant_id INTEGER NOT NULL,
application_no INTEGER NOT NULL,
by_ VARCHAR NOT NULL 
);


CREATE TABLE admin_login(
user_id INTEGER NOT NULL,
pass VARCHAR NOT NULL
);