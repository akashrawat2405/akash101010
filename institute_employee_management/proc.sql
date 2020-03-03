
CREATE OR REPLACE FUNCTION change_route(INT)
RETURNS VOID
LANGUAGE plpgsql    
AS $$
BEGIN

    UPDATE route 
    SET valid_bit = 0;
    
    UPDATE route
    SET valid_bit = 1
    WHERE r_no = $1;
 
END;
$$;



select "change_route"(2); 

CREATE TRIGGER system_msg
 AFTER INSERT
   ON archieve
   FOR EACH ROW
   EXECUTE PROCEDURE system_message_creation();


CREATE FUNCTION system_message_creation()
RETURNS trigger AS
 
$$
BEGIN
    IF NEW.status_ = 'approved'
    THEN
     INSERT INTO comments(application_number,applicant_id,by_,comment) 
     values (NEW.application_number,NEW.applicant_id,NEW.by_,'System Message : Application Approved');
    END IF;
    IF NEW.status_ = 'rejected'
    THEN
     INSERT INTO comments(application_number,applicant_id,by_,comment) 
     values (NEW.application_number,NEW.applicant_id,NEW.by_,'System Message : Application Rejected');
    END IF;
    RETURN NEW;
END;
$$
language plpgsql;



CREATE OR REPLACE FUNCTION update_availability(int,int)
RETURNS VOID
LANGUAGE plpgsql    
AS $$
DECLARE 
      a alias for $1;
      b alias for $2;
      z integer;
BEGIN
      z = (SELECT available_leaves from faculty where faculty_id = a) - b;

      IF z<0
      THEN
      UPDATE faculty set available_leaves = 0 where faculty_id = a ;
      UPDATE faculty set leaves_from_next_year = leaves_from_next_year -z where faculty_id = a ;
      END IF;
      IF z>0
      THEN
      UPDATE faculty set available_leaves = z where faculty_id = a ;
      END IF;
END;
$$;





CREATE OR REPLACE FUNCTION check_eligibility(int,int)
RETURNS boolean
LANGUAGE plpgsql    
AS $$
DECLARE 
      a alias for $1;
      b alias for $2;
      z integer;
      
BEGIN
      
      z = (SELECT available_leaves from faculty where faculty_id = a) +
          ((SELECT max_borrow_limit from rules) - (SELECT leaves_from_next_year from faculty where faculty_id = a )) ;
      z =  z - b;

      IF z<0
      THEN
       return 0;
      END IF;
      IF z>=0
      THEN
       return 1;
      END IF;

END;
$$;





CREATE TRIGGER create_faculty_login
 AFTER INSERT
   ON faculty
   FOR EACH ROW
   EXECUTE PROCEDURE faculty_login_creation();


CREATE FUNCTION faculty_login_creation()
RETURNS trigger AS
 
$$
BEGIN
    INSERT INTO FACULTY_LOGIN(faculty_id,pass) VALUES (NEW.faculty_id,'pass');
    RETURN NEW;
END;
$$
language plpgsql;
