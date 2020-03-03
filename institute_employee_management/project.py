from flask import Flask, redirect, url_for, request
from flask import render_template
import psycopg2
import pymongo



connection = pymongo.MongoClient('localhost',27017)
database = connection['EXAMPLE2']
collection=database['new_col']

app = Flask(__name__)
conn=psycopg2.connect(database="postgres",user="postgres",password="pass",host="127.0.0.1",port="5432")
cur1 = conn.cursor()
print("opened database")

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/profilelist')
def profiles():
    cur1.execute("SELECT faculty_id,employee_name,department FROM faculty;" )
    data= cur1.fetchall()
    return render_template("profilelist.html",data=data)


@app.route('/view_profile',methods=['GET', 'POST'])
def view_portal():
    id_login=request.form['faculty_id']
    result=collection.find(  { "id" : id_login   })
    if result.count()==0:
        return "*****     Profile Do Not Exist       *****"    
    for x in result:
        text=x['data']
        info=x['personal_info']
        ach=x['achievements']
    request.args.get('data',text)
    request.args.get('personal_info',info)
    request.args.get('achievements',ach)
    return render_template('view_profile.html',text=text,info=info,ach=ach)

@app.route('/pb_portal/<login_id>', methods=['GET', 'POST'])
def portal(login_id):
    #id=11
    result=collection.find(  { "id" : login_id   })
    if result.count()!=0:
    
        for x in result:
            text=x['data']
            info=x['personal_info']
            ach=x['achievements']
            #print(text,info,ach)
    else:        
        #print("#############################################")
        collection.insert_one({"id":login_id , "data":" ","personal_info":" ","achievements":" "})
        result=collection.find(  { "id" : login_id })
        for x in result:
            text=x['data']
            info=x['personal_info']
            ach=x['achievements']
    
    request.args.get('data',text)
    request.args.get('personal_info',info)
    request.args.get('achievements',ach)
    #print("%%%%%%%%%%%%%%%%%%%%")
    
    #print("###################3")
    if request.method == "POST":
        print("&&&&&&&")
        #if 'setInfo1' in request.form:
        updated1 = request.form['personal_info']
        #if 'setInfo2' in request.form:
        updated2= request.form['data']
        #if 'setInfo' in request.form:
        updated3 = request.form['achievements']
        collection.update_one({"id":login_id},{"$set": {"personal_info":updated1,"data":updated2,"achievements":updated3}})
        return render_template("pb_portal.html", msg = "Updated ",user=login_id,data_to_edit1=updated1,data_to_edit2=updated2,data_to_edit3=updated3) 
    return render_template("pb_portal.html",data_to_edit1=info,data_to_edit2=text,data_to_edit3=ach,user=login_id)







cur1.execute("SELECT r_no FROM route where valid_bit=1;")
route = cur1.fetchone()
route=route[0]


cur1.execute("SELECT max_steps FROM route where valid_bit=1;")
max_steps = cur1.fetchone()
max_steps = max_steps[0]


cur1.execute("SELECT max_annual_leaves FROM rules;")
max_leaves = cur1.fetchone()[0]
max_leaves = str(max_leaves)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':  
        choice = request.form['choice']
        username1=request.form['username'] 
        password1=request.form['password']
        print(choice,username1,password1)
        user= username1
        #query=""
        if choice == '1':
            query="SELECT faculty_login.faculty_id from faculty_login  WHERE faculty_login.faculty_id ="+username1+ "and faculty_login.pass ='"+password1+"';"
            to = 'faculty_home'
        if choice == '2':
            query="SELECT HOD_login.HOD_id from HOD_login  WHERE HOD_login.HOD_id ="+username1+ "and HOD_login.pass ='"+password1+"';"
            to = 'hod_home'
        if choice == '3':
            query="SELECT Cross_login.Cross_id from Cross_login  WHERE cross_login.CROSS_id ="+username1+ "and CROSS_login.pass ='"+password1+"';"    
            q="select post from cross_faculty where cross_id = "+user+" ; "
            cur.execute(q)
            post =cur.fetchone()
            post = ''.join(post)
            if post == 'DIRECTOR':
                to = 'director_home'
            elif post == 'DEAN FACULTY AFFAIRS' :
                to = 'dean_home' 
            else :
                to = 'cross_home'
        if choice == '4':
            query="SELECT admin_login.user_id from admin_login  WHERE admin_login.user_id ="+username1+ "and admin_login.pass ='"+password1+"';" 
            to = 'admin_home'
        cur.execute(query)
        record=cur.fetchall()
        print(record)
        if(len(record)!=0):
            print("GDFG")
            return redirect(url_for(to,login_id=user))
        else:
            error='WRONG DETAILS'
    return render_template('login.html',error=error)


cur = conn.cursor()
@app.route('/faculty_home/<login_id>')
def faculty_home(login_id):
   cur1.execute("SELECT employee_name,available_leaves,leaves_from_next_year FROM faculty where faculty.faculty_id= "+login_id+";")
   a = cur1.fetchone()
   (name,available_leaves,borrowed) =a
   return render_template("faculty_home.html",message1="Welcome :",message2=name,user=login_id,available_leaves=available_leaves,borrowed=borrowed)


@app.route('/adminhome/<login_id>')
def admin_home(login_id):
    return render_template('admin_home.html')

@app.route('/add')
def open_template():
    return render_template('add_faculty.html')


@app.route('/addfaculty',methods=['GET', 'POST'])
def add_faculty():
    if request.method == 'POST':
        faculty_id= request.form['faculty_id']
        name  = request.form['name']
        branch = request.form['branch'] 
        cur1.execute("select faculty_id from faculty where faculty_id ="+faculty_id+";")
        x = cur1.fetchone()
        if x is not None:         
             return " ***** Provided id exists *****"
        else :
            query = "INSERT into faculty(faculty_id,employee_name,department,available_leaves,leaves_from_next_year) VALUES ("+faculty_id+",'"+name+"', '"+branch+"' ,"+max_leaves+",0);"
            cur1.execute(query)
            conn.commit()
            return "Faculty added"


@app.route('/remove')
def rm():
    return render_template('remove_faculty.html')


@app.route('/removefaculty',methods=['GET', 'POST'])
def rem_faculty():
    if request.method == 'POST':
        faculty_id= request.form['faculty_id']
        cur1.execute("select faculty_id from faculty where faculty_id ="+faculty_id+";")
        x = cur1.fetchone()
        if x is not None:         

            q = "DELETE from faculty_login where faculty_id="+faculty_id+";"
            cur1.execute(q)
            query = "DELETE from faculty where faculty_id="+faculty_id+";"
            cur1.execute(query)
            conn.commit()
            return " ***** Faculty Removed *****"
        else :
            return "********* Provided ID doesn't match any present appointment  *********** "

@app.route('/assign_hod')
def open_hod():
    return render_template('assign_hod.html')


@app.route('/assign_cross')
def open_cross():
    return render_template('assign_cross.html')

@app.route('/insert_hod_data',methods=['GET', 'POST'])
def hod_data():
    if request.method == 'POST':
        faculty_id= request.form['faculty_id']
        branch = request.form['branch'] 
        from_=request.form['from']
        to_ = request.form['to']

        cur1.execute("select faculty_id from hod where hod.faculty_id ="+faculty_id+" and hod.department='"+branch+"';")
        x = cur1.fetchone()
        if x is not None:         
            return "******** PROVIDED ID might be existing already as HOD    *********"
             
        else :
            query = "UPDATE HOD SET faculty_id="+faculty_id+" where department='"+branch+"' ;"
            cur1.execute(query)
            conn.commit()
            query = "UPDATE HOD SET appointed_on='"+from_+"' where department='"+branch+"';"
            cur1.execute(query)
            conn.commit()
            query = "UPDATE HOD SET appointed_to='"+to_+"' where department='"+branch+"';"
            cur1.execute(query)
            conn.commit()
            return "HOD Added"

@app.route('/insert_cross_data',methods=['GET', 'POST'])
def cross_data():
    if request.method == 'POST':
        faculty_id= request.form['faculty_id']
        post = request.form['post'] 
        from_=request.form['from']
        to_ = request.form['to']

        cur1.execute("select faculty_id from cross_faculty where cross_faculty.faculty_id ="+faculty_id+" and cross_faculty.post='"+post+"';")
        x = cur1.fetchone()
        if x is not None:         
            return "******** PROVIDED ID might be existing already as an member to cross_faculty    *********"
             
        else :
            
            query = "UPDATE cross_faculty SET faculty_id="+faculty_id+" where post='"+post+"' ;"
            cur1.execute(query)
            conn.commit()
            query = "UPDATE cross_faculty SET appointed_on='"+from_+"' where post='"+post+"';"
            cur1.execute(query)
            conn.commit()
            query = "UPDATE cross_faculty SET appointed_to='"+to_+"' where post='"+post+"';"
            cur1.execute(query)
            conn.commit()
            return "****************   Changes Done !  ************"

@app.route('/route')
def r():
    cur1.execute("SELECT r_no,stage1,stage2 FROM route ;" )
    data= cur1.fetchall()
    return render_template("select_route.html",data=data)
    
@app.route('/selectroute',methods=['GET', 'POST'])
def select_route():
    if request.method == 'POST':
        route= request.form['route']
        cur1.callproc('change_route',[route])
        conn.commit()
        return "Route selected"

@app.route('/rules')
def rules():
     return render_template('change_rules.html')


@app.route('/changerules',methods=['GET', 'POST'])
def changerules():
    if request.method == 'POST':
        max_leaves= request.form['max_leaves']
        max_borrow= request.form['max_borrow']
        cur.execute("UPDATE rules SET max_borrow_limit= "+max_borrow+";")
        conn.commit()
        cur.execute("UPDATE rules SET max_annual_leaves= "+max_leaves+";")
        conn.commit()
        return "******************  Changes Applied   *******************"


@app.route('/hod_home/<login_id>')
def hod_home(login_id):
   cur1.execute("SELECT employee_name,available_leaves,leaves_from_next_year FROM hod,faculty where hod.hod_id= "+login_id+" and hod.faculty_id=faculty.faculty_id;")
   a = cur1.fetchone()
   (name,available_leaves,borrowed) =a
   return render_template("hod_home.html",message1="hello",message2=name,user=login_id,available_leaves=available_leaves,borrowed=borrowed)


@app.route('/facultydean/<login_id>')
def dean_home(login_id):
   return render_template("dean_home.html",message1="hello",message2=login_id,user=login_id)


@app.route('/crosshome/<login_id>')
def cross_home(login_id):
   return render_template("cross_home.html",message1="hello",message2=login_id,user=login_id)


@app.route('/director_home/<login_id>')
def director_home(login_id):
   return render_template("director_home.html",message1="hello",message2="Director",user=login_id)


@app.route('/hoddesk/<login_id>')
def hod_desk(login_id):

    cur1.execute("SELECT faculty.department FROM hod,faculty where faculty.faculty_id=hod.faculty_id and hod.hod_id="+login_id+";")
    dept1 = cur1.fetchone()
    dept= ''.join(dept1)
    print(dept)
    cur.execute("SELECT * FROM Applications,hod_desk,Faculty where hod_desk.application_number=applications.application_number and faculty.faculty_id = applications.faculty_id and faculty.department='"+dept+"'")
    data = cur.fetchall()
    return render_template("hod_desk.html",data=data)


@app.route('/crossdesk/<login_id>')
def cross_desk(login_id):
    cur1.execute("SELECT * FROM Applications,cross_desk where cross_desk.application_number=applications.application_number;" )
    data= cur1.fetchall()
    return render_template("cross_desk.html",data=data)


@app.route('/directordesk/<login_id>')
def director_desk(login_id):
    cur1.execute("SELECT * FROM Applications,director_desk where director_desk.application_number=applications.application_number;" )
    data= cur1.fetchall()
    return render_template("director_desk.html",data=data)

@app.route('/status/<login_id>')
def status(login_id):
  cur1.execute("select approvals from applications where faculty_id ="+login_id+";")
  x = cur1.fetchone()
  if x is not None:
      stage = x[0]
      if stage!=0:
         no=str(route)
         if stage == 1 :
          cur1.execute("select stage1 from route where r_no = "+no+";")
         else :
          cur1.execute("select stage2 from route where r_no = "+no+";")
          last_stage = cur1.fetchone()
          last_stage= ''.join(last_stage)
      else :
       last_stage = "--FIRST STAGE,NOT YET RESPONDED --"
      print(last_stage)
      return render_template('status.html',msg1 = last_stage)
  else :
      return "#******  LAST APPLICATION WAS PROCESSED CHECK YOUR MESSAGES   ******#"
  

@app.route('/inbox/<login_id>')
def msgs(login_id):
   cur1.execute("SELECT application_number,by_,comment  FROM comments where applicant_id ="+login_id+";")
   data = cur1.fetchall()
   return render_template("msg.html",data=data)



@app.route('/redirect/<login_id>')
def redirect_(login_id):
    cur1.execute("SELECT for_days,starting_date,type_ FROM redirected,applications where applications.application_number=redirected.application_no and redirected.applicant_id = "+login_id+";" )
    data= cur1.fetchall()
    cur1.execute("Select application_no from redirected where applicant_id="+login_id+";")
    found = cur1.fetchone()
    if found is not None:
        return render_template("redirect.html",data=data,user=login_id)
    else :
        return "************   No redirected application   *************"


@app.route('/resubmit/<login_id>',methods=['GET', 'POST'])
def resubmit(login_id):
      if request.method == 'POST':
        date  = request.form['date']
        days  = request.form['number']
        type_ = request.form['type']     

        cur1.callproc('check_eligibility',[login_id,days])
        x = cur1.fetchone()[0]
        if x :
          cur=conn.cursor()
          cur.execute("UPDATE APPLICATIONS SET starting_date='"+date+"' where applications.faculty_id="+login_id+";")
          cur.execute("UPDATE APPLICATIONS SET for_days= "+days+" where applications.faculty_id="+login_id+";")
          cur.execute("UPDATE APPLICATIONS SET type_='"+type_+"' where applications.faculty_id="+login_id+";")
          conn.commit()
          
          cur.execute("select application_no from redirected where applicant_id = "+login_id+" ")
          appl = cur.fetchone()[0]
          cdc=str(appl)

          s="select by_ from redirected where applicant_id = "+login_id+" ; "
          cur.execute(s)
          act_by =cur.fetchone()
          act_by = ''.join(act_by)
          if act_by == 'HOD':
               cur.execute("insert into hod_desk(application_number) values("+cdc+")")
          elif act_by == 'DEAN':
               cur.execute("insert into cross_desk(application_number) values("+cdc+")") 
          conn.commit()
          cur.execute("DELETE FROM redirected where applicant_id="+login_id+";")
          conn.commit()
          return "Resubmitted"
        else :
           return "Number of days out of bound w.r.t maximum borrowing allowed"
  

@app.route('/form/<login_id>')
def form(login_id):
    return render_template("apply.html",user=login_id)


@app.route('/hodform/<login_id>')
def hod_form(login_id):
    return render_template("hod_apply.html",user=login_id)

@app.route('/crossform/<login_id>')
def cross_form(login_id):
    return render_template("cross_apply.html",user=login_id)

@app.route('/apply/<login_id>',methods=['GET', 'POST'])
def apply(login_id):
     if request.method == 'POST':
         date  = request.form['date']
         days  = request.form['number']
         type_ = request.form['type']     
         
         cur1.callproc('check_eligibility',[login_id,days])
         x = cur1.fetchone()[0]
         if x :
             cur=conn.cursor()
             cur.execute("select application_number from applications where faculty_id = "+login_id+" ;")
             d=cur.fetchone()
             if d is not None :
                return "You already submitted one application"
             else :
                query = "INSERT INTO APPLICATIONS(faculty_id,starting_date,for_days,type_,approvals) VALUES ("+login_id+",'"+date+"', "+days+" ,'"+type_+"',0);"
                cur.execute(query)
                cur.execute("select application_number from applications where faculty_id = "+login_id+"; ")
                application_no = cur.fetchone()
                application_no2 = application_no[0]
                cdc=str(application_no2)
                if (route <= 2):
                    cur.execute("insert into hod_desk(application_number) values("+cdc+")")
                else:
                    cur.execute("insert into cross_desk(application_number) values("+cdc+")")
             conn.commit()
             return "************  APPLICATION APPLIED   ****************" 
         else :
            return "Number of days out of bound w.r.t maximum borrowing allowed"
     else:
        return redirect(url_for('faculty_home')) 



@app.route('/hod_apply/<login_id>',methods=['GET', 'POST'])
def hod_apply(login_id):
     if request.method == 'POST':
         date  = request.form['date']
         days  = request.form['number']
         type_ = request.form['type']     
          
         cur1.execute(" SELECT faculty_id from hod where hod_id = "+login_id+" ;")
         f = cur1.fetchone()[0]
         print("hellllllllllllllllllllllllllllllllllllldlfldgf##################################3")
         print(f)
         cur1.callproc('check_eligibility',[f,days])
         x = cur1.fetchone()[0]
         if x :
          cur=conn.cursor()
          query = "INSERT INTO APPLICATIONS(faculty_id,starting_date,for_days,type_,approvals) VALUES ("+login_id+",'"+date+"', "+days+" ,'"+type_+"',0);"
          cur.execute(query)
          cur.execute("select application_number from applications where faculty_id = "+login_id+" ")
          application_no = cur.fetchone()
          application_no2 = application_no[0]
          cdc=str(application_no2)
          cur.execute("insert into director_desk(application_number) values("+cdc+")")
          conn.commit()

          return "************  APPLICATION APPLIED   ****************"  
         else :
           return "Number of days out of bound w.r.t maximum borrowing allowed"
     else:
        return redirect(url_for('hod_home')) 
         


