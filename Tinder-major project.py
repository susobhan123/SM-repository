import mysql.connector

class tinder:

    def __init__(self):

        self.conn=mysql.connector.connect(host="127.0.0.1", user="root", password="", database="tinderb1")
        self.mycursor=self.conn.cursor()

        self.program_menu()

    def program_menu(self):

        program_input=input("""Hi, welcome to The pseudo_tinder, meet your date
        1. pres 1 to login
        2. press 2 to register
        3. press anything else to exit""")

        if program_input=="1":
            self.login()
        elif program_input=="2":
            self.register()
        else:
            print("Thank you, Bye")


    def register(self):
        print("Welcome to registration page")

        name=input("enter name")
        email=input("enter email")
        password=input("enter password")
        age=input("enter age")
        gender=input("enter gender")
        city=input("enter city")

        self.mycursor.execute("""INSERT INTO `user` (`user_id`, `name`, `email`, `password`, `Age`, `Gender`, `City`)
                                                VALUES (NULL, '{}', '{}', '{}', '{}', '{}', '{}')""".format(name,email, password, age, gender, city))

        

        print("registration is successful")
        self.conn.commit()
        self.program_menu()

        
    def login(self):

        email=input("Enter your email : ")
        password=input("Enter your password :")

        self.mycursor.execute("""SELECT * FROM `user` WHERE `email`
                                                    LIKE '{}' AND `password` LIKE '{}'""".format(email,password))

        user_list=self.mycursor.fetchall()

        #print(user_list)

        if len(user_list)>0:
            print("Welcome")
            self.current_user_id=user_list[0][0]
            self.user_menu()


        else:
            print("Incorrect email/password")
            self.program_menu()

    def user_menu(self):

        user_input=input("""Hi how would you like to proceed?
        1. view all users
        2. view who proposed u
        3. view ur proposal
        4.view ur matches
        5. anything to get out""")
        
        if user_input=="1":
            self.view_all_user()
        elif user_input=="2":
            self.view_proposed()
        elif user_input=="3":
            self.view_proposal()
        elif user_input=="4":
            self.view_matches()
        else:
            self.logout()

    def view_all_user(self):

        self.mycursor.execute("""SELECT * FROM `user` WHERE `user_id`
        NOT LIKE `{}`""".format(self.current_user_id))
        all_user=self.mycursor.fetchall()
        #print(all_users)

        for i in all_user:
            print(i[0],"|",i[1],"|",i[4],"|",i[5],"|",i[6])
            print("______________________________")

        self.juliet_id=int(input("Enter the id of the user whom you would like to propose"))

        self.propose(self.juliet_id)

    def propose(self, juliet_id):
        self.mycursor.execute("""INSERT INTO `proposals` (`proposal_id`, `romeo_id`, `juliet_id`)
                                             VALUES (NULL, '{}', '{}')""".format(self.current_user_id, juliet_id))

        self.conn.commit()

        print("proposal sent successfully!finger crossed")
        self.user_menu()

    def view_proposed(self):
        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN `user` u ON u.`user_id`=p.`romeo_id`
        WHERE p.`juliet_id`='{}'""".format(self.current_user_id))

        who_proposed=self.mycursor.fetchall()

        for i in who_proposed:
            print(i[4],"|",i[5],"|",i[7],"|",i[8],"|",i[9])
            print("----------------------------------------------")

            self.user_menu()

    def view_proposal(self):
         self.mycursor.execute("""SELECT * FROM `proposals` p JOIN `user` u ON u.`user_id`=p.`juliet_id`
         WHERE p.`romeo_id`='{}'""".format(self.current_user_id))
         
         who_proposed=self.mycursor.fetchall()

         for i in who_proposed:
            print(i[4],"|",i[5],"|",i[7],"|",i[8],"|",i[9])
            print("----------------------------------------------")

            self.user_menu()
    def view_matches(self):

        self.mycursor.execute("""SELECT * FROM `proposals` p JOIN `user`u ON u.`user_id`=p.`juiet_id`
WHERE p.`juliet_id` IN (SELECT `romeo_id` FROM `proposals` WHERE `juliet_id` LIKE '{}')AND p.`romeo_id`
LIKE '{}'""".format(self.current_user_id,self.current_user_id))
        matched=self.mycursor.fetchall()
        if len(matched)>0:
            print("NAME \t|\t EMAIL ID \t|\t GENDER \t|\t AGE \t|\t CITY \n ~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            for i in matched:
                print(i[4],"|",i[5],"|",i[7],"|",i[8],"|",i[9])
                print("~~~~~~~~~~~~~~~~~~~~ ~~~~~~~~~")
        else:
            print("sorry!no ane is matched with you yet....but dont lose hope")
            self.user_menu

    def logout(self):
        self.current_user_id=0
        option=input("""do you really want to logout and return to login page?\n enter 'yes' to logout,
                     anything else to stay on this page""")
        if option=="yes":
            print("logged out")
            self.program_menu()
        else:
            self.user_menu()        
  
obj1=tinder()
