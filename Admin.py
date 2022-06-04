import pymysql.cursors
from datetime import datetime
from Student import Student
from Teacher import Teacher
from Course import Course

class Admin:

    def AdminLogin(self):
        print("************************Admin Login************************")
        success = False

        while(success == False):
            usr = input("Enter Admin Username: ")
            passw = input("Enter Admin Password: ")

            try:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234',
                                             database='cms',
                                             cursorclass=pymysql.cursors.DictCursor)

                cursor = connection.cursor()

                cursor.execute("select * from Credentials")

                array_of_dict_creds = cursor.fetchall()
                type = "admin"

                for i in array_of_dict_creds:

                    if (usr == str(i['Username']) and passw == str(i['Password'])
                            and type == str(i['Type'])):
                        success = True

                if (success == False):
                    print("Error! Invalid Username or Password entered.Try again\n")

                cursor.close()

                connection.close()

            except Exception as ex:
                print("Error! Unable to connect to Database")
                print(ex)

        self.DisplayAdminMenu()
        return True

    def DisplayAdminMenu(self):
        running = True

        while running:
            print("\n")
            print("Enter 1 to Manage Students\n")
            print("Enter 2 to Manage Teachers\n")
            print("Enter 3 to Manage Courses\n")
            print("Enter 4 to Exit\n")

            inp = int(input("Enter Choice: "))

            if inp < 1 or inp > 4:
                print("Invalid input! Must be in range 1-4\n")

            else:
                if inp == 1:
                    self.ManageStudent()

                elif inp == 2:
                    self.ManageTeacher()

                elif inp == 3:
                    self.ManageCourses()
                else:
                    running = False

    def ManageStudent(self):
        running = True

        while running:
            print("\n")
            print("Enter 1 to Add Student\n")
            print("Enter 2 to Update Student\n")
            print("Enter 3 to Delete Student\n")
            print("Enter 4 to View All Students\n")
            print("Enter 5 to Display Outstanding Semester Dues\n")
            print("Enter 6 to Assign Course to Student\n")
            print("Enter 7 to Exit\n")

            inp = int(input("Enter Choice: "))

            if inp < 1 or inp > 7:
                print("Invalid input! Must be in range 1-7\n")

            else:
                if inp == 1:
                    try:
                        connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='1234',
                                                     database='cms',
                                                     cursorclass=pymysql.cursors.DictCursor)

                        cursor = connection.cursor()

                        usr = input("Enter Username for new Student to save in Database: ")
                        passw = input("Enter Password for new Student to save in Database: ")

                        st = "INSERT INTO Credentials (Username,Password,Type) VALUES (%s,%s,%s)"

                        val = (usr,passw,"student")

                        cursor.execute(st, val)

                        connection.commit()

                        cursor.execute("select Id from Credentials WHERE Username = '"+usr+"'")
                        res = cursor.fetchone()

                        stu = Student()
                        nm = input("Enter Name: ")
                        stu.set_name(nm)
                        rno = input("Enter Roll no: ")
                        stu.set_roll_no(rno)
                        bch = input("Enter Batch: ")
                        stu.set_batch(bch)
                        due = input("Enter Semester Dues: ")
                        stu.set_semester_dues(due)
                        cs = input("Enter Current Semester: ")
                        stu.set_current_semester(cs)

                        st2 = "INSERT INTO Student (Name,Rollno,Batch,SemesterDues,CurrentSemester,Cred_Id) " \
                             "VALUES (%s,%s,%s,%s,%s,%s)"

                        val2 = (stu.get_name(),stu.get_roll_no(),stu.get_batch(),stu.get_semester_dues(),
                                stu.get_current_semester(),res['Id'])

                        cursor.execute(st2, val2)

                        connection.commit()

                        connection.rollback()

                        connection.close()

                    except Exception as ex:
                        print("Error! Unable to connect to Database")
                        print(ex)

                elif inp == 2:
                    success = False

                    while (success == False):
                        sid = input("Enter Student ID to update Student: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Student")

                            array_of_dict_studs = cursor.fetchall()

                            for i in array_of_dict_studs:

                                if (sid == str(i['Id'])):
                                    success = True
                                    cursor.execute("select * from Student where Id = '"+sid+"'")
                                    stud = cursor.fetchone()

                                    uName = input("Enter Username if you want to update : ")
                                    passw = input("Enter Password if you want to update : ")
                                    name = input("Enter Name if you want to update : ")
                                    rollno = input("Enter Roll no if you want to update : ")
                                    batch = input("Enter Batch if you want to update : ")
                                    dues = input("Enter Semester dues if you want to update : ")
                                    sem = input("Enter Current Semester if you want to update : ")

                                    if (uName != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Credentials
                                                                SET Username=%s
                                                                WHERE Id =%s
                                                                """, (uName, stud['Cred_Id']))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (passw != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Credentials
                                                                SET Password=%s
                                                                WHERE Id =%s
                                                                """, (passw, stud['Cred_Id']))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (name != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Student
                                                                SET Name=%s
                                                                WHERE Id =%s
                                                                """, (name,sid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (rollno != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Student
                                                                SET Rollno=%s
                                                                WHERE Id =%s
                                                                """, (rollno,sid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (batch != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Student
                                                                SET Batch=%s
                                                                WHERE Id =%s
                                                                """, (batch,sid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (dues != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Student
                                                                SET SemesterDues=%s
                                                                WHERE Id =%s
                                                                """, (dues,sid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (sem != ""):
                                        try:
                                            cursor.execute("""
                                                                UPDATE Student
                                                                SET CurrentSemester=%s
                                                                WHERE Id =%s
                                                                """, (sem,sid))
                                            connection.commit()
                                        except:
                                            connection.rollback()


                            if (success == False):
                                print("Error! Invalid Student ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 3:
                    success = False

                    while (success == False):
                        sid = input("Enter Student ID to delete Student: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Student")

                            array_of_dict_studs = cursor.fetchall()

                            for i in array_of_dict_studs:

                                if (sid == str(i['Id'])):
                                    success = True
                                    cursor.execute("select Cred_Id from Student where Id = '" + sid + "'")
                                    cred_Id = cursor.fetchone()
                                    cursor.execute("delete from Credentials "
                                                   "where Id = '" + str(cred_Id['Cred_Id']) + "'")

                                    connection.commit()

                            if (success == False):
                                print("Error! Invalid Student ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 4:
                    print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format
                          ('ID', 'Name', 'RollNo', 'Batch', 'SemesterDues', 'CurrentSemester'))

                    try:
                        connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='1234',
                                                     database='cms',
                                                     cursorclass=pymysql.cursors.DictCursor)

                        cursor = connection.cursor()

                        cursor.execute("select * from Student")

                        array_of_dict_studs = cursor.fetchall()

                        for i in array_of_dict_studs:
                            print("{:<15} {:<15} {:<15} {:<15} {:<15} {:<15}".format
                                  (str(i['Id']), str(i['Name']),str(i['Rollno']),str(i['Batch']),
                                   str(i['SemesterDues']),str(i['CurrentSemester'])))

                        cursor.close()

                        connection.close()

                    except Exception as ex:
                        print("Error! Unable to connect to Database")
                        print(ex)

                elif inp == 5:
                    success = False

                    while (success == False):
                        sid = input("Enter Student ID to view Outstanding Semester Dues: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Student")

                            array_of_dict_studs = cursor.fetchall()

                            for i in array_of_dict_studs:

                                if (sid == str(i['Id'])):
                                    success = True
                                    cursor.execute("select SemesterDues from Student where Id = '" + sid + "'")
                                    dues = cursor.fetchone()

                                    print("Outstanding Semester Dues: "+str(dues['SemesterDues']))

                            if (success == False):
                                print("Error! Invalid Student ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 6:
                    id_success = False

                    while (id_success == False):
                        sid = input("Enter Student ID to Assign Course to Student: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Student")

                            array_of_dict_studs = cursor.fetchall()

                            for i in array_of_dict_studs:

                                if (sid == str(i['Id'])):
                                    id_success = True

                                    crs_success = False

                                    while (crs_success == False):
                                        cid = input("Enter Course ID to Assign Course to Student: ")
                                        cursor = connection.cursor()

                                        cursor.execute("select * from Course")

                                        array_of_dict_crs = cursor.fetchall()

                                        for i in array_of_dict_crs:

                                            if (cid == str(i['Id'])):
                                                crs_success = True

                                                dt = input("Enter Admission Date: ")

                                                st = "INSERT INTO Enroll (Student_Id,Course_Id,Admission_Date) " \
                                                     "VALUES (%s,%s,%s)"

                                                date_obj = datetime.strptime(dt, '%d/%m/%Y')
                                                val = (sid, cid, date_obj)

                                                cursor.execute(st, val)

                                                connection.commit()

                                        if (crs_success == False):
                                            print("Error! Invalid Course ID entered.Try again\n")

                            if (id_success == False):
                                print("Error! Invalid Student ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)
                else:
                    running = False

    def ManageTeacher(self):
        running = True

        while running:
            print("\n")
            print("Enter 1 to Add Teacher\n")
            print("Enter 2 to Update Teacher\n")
            print("Enter 3 to Delete Teacher\n")
            print("Enter 4 to View All Teachers\n")
            print("Enter 5 to Assign Course to Teacher\n")
            print("Enter 6 to Exit\n")

            inp = int(input("Enter Choice: "))

            if inp < 1 or inp > 6:
                print("Invalid input! Must be in range 1-6\n")

            else:
                if inp == 1:
                    try:
                        connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='1234',
                                                     database='cms',
                                                     cursorclass=pymysql.cursors.DictCursor)

                        cursor = connection.cursor()

                        usr = input("Enter Username for new Teacher to save in Database: ")
                        passw = input("Enter Password for new Teacher to save in Database: ")

                        st = "INSERT INTO Credentials (Username,Password,Type) VALUES (%s,%s,%s)"

                        val = (usr,passw,"teacher")

                        cursor.execute(st, val)

                        connection.commit()

                        cursor.execute("select Id from Credentials WHERE Username = '"+usr+"'")
                        res = cursor.fetchone()

                        tch = Teacher()
                        nm = input("Enter Name: ")
                        tch.set_name(nm)
                        sal = input("Enter Salary: ")
                        tch.set_salary(sal)
                        exp = input("Enter Experience: ")
                        tch.set_experience(exp)

                        st2 = "INSERT INTO Teacher (Name,Salary,Experience,NoOfCoursesAssigned,Cred_Id) " \
                             "VALUES (%s,%s,%s,%s,%s)"

                        val2 = (tch.get_name(),tch.get_salary(),tch.get_experience(),
                                0,res['Id'])

                        cursor.execute(st2, val2)

                        connection.commit()

                        connection.rollback()

                        connection.close()

                    except Exception as ex:
                        print("Error! Unable to connect to Database")
                        print(ex)

                elif inp == 2:
                    success = False

                    while (success == False):
                        tid = input("Enter Teacher ID to update Teacher: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Teacher")

                            array_of_dict_tchs = cursor.fetchall()

                            for i in array_of_dict_tchs:

                                if (tid == str(i['Id'])):
                                    success = True
                                    cursor.execute("select * from Teacher where Id = '" + tid + "'")
                                    tch = cursor.fetchone()

                                    uName = input("Enter Username if you want to update : ")
                                    passw = input("Enter Password if you want to update : ")
                                    name = input("Enter Name if you want to update : ")
                                    sal = input("Enter Salary if you want to update : ")
                                    exp = input("Enter Experience if you want to update : ")
                                    crs = input("Enter No. of Courses Assigned if you want to update : ")

                                    if (uName != ""):
                                        try:
                                            cursor.execute("""
                                                                            UPDATE Credentials
                                                                            SET Username=%s
                                                                            WHERE Id =%s
                                                                            """, (uName, tch['Cred_Id']))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (passw != ""):
                                        try:
                                            cursor.execute("""
                                                                            UPDATE Credentials
                                                                            SET Password=%s
                                                                            WHERE Id =%s
                                                                            """, (passw, tch['Cred_Id']))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (name != ""):
                                        try:
                                            cursor.execute("""
                                                                            UPDATE Teacher
                                                                            SET Name=%s
                                                                            WHERE Id =%s
                                                                            """, (name, tid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (sal != ""):
                                        try:
                                            cursor.execute("""
                                                                            UPDATE Teacher
                                                                            SET Salary=%s
                                                                            WHERE Id =%s
                                                                            """, (sal, tid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (exp != ""):
                                        try:
                                            cursor.execute("""
                                                                             UPDATE Teacher
                                                                             SET Experience=%s
                                                                             WHERE Id =%s
                                                                             """, (exp, tid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (crs != ""):
                                        try:
                                            cursor.execute("""
                                                                            UPDATE Teacher
                                                                            SET NoOfCoursesAssigned=%s
                                                                            WHERE Id =%s
                                                                            """, (crs, tid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                            if (success == False):
                                print("Error! Invalid Teacher ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 3:
                    success = False

                    while (success == False):
                        tid = input("Enter Teacher ID to delete Teacher: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Teacher")

                            array_of_dict_tchs = cursor.fetchall()

                            for i in array_of_dict_tchs:

                                if (tid == str(i['Id'])):
                                    success = True
                                    cursor.execute("""
                                                                            UPDATE Course
                                                                            SET Teacher_Id=%s
                                                                            WHERE Teacher_Id =%s
                                                                            """,(None,tid))
                                    connection.commit()

                                    cursor.execute("select Cred_Id from Teacher where Id = '" + tid + "'")
                                    cred_Id = cursor.fetchone()
                                    cursor.execute("delete from Credentials "
                                                   "where Id = '" + str(cred_Id['Cred_Id']) + "'")

                                    connection.commit()

                            if (success == False):
                                print("Error! Invalid Teacher ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 4:
                    print("{:<15} {:<15} {:<15} {:<15} {:<15}".format('ID', 'Name', 'Salary', 'Experience',
                                                                      'NoOfCoursesAssigned'))
                    try:
                        connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='1234',
                                                     database='cms',
                                                     cursorclass=pymysql.cursors.DictCursor)

                        cursor = connection.cursor()

                        cursor.execute("select * from Teacher")

                        array_of_dict_tchs = cursor.fetchall()

                        for i in array_of_dict_tchs:
                            print("{:<15} {:<15} {:<15} {:<15} {:<15}".format(str(i['Id']), str(i['Name']),
                                                                str(i['Salary']),str(i['Experience']),
                                                                              str(i['NoOfCoursesAssigned'])))
                        cursor.close()

                        connection.close()

                    except Exception as ex:
                        print("Error! Unable to connect to Database")
                        print(ex)

                elif inp == 5:
                    id_success = False

                    while (id_success == False):
                        tid = input("Enter Teacher ID to Assign Course to Teacher: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Teacher")

                            array_of_dict_tchs = cursor.fetchall()

                            for i in array_of_dict_tchs:

                                if (tid == str(i['Id'])):
                                    id_success = True
                                    count = i['NoOfCoursesAssigned']

                                    crs_success = False

                                    while (crs_success == False):
                                        cid = input("Enter Course ID to Assign Course to Teacher: ")
                                        cursor = connection.cursor()

                                        cursor.execute("select * from Course")

                                        array_of_dict_crs = cursor.fetchall()

                                        for i in array_of_dict_crs:

                                            if (cid == str(i['Id'])):
                                                crs_success = True

                                                cursor.execute("""
                                                                            UPDATE Course
                                                                            SET Teacher_Id=%s
                                                                            WHERE Id =%s
                                                                            """,
                                                                            (tid, cid))

                                                connection.commit()

                                                count = count + 1

                                                cursor.execute("""
                                                                            UPDATE Teacher
                                                                            SET NoOfCoursesAssigned=%s
                                                                            WHERE Id =%s
                                                                             """,
                                                                            (count, tid))

                                                connection.commit()

                                        if (crs_success == False):
                                            print("Error! Invalid Course ID entered.Try again\n")

                            if (id_success == False):
                                print("Error! Invalid Student ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)
                else:
                    running = False

    def ManageCourses(self):
        running = True

        while running:
            print("\n")
            print("Enter 1 to Add Courses\n")
            print("Enter 2 to Update Courses\n")
            print("Enter 3 to Delete Courses\n")
            print("Enter 4 to View All Courses\n")
            print("Enter 5 to Exit\n")

            inp = int(input("Enter Choice: "))

            if inp < 1 or inp > 5:
                print("Invalid input! Must be in range 1-5\n")

            else:
                if inp == 1:
                    try:
                        connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='1234',
                                                     database='cms',
                                                     cursorclass=pymysql.cursors.DictCursor)

                        cursor = connection.cursor()

                        course = Course()
                        crs = input("Enter Course Name for new Course to save in Database: ")
                        course.set_course_name(crs)
                        crh = input("Enter Course Credit Hours: ")
                        course.set_credit_hours(crh)

                        st = "INSERT INTO Course (CourseName,CreditHours,Teacher_Id) VALUES (%s,%s,%s)"

                        val = (course.get_course_name(),course.get_credit_hours(),None)

                        cursor.execute(st, val)

                        connection.commit()

                        connection.close()

                    except Exception as ex:
                        print("Error! Unable to connect to Database")
                        print(ex)

                elif inp == 2:
                    success = False

                    while (success == False):
                        cid = input("Enter Course ID to update Course: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Course")

                            array_of_dict_crs = cursor.fetchall()

                            for i in array_of_dict_crs:

                                if (cid == str(i['Id'])):
                                    success = True

                                    name = input("Enter Course Name if you want to update : ")
                                    hrs = input("Enter Credit Hours if you want to update : ")

                                    if (name != ""):
                                        try:
                                            cursor.execute("""
                                                                                    UPDATE Course
                                                                                    SET CourseName=%s
                                                                                    WHERE Id =%s
                                                                                    """,(name, cid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                                    if (hrs != ""):
                                        try:
                                            cursor.execute("""
                                                                                    UPDATE Course
                                                                                    SET CreditHours=%s
                                                                                    WHERE Id =%s
                                                                                    """, (hrs, cid))
                                            connection.commit()
                                        except:
                                            connection.rollback()

                            if (success == False):
                                print("Error! Invalid Course ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 3:
                    success = False

                    while (success == False):
                        cid = input("Enter Course ID to delete Course: ")

                        try:
                            connection = pymysql.connect(host='localhost',
                                                         user='root',
                                                         password='1234',
                                                         database='cms',
                                                         cursorclass=pymysql.cursors.DictCursor)

                            cursor = connection.cursor()

                            cursor.execute("select * from Course")

                            array_of_dict_crs = cursor.fetchall()

                            for i in array_of_dict_crs:

                                if (cid == str(i['Id'])):
                                    success = True

                                    cursor.execute("delete from Course where Id = '" + cid + "'")

                                    connection.commit()

                            if (success == False):
                                print("Error! Invalid Course ID entered.Try again\n")

                            cursor.close()

                            connection.close()

                        except Exception as ex:
                            print("Error! Unable to connect to Database")
                            print(ex)

                elif inp == 4:
                    print("{:<15} {:<15} {:<15} {:<15}".format('ID', 'CourseName', 'CreditHours',
                                                               'AssignedTeacherID'))
                    try:
                        connection = pymysql.connect(host='localhost',
                                                     user='root',
                                                     password='1234',
                                                     database='cms',
                                                     cursorclass=pymysql.cursors.DictCursor)

                        cursor = connection.cursor()

                        cursor.execute("select * from Course")

                        array_of_dict_crs = cursor.fetchall()

                        for i in array_of_dict_crs:
                            print("{:<15} {:<15} {:<15} {:<15}".format(str(i['Id']), str(i['CourseName']),
                                                                str(i['CreditHours']),str(i['Teacher_Id'])))
                        cursor.close()

                        connection.close()

                    except Exception as ex:
                        print("Error! Unable to connect to Database")
                        print(ex)
                else:
                    running = False

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance