import pymysql.cursors
from datetime import datetime

class Teacher:
    __Id = None
    __Name = None
    __Salary = None
    __Experience = None
    __NoOfCoursesAssigned = None

    def get_Id(self):
        return self.__Id

    def get_name(self):
        return self.__Name

    def get_salary(self):
        return self.__Salary

    def get_experience(self):
        return self.__Experience

    def get_no_of_courses_assigned(self):
        return self.__NoOfCoursesAssigned

    def set_Id(self,id):
        self.__Id = id

    def set_name(self, nm):
        self.__Name = nm

    def set_salary(self, sal):
        self.__Salary = sal

    def set_experience(self, exp):
        self.__Experience = exp

    def set_no_of_courses_assigned(self, crs):
        self.__NoOfCoursesAssigned = crs

    def TeacherLogin(self):
        print("************************Instructor Login************************")
        success = False

        while (success == False):
            try:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234',
                                             database='cms',
                                             cursorclass=pymysql.cursors.DictCursor)

                cursor = connection.cursor()

                result = cursor.execute("select * from Credentials")

                if (result == 1):
                    print("Unable to proceed! No data for Instructors exit in Database\n")
                    return False

                usr = input("Enter Instructor Username: ")
                passw = input("Enter Instructor Password: ")
                type = "teacher"

                array_of_dict_creds = cursor.fetchall()

                for i in array_of_dict_creds:

                    if (usr == str(i['Username']) and passw == str(i['Password'])
                            and type == str(i['Type'])):

                        success = True
                        cursor.execute("select Id from Credentials where Username = '" + usr + "'")
                        cid = cursor.fetchone()
                        cursor.execute("select Id from Teacher where Cred_Id = '" + str(cid['Id']) + "'")
                        tid = cursor.fetchone()
                        self.__Id = tid['Id']

                if (success == False):
                    print("Error! Invalid Username or Password entered.Try again\n")

                cursor.close()

                connection.close()

            except Exception as ex:
                print("Error! Unable to connect to Database")
                print(ex)

        self.DisplayTeacherMenu()
        return True

    def DisplayTeacherMenu(self):
        running = True

        while running:
            print("\n")
            print("Enter 1 to Mark Attendance\n")
            print("Enter 2 to post assignment\n")
            print("Enter 3 to view Assigned Courses\n")
            print("Enter 4 to Exit\n")

            inp = int(input("Enter Choice: "))

            if inp < 1 or inp > 4:
                print("Invalid input! Must be in range 1-4\n")

            else:
                if inp == 1:
                    self.MarkAttendance()

                elif inp == 2:
                    self.PostAssignment()

                elif inp == 3:
                    self.ViewAssignedCourses()
                else:
                    running = False

    def MarkAttendance(self):

        if self.ViewAssignedCourses():
            success = False

            while (success == False):
                cid = input("Enter Course ID of which you want to mark attendance: ")

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

                        if (cid == str(i['Id']) and self.__Id == i['Teacher_Id']):
                            success = True

                            id_res = cursor.execute("select Student_Id from Enroll where Course_Id "
                                                    "= '" + cid + "'")

                            if id_res == 0:
                                print("No students are enrolled in this course yet!")
                            else:
                                sids = cursor.fetchall()

                                dt = input("Enter Attendance Date: ")

                                print("{:<15} {:<15} {:<15}".format('Rollno', 'Name', 'Attendance Status'))

                                for j in sids:
                                    cursor.execute("select * from Student where "
                                                   "Id = '" + str(j["Student_Id"]) + "'")

                                    studs = cursor.fetchall()

                                    for k in studs:
                                        status = input("{:<15} {:<15}".format(str(k['Rollno']),
                                                        str(k['Name'])))

                                        while status != 'P' and status != 'A':
                                            print("Error! Invalid input. You must enter 'P' or 'A' only")

                                            print("{:<15} {:<15} {:<15}".format('Rollno', 'Name',
                                                    'Attendance Status'))

                                            status = input("{:<15} {:<15}".format(str(k['Rollno']),
                                                            str(k['Name'])))

                                        st = "INSERT INTO AttendanceInformation (Student_Id,Course_Id,Date," \
                                             "Attendance_Status) " \
                                             "VALUES (%s,%s,%s,%s)"

                                        date_obj = datetime.strptime(dt, '%d/%m/%Y')
                                        val = (k['Id'], cid, date_obj, status)

                                        cursor.execute(st, val)

                                        connection.commit()

                    if (success == False):
                        print("Error! Invalid Course ID entered.Try again\n")

                    cursor.close()

                    connection.close()

                except Exception as ex:
                    print("Error! Unable to connect to Database")
                    print(ex)

    def PostAssignment(self):
        if self.ViewAssignedCourses():
            success = False

            while (success == False):
                cid = input("Enter Course ID of which you want to post assignment: ")

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

                        if (cid == str(i['Id']) and self.__Id == i['Teacher_Id']):
                            success = True

                            id_res = cursor.execute("select Student_Id from Enroll where Course_Id "
                                                    "= '" + cid + "'")

                            if id_res == 0:
                                print("No students are enrolled in this course yet!")
                            else:
                                sids = cursor.fetchall()

                                nm = input("Enter Topic Name: ")
                                desc = input("Enter Assignment Description: ")
                                dt = input("Enter Deadline for submission: ")

                                st = "INSERT INTO Assignment (Topic,Description,Deadline,Course_Id) " \
                                     "VALUES (%s,%s,%s,%s)"

                                date_obj = datetime.strptime(dt, '%d/%m/%Y')
                                val = (nm, desc, date_obj,cid)

                                cursor.execute(st, val)

                                connection.commit()

                                cursor.execute("select Id from Assignment where Topic = '"+nm+"' "
                                    "and Description = '"+desc+"'and "
                                        "Deadline = '"+str(date_obj)+"'"
                                            "and Course_Id = '"+cid+"'")

                                assign_id = cursor.fetchone()

                                for j in sids:
                                    st2 = "INSERT INTO Assignment_Status (Assignment_Id,Student_Id,Pending) " \
                                         "VALUES (%s,%s,%s)"

                                    val2 = (assign_id['Id'], j['Student_Id'], 1)

                                    cursor.execute(st2, val2)

                                    connection.commit()

                    if (success == False):
                        print("Error! Invalid Course ID entered.Try again\n")

                    cursor.close()

                    connection.close()

                except Exception as ex:
                    print("Error! Unable to connect to Database")
                    print(ex)

    def ViewAssignedCourses(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='1234',
                                         database='cms',
                                         cursorclass=pymysql.cursors.DictCursor)

            cursor = connection.cursor()

            res = cursor.execute("select * from Course where Teacher_Id = '" + str(self.__Id) + "'")
            crs = cursor.fetchall()

            if res == 0:
                print("You are not Assigned any Course yet!")
                return False
            else:
                print("{:<15} {:<15} {:<15}".format('ID', 'CourseName', 'CreditHours'))

                for i in crs:
                    print("{:<15} {:<15} {:<15}".format(str(i['Id']), str(i['CourseName']), str(i['CreditHours'])))

            cursor.close()

            connection.close()

            return True

        except Exception as ex:
            print("Error! Unable to connect to Database")
            print(ex)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance