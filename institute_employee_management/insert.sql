INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (101,'Jagdeep','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (102,'Akash','ME',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (103,'Ankit','EE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (104,'Gaurav','ME',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (105,'Rohan','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (106,'Azhar','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (107,'Arman Malik','ME',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (108,'Gaurav','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (109,'Piyush','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (110,'Raghav','ME',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (111,'Ravneesh','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (112,'Vimal','ME',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (113,'Vimlesh','CSE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (114,'Mohit','EE',3,0);

INSERT INTO FACULTY(faculty_id,employee_name,department,available_leaves,leaves_from_next_year)
values (115,'Rehan Khan','EE',3,0);

select hod.faculty_id,employee_name,department
from faculty,hod
where hod.faculty_id=faculty.faculty_id;



INSERT INTO HOD(hod_id,faculty_id,department,appointed_on,appointed_to)
values (201,101,'CSE','05/01/19','04/30/20');

INSERT INTO HOD(hod_id,faculty_id,department,appointed_on,appointed_to)
values (202,104,'ME','05/01/19','04/30/20');


INSERT INTO HOD(hod_id,faculty_id,department,appointed_on,appointed_to)
values (203,103,'EE','05/01/19','04/30/20');



select employee_name,post,appointed_on,appointed_to
from faculty,cross_faculty
where cross_faculty.faculty_id=faculty.faculty_id;


INSERT INTO CROSS_FACULTY(cross_id,faculty_id,post,appointed_on,appointed_to)
VALUES (301,107,'DEAN FACULTY AFFAIRS','05/01/17','04/30/20');



INSERT INTO CROSS_FACULTY(cross_id,faculty_id,post,appointed_on,appointed_to)
VALUES (302,108,'DEAN RESEARCH','05/01/17','04/30/20');



INSERT INTO CROSS_FACULTY(cross_id,faculty_id,post,appointed_on,appointed_to)
VALUES (303,109,'DEAN ACADEMIC AFFIARS','05/01/17','04/30/20');


INSERT INTO CROSS_FACULTY(cross_id,faculty_id,post,appointed_on,appointed_to)
VALUES (304,110,'DEAN STUDENT AFFAIRS','05/01/17','04/30/20');



INSERT INTO CROSS_FACULTY(cross_id,faculty_id,post,appointed_on,appointed_to)
VALUES (305,115,'DIRECTOR','05/01/17','04/30/20');



INSERT INTO route(r_no,stage1,stage2,valid_bit,max_steps) 
values(1,'HOD',null,1,1);

INSERT INTO route(r_no,stage1,stage2,valid_bit,max_steps) 
values(2,'HOD','DEAN',0,2);

INSERT INTO route(r_no,stage1,stage2,valid_bit,max_steps) 
values(3,'DEAN',null,0,1);

INSERT INTO route(r_no,stage1,stage2,valid_bit,max_steps) 
values(4,'DEAN','HOD',0,2);

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (101,'pass');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (102,'pass');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (103,'pass');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (104,'pass');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (105,'pass');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (106,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (107,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (108,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (109,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (110,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (111,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (112,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (113,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (114,'pass1');

INSERT INTO FACULTY_LOGIN(faculty_id,pass)
values (115,'pass1');



INSERT INTO CROSS_LOGIN(cross_id,pass)
VALUES (301,'pass');

INSERT INTO CROSS_LOGIN(cross_id,pass)
VALUES (302,'pass');


INSERT INTO CROSS_LOGIN(cross_id,pass)
VALUES (303,'pass1');

INSERT INTO CROSS_LOGIN(cross_id,pass)
VALUES (304,'pass1');


INSERT INTO CROSS_LOGIN(cross_id,pass)
VALUES (305,'pass1');




INSERT INTO admin_login(user_id,pass) values (999,'adminpass');


INSERT INTO HOD_LOGIN(hod_id,pass)
VALUES (201,'pass');

INSERT INTO HOD_LOGIN(hod_id,pass)
VALUES (202,'pass');


INSERT INTO HOD_LOGIN(hod_id,pass)
VALUES (203,'pass');