@app.route('/cross_apply/<login_id>',methods=['GET', 'POST'])
def cross_apply(login_id):
     if request.method == 'POST':
         date  = request.form['date']
         days  = request.form['number']
         type_ = request.form['type']     
          
         cur1.execute(" SELECT faculty_id from CROSS_FACULTY where cross_id = "+login_id+" ;")
         f = cur1.fetchone()[0]
         cur1.callproc('check_eligibility',[f,days])
         x = cur1.fetchone()[0]
         if x :
          cur=conn.cursor()
          query = "INSERT INTO APPLICATIONS(faculty_id,starting_date,for_days,type_,approvals) VALUES ("+login_id+",'"+date+"', "+days+" ,'"+type_+"',0);"
          cur.execute(query)
          cur.execute("select application_number from applications where faculty_id = "+login_id+" ")
          application_no = cur.fetchone()
          application_no2 = application_no[0]
          cdc=str(application_no2)
          cur.execute("insert into director_desk(application_number) values("+cdc+")")

          conn.commit()
          return "************  APPLICATION APPLIED   ****************" 
         else :
           return "Number of days out of bound w.r.t maximum borrowing allowed"
     else:
        return redirect(url_for('cross_home')) 
         

@app.route('/hod_response',methods=['GET','POST']) 
def hod_response():
    if request.method == 'POST':
        application_no  = request.form['application_no']
        response = request.form['response']
        comment = request.form['comment']

        
        query="SELECT faculty_id from applications where applications.application_number="+application_no+";"
        cur1.execute(query)
        y=cur1.fetchone()[0]
        applicant = str(y)
        
        
        query="SELECT for_days from applications where applications.application_number="+application_no+";"
        cur1.execute(query)
        z=cur1.fetchone()[0]
        days = str(z)

        if response == 'Approved':
            
            query="UPDATE APPLICATIONS SET approvals = (approvals + 1) where applications.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            query="SELECT approvals from applications where applications.application_number="+application_no+";"
            cur1.execute(query)
            app=cur1.fetchone()
            approvals=app[0]
            
         
            if approvals == max_steps:

               query="INSERT INTO ARCHIEVE(application_number,applicant_id,status_,by_) values ("+application_no+","+applicant+",'approved','HOD')"
               cur1.execute(query)
               conn.commit()
               
               query="DELETE FROM HOD_DESK where hod_desk.application_number="+application_no+"; "
               cur1.execute(query)
               conn.commit()

               query="DELETE FROM applications where application_number="+application_no+"; "
               cur1.execute(query)
               conn.commit()
               
               #adding comment 
               query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'HOD','"+comment+"');"
               cur1.execute(query)
               conn.commit()

               cur1.callproc('update_availability',[applicant,days])
               conn.commit()

               return "Granted Approval"
            else:

               query="INSERT INTO CROSS_DESK(application_number) values ("+application_no+"); "
               cur1.execute(query)
               conn.commit()
               query="DELETE FROM HOD_DESK where hod_desk.application_number="+application_no+"; "
               cur1.execute(query)
               
               #adding comment 
               query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'HOD','"+comment+"'); "
               cur1.execute(query)
              
               conn.commit()
               return"Forwarded"
        
        elif response == 'Redirect':
            query="INSERT INTO redirected(applicant_id,application_no,by_) values ("+applicant+","+application_no+",'HOD'); "
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM HOD_DESK where hod_desk.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            #adding comment 
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'HOD','"+comment+"'); "
            cur1.execute(query)
            conn.commit()

            #adding comment 
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'HOD','Info: Application Redirected'); "
            cur1.execute(query)
            conn.commit()

            return "redirected"

        else:
            query="INSERT INTO ARCHIEVE(application_number,applicant_id,status_,by_) values ("+application_no+","+applicant+",'rejected','HOD')"
            cur1.execute(query)
            conn.commit()
            
            query="DELETE FROM HOD_DESK where hod_desk.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            
            query="DELETE FROM applications where application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            #adding comment 
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'HOD','"+comment+"'); "
            cur1.execute(query)
            conn.commit()

            
            return "Rejected an application"

   
@app.route('/cross_response',methods=['GET','POST']) 
def cross_response():
    if request.method == 'POST':
        application_no  = request.form['application_no']
        response = request.form['response']
        comment = request.form['comment']
    
        
        query="SELECT faculty_id from applications where applications.application_number="+application_no+";"
        cur1.execute(query)
        y=cur1.fetchone()[0]
        applicant = str(y)
         
        
        query="SELECT for_days from applications where applications.application_number="+application_no+";"
        cur1.execute(query)
        z=cur1.fetchone()[0]
        days = str(z)

        if response == 'Approved':
            query="UPDATE APPLICATIONS SET approvals = (approvals + 1) where applications.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()
            query="SELECT approvals from applications where applications.application_number="+application_no+";"
            cur1.execute(query)
            app=cur1.fetchone()
            approvals=app[0]


            if approvals == max_steps:

               query="INSERT INTO ARCHIEVE(application_number,applicant_id,status_,by_) values ("+application_no+","+applicant+",'approved','DEAN')"
               cur1.execute(query)
               conn.commit()

               query="DELETE FROM CROSS_DESK where cross_desk.application_number="+application_no+"; "
               cur1.execute(query)
               
               query="DELETE FROM applications where application_number="+application_no+"; "
               cur1.execute(query)
               conn.commit()

                #insert comment
               query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DEAN','"+comment+"'); "
               cur1.execute(query)
               conn.commit()
               
               cur1.callproc('update_availability',[applicant,days])
               conn.commit()

               return "approved"
            else:
               query="INSERT INTO HOD_DESK(application_number) values ("+application_no+"); "
               cur1.execute(query)
               conn.commit()
               query="DELETE FROM CROSS_DESK where cross_desk.application_number="+application_no+"; "
               cur1.execute(query)
               
                #insert comment
               query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DEAN','"+comment+"'); "
               cur1.execute(query)

               conn.commit()
               return"forwarded"


        elif response == 'Redirect':
            query="INSERT INTO redirected(applicant_id,application_no,by_) values ("+applicant+","+application_no+",'DEAN'); "
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM CROSS_DESK where cross_desk.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            #adding comment 
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DEAN','"+comment+"'); "
            cur1.execute(query)
            conn.commit()

            #adding comment 
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DEAN','Info: Application Redirected'); "
            cur1.execute(query)
            conn.commit()

            return "redirected"
          
        else:
             
            query="INSERT INTO ARCHIEVE(application_number,applicant_id,status_,by_) values ("+application_no+","+applicant+",'rejected','DEAN')"
            cur1.execute(query)
            conn.commit()


            #insert comment
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DEAN','"+comment+"'); "
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM CROSS_DESK where cross_desk.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM applications where application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()
           
            return "rejected"
    


 
@app.route('/director_response',methods=['GET','POST']) 
def director_response():
    if request.method == 'POST':
        application_no  = request.form['application_no']
        response = request.form['response']
        comment = request.form['comment']
    
        
        query="SELECT faculty_id from applications where applications.application_number="+application_no+";"
        cur1.execute(query)
        y=cur1.fetchone()[0]
        applicant = str(y)
         
        
        query="SELECT for_days from applications where applications.application_number="+application_no+";"
        cur1.execute(query)
        z=cur1.fetchone()[0]
        days = str(z)

        if response == 'Approved':
            query="UPDATE APPLICATIONS SET approvals = (approvals + 1) where applications.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            query="INSERT INTO ARCHIEVE(application_number,applicant_id,status_,by_) values ("+application_no+","+applicant+",'approved','DIRECTOR')"
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM director_desk where director_desk.application_number="+application_no+"; "
            cur1.execute(query)
               
            query="DELETE FROM applications where application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            #insert comment
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DIRECTOR','"+comment+"'); "
            cur1.execute(query)
            conn.commit()
               
            cur1.callproc('update_availability',[applicant,days])
            conn.commit()

            return "***********       you approved an application    ************"
            
        else:
             
            query="INSERT INTO ARCHIEVE(application_number,applicant_id,status_,by_) values ("+application_no+","+applicant+",'rejected','DIRECTOR')"
            cur1.execute(query)
            conn.commit()


            #insert comment
            query="INSERT INTO COMMENTS(application_number,applicant_id,by_,comment) values ("+application_no+","+applicant+",'DIRECTOR','"+comment+"'); "
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM director_DESK where director_desk.application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()

            query="DELETE FROM applications where application_number="+application_no+"; "
            cur1.execute(query)
            conn.commit()
           
            return "*************   Rejected    **************"
    





if __name__ == '__main__':
   app.run(debug = True)
