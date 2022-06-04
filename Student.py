import pymysql.cursors

class Student:
    __Id = None
    __Name = None
    __Rollno = None
    __Batch = None
    __SemesterDues = None
    __CurrentSemester = None

    def get_Id(self):
        return self.__Id

    def get_name(self):
        return self.__Name

    def get_roll_no(self):
        return self.__Rollno

    def get_batch(self):
        return self.__Batch

    def get_semester_dues(self):
        return self.__SemesterDues

    def get_current_semester(self):
        return self.__CurrentSemester

    def set_Id(self,id):
        self.__Id = id

    def set_name(self, nm):
        self.__Name = nm

    def set_roll_no(self, rno):
        self.__Rollno = rno

    def set_batch(self, bch):
        self.__Batch = bch

    def set_semester_dues(self, dues):
        self.__SemesterDues = dues

    def set_current_semester(self, sem):
        self.__CurrentSemester = sem

    def StudentLogin(self):
        print("************************Student Login************************")
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
                    print("Unable to proceed! No data for Students exit in Database\n")
                    return False

                usr = input("Enter Student Username: ")
                passw = input("Enter Student Password: ")
                type = "student"

                array_of_dict_creds = cursor.fetchall()

                for i in array_of_dict_creds:

                    if usr == str(i['Username']) and passw == str(i['Password']) \
                            and type == str(i['Type']):

                        success = True
                        cursor.execute("select Id from Credentials where Username = '"+usr+"'")
                        cid = cursor.fetchone()
                        cursor.execute("select Id from Student where Cred_Id = '"+str(cid['Id'])+"'")
                        sid = cursor.fetchone()
                        self.__Id = sid['Id']

                if (success == False):
                    print("Error! Invalid Username or Password entered.Try again\n")

                cursor.close()

                connection.close()

            except Exception as ex:
                print("Error! Unable to connect to Database")
                print(ex)

        self.DisplayStudentMenu()
        return True

    def DisplayStudentMenu(self):
        running = True

        while running:
            print("\n")
            print("Enter 1 to Pay Semester Dues\n")
            print("Enter 2 to view enrolled courses\n")
            print("Enter 3 to view Assignments\n")
            print("Enter 4 to Update Assignment Status\n")
            print("Enter 5 to Exit\n")

            inp = int(input("Enter Choice: "))

            if inp < 1 or inp > 5:
                print("Invalid input! Must be in range 1-5\n")

            else:
                if inp == 1:
                    self.PaySemesterDues()

                elif inp == 2:
                    self.ViewEnrolledCourses()

                elif inp == 3:
                    connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='1234',
                                                 database='cms',
                                                 cursorclass=pymysql.cursors.DictCursor)

                    cursor = connection.cursor()

                    en_res = cursor.execute("select Course_Id from Enroll "
                                            "where Student_Id = '" + str(self.__Id) + "'")

                    if en_res == 0:
                        print("You are not Enrolled in any Course yet!")
                        cursor.close()
                        connection.close()
                    else:
                        c_id = input("Enter Course ID of whose assignments you want to view: ")
                        self.ViewAssignments(c_id)

                elif inp == 4:
                    connection = pymysql.connect(host='localhost',
                                                 user='root',
                                                 password='1234',
                                                 database='cms',
                                                 cursorclass=pymysql.cursors.DictCursor)

                    cursor = connection.cursor()

                    en_res = cursor.execute("select Course_Id from Enroll "
                                            "where Student_Id = '" + str(self.__Id) + "'")

                    if en_res == 0:
                        print("You are not Enrolled in any Course yet!")
                        cursor.close()
                        connection.close()
                    else:
                        self.UpdateAssignmentStatus()
                else:
                    running = False

    def PaySemesterDues(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='1234',
                                         database='cms',
                                         cursorclass=pymysql.cursors.DictCursor)

            cursor = connection.cursor()

            cursor.execute("select SemesterDues from Student where Id = '" + str(self.__Id) + "'")
            dues = cursor.fetchone()

            if dues['SemesterDues']!=0:
                self.__SemesterDues = dues['SemesterDues']

                amt = int(input("Enter Amount to Pay: Rs."))

                while amt > dues['SemesterDues'] or amt <= 0:
                    print("Invalid Input! Entered Amount must be > 0 and <= " + str(dues['SemesterDues']))
                    amt = int(input("Enter Amount to Pay: Rs. "))

                self.__SemesterDues = self.__SemesterDues - amt

                print("\n Your remaining Dues are: Rs." + str(self.__SemesterDues))

                cursor.execute("""
                                        UPDATE Student
                                        SET SemesterDues=%s
                                        WHERE Id =%s
                                        """,
                                        (self.__SemesterDues, self.__Id))

                connection.commit()

            else:
                print("Your all Dues are clear!")

            cursor.close()

            connection.close()

        except Exception as ex:
            print("Error! Unable to connect to Database")
            print(ex)

    def ViewEnrolledCourses(self):
        try:
            connection = pymysql.connect(host='localhost',
                                         user='root',
                                         password='1234',
                                         database='cms',
                                         cursorclass=pymysql.cursors.DictCursor)

            cursor = connection.cursor()

            res = cursor.execute("select Course_Id from Enroll where Student_Id = '" + str(self.__Id) + "'")
            cids = cursor.fetchall()

            if res == 0:
                print("You are not Enrolled in any Course yet!")

            else:
                print("{:<15} {:<15} {:<15} {:<15}".format('ID', 'CourseName', 'CreditHours', 'AssignedTeacherID'))

                for i in cids:
                    cursor.execute("select * from Course where Id = '" + str(i['Course_Id']) + "'")
                    arr = cursor.fetchall()
                    crs = arr[0]

                    print("{:<15} {:<15} {:<15} {:<15}".format(str(crs['Id']),str(crs['CourseName']),
                          str(crs['CreditHours']),str(crs['Teacher_Id'])))

            cursor.close()

            connection.close()

        except Exception as ex:
            print("Error! Unable to connect to Database")
            print(ex)

    def ViewAssignments(self,course_id):
        success = False

        while (success == False):
            try:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234',
                                             database='cms',
                                             cursorclass=pymysql.cursors.DictCursor)

                cursor = connection.cursor()

                res = cursor.execute("select * from Enroll where Student_Id = '"+str(self.__Id)+"' and "
                                    "Course_Id = '"+course_id+"'")

                if res != 0:
                    success = True
                    is_Pending = False
                    lis = []

                    cursor.execute("select Id from Assignment where Course_Id = '"+course_id+"'")
                    array_of_dict_assign_id = cursor.fetchall()

                    for i in array_of_dict_assign_id:
                        assign_res = cursor.execute("select Assignment_Id from Assignment_Status where "
                                       "Assignment_Id = '"+str(i['Id'])+"' and Student_Id = '"+str(self.__Id)+"' "
                                        "and Pending = 1")

                        array_of_dict_assign_status = cursor.fetchall()

                        if assign_res != 0:
                            is_Pending = True

                            for j in array_of_dict_assign_status:
                                cursor.execute("select * from Assignment "
                                               "where Id = '" + str(j['Assignment_Id']) + "'")

                                array_of_dict_assign = cursor.fetchall()

                                for k in array_of_dict_assign:
                                    details = (str(k['Id']),k["Topic"],k["Description"],str(k['Deadline']))
                                    lis.append(details)

                    if is_Pending == False:
                        print("There are currently no pending assignments!")
                    else:
                        print("{:<15} {:<15} {:<25} {:<15}".format('ID', 'Topic', 'Description', 'Deadline'))

                        for i in lis:
                            print("{:<15} {:<15} {:<25} {:<15}".format(str(i[0]), str(i[1]),str(i[2]), str(i[3])))

                if (success == False):
                    print("Error! Invalid Course ID entered.Try again\n")
                    course_id = input("Enter Course ID of whose assignments you want to view: ")

                cursor.close()

                connection.close()

            except Exception as ex:
                print("Error! Unable to connect to Database")
                print(ex)

    def UpdateAssignmentStatus(self):
        success = False

        while (success == False):
            try:
                connection = pymysql.connect(host='localhost',
                                             user='root',
                                             password='1234',
                                             database='cms',
                                             cursorclass=pymysql.cursors.DictCursor)

                cursor = connection.cursor()

                assign_count = cursor.execute("select * from Assignment_Status "
                                              "where Student_Id = '" + str(self.__Id) + "'")

                if assign_count == 0:
                    print("There are currently no assignments!")
                    success = True
                else:
                    assign_id = input("Enter Assignment ID to Update Assignment Status: ")

                    res = cursor.execute("select * from Assignment_Status "
                                         "where Student_Id = '" + str(self.__Id) + "'"
                                            " and Assignment_Id = '" + assign_id + "'")
                    if res != 0:
                        success = True

                        status = input("Enter Assignment Status ('1' for Pending OR '0' for Completed): ")

                        while status != '0' and status != '1':
                            print("Error! Invalid input. You must enter '0' or '1' only")
                            status = input("Enter Assignment Status ('1' for Pending OR '0' for Completed): ")

                        cursor.execute("""
                                                                UPDATE Assignment_Status
                                                                SET Pending=%s
                                                                WHERE Assignment_Id =%s
                                                                and Student_Id =%a
                                                                """, (status, assign_id, self.__Id))

                        connection.commit()

                    if (success == False):
                        print("Error! Invalid Assignment ID entered.Try again\n")

                    cursor.close()

                    connection.close()

            except Exception as ex:
                print("Error! Unable to connect to Database")
                print(ex)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)

        return cls.instance