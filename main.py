from Student import Student
from Teacher import Teacher
from Admin import Admin
from Course import Course
import pymysql.cursors

stu = Student()
tch = Teacher()
crs = Course()

def cms():
    try:
        connection = pymysql.connect(host='localhost',
                                      user='root',
                                      password='1234',
                                      database='cms',
                                      cursorclass=pymysql.cursors.DictCursor)

        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS Credentials (Id INT(15) AUTO_INCREMENT PRIMARY KEY,"
                       "Username VARCHAR(50) NOT NULL,Password VARCHAR(50) NOT NULL,Type VARCHAR(8) NOT NULL)")

        st = "INSERT IGNORE INTO Credentials (Id, Username, Password,Type) VALUES (%s,%s,%s,%s)"

        val = (1, "admin", "admin", "admin")

        cursor.execute(st, val)

        connection.commit()

        cursor.execute("CREATE TABLE IF NOT EXISTS Student (Id INT(15) AUTO_INCREMENT PRIMARY KEY,"
                       "Name VARCHAR(50) NOT NULL,Rollno VARCHAR(15) NOT NULL,"
                       "Batch VARCHAR(25) NOT NULL,SemesterDues INT(5) NOT NULL,CurrentSemester INT(1) NOT NULL,"
                       "Cred_Id INT(15), CONSTRAINT cred_id_stu_fk FOREIGN KEY (Cred_Id) REFERENCES "
                       "Credentials (Id) ON DELETE CASCADE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS Teacher (Id INT(15) AUTO_INCREMENT PRIMARY KEY,"
                       "Name VARCHAR(50) NOT NULL,Salary INT(7) NOT NULL,"
                       "Experience INT(3) NOT NULL,NoOfCoursesAssigned INT(3) NOT NULL,Cred_Id INT(15),"
                       "CONSTRAINT cred_id_tch_fk FOREIGN KEY (Cred_Id) REFERENCES "
                       "Credentials (Id) ON DELETE CASCADE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS Course (Id INT(15) AUTO_INCREMENT PRIMARY KEY,"
                       "CourseName VARCHAR(50) NOT NULL,CreditHours INT(2) NOT NULL,"
                       "Teacher_Id INT(15),CONSTRAINT teacher_id_crs_fk FOREIGN KEY (Teacher_Id) "
                       "REFERENCES Teacher (Id))")

        cursor.execute("CREATE TABLE IF NOT EXISTS Assignment (Id INT(15) AUTO_INCREMENT PRIMARY KEY,"
                       "Topic VARCHAR(50) NOT NULL,Description VARCHAR(500) NOT NULL,"
                       "Deadline DATE NOT NULL,Course_Id INT(15),"
                       "CONSTRAINT course_id_ass_fk FOREIGN KEY (Course_Id) "
                       "REFERENCES Course (Id) ON DELETE CASCADE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS Assignment_Status (Assignment_Id INT(15) NOT NULL,"
                       "Student_Id INT(15) NOT NULL,Pending INT(1) NOT NULL,"
                       "PRIMARY KEY (Assignment_Id,Student_Id),CONSTRAINT assign_id_ass_fk "
                       "FOREIGN KEY (Assignment_Id) "
                       "REFERENCES Assignment (Id) ON DELETE CASCADE,CONSTRAINT student_id_ass_fk "
                       "FOREIGN KEY (Student_Id) REFERENCES Student (Id) ON DELETE CASCADE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS AttendanceInformation (Student_Id INT(15) NOT NULL,"
                       "Course_Id INT(15) NOT NULL,"
                       "Date DATE NOT NULL,Attendance_Status VARCHAR(1) NOT NULL,"
                       "PRIMARY KEY (Student_Id,Course_Id,Date),"
                       "CONSTRAINT student_id_att_fk FOREIGN KEY (Student_Id) "
                       "REFERENCES Student (Id) ON DELETE CASCADE,"
                       "CONSTRAINT course_id_att_fk FOREIGN KEY (Course_Id)"
                       "REFERENCES Course (Id) ON DELETE CASCADE)")

        cursor.execute("CREATE TABLE IF NOT EXISTS Enroll (Student_Id INT(15) NOT NULL,"
                       "Course_Id INT(15) NOT NULL,"
                       "Admission_Date DATE NOT NULL,"
                       "PRIMARY KEY (Student_Id,Course_Id),"
                       "CONSTRAINT student_id_en_fk FOREIGN KEY (Student_Id) "
                       "REFERENCES Student (Id) ON DELETE CASCADE,"
                       "CONSTRAINT course_id_en_fk FOREIGN KEY (Course_Id)"
                       "REFERENCES Course (Id) ON DELETE CASCADE)")

        connection.rollback()

        cursor.close()

        connection.close()

    except Exception as ex:
        print("Error! Unable to connect to Database")
        print(ex)

    print("************************Course Management System************************")

    running = True

    while running:
        print("\n")
        print("Enter 1 to Login as Student\n")
        print("Enter 2 to Login as Instructor\n")
        print("Enter 3 to Login as Admin\n")
        print("Enter 4 to Exit\n")

        inp = int(input("Enter Choice: "))

        if inp < 1 or inp > 4:
            print("Invalid input! Must be in range 1-4\n")

        else:
            if inp == 1:
                student = Student()
                student.StudentLogin()

            elif inp == 2:
                teacher = Teacher()
                teacher.TeacherLogin()

            elif inp == 3:
                admin = Admin()
                admin.AdminLogin()
            else:
                running = False
                print("Program Terminated\n")

cms()