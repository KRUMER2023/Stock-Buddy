import re
from datetime import datetime
import VerifyEmail
import database
import time
from tools import printMessage,userChoice

# Name:   r'^[A-Z][a-z]+(?: [A-Z][a-z]+)*$'
# email:  r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
# Nt:     r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z0-9_]+$'
# passw:  r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$'



def verifyName():
    while True:
        Name=input("\nEnter Your Full Name : ")
        pattern = r'^[A-Z][a-z]+(?: [A-Z][a-z]+)*$'
        if re.match(pattern, Name):
            if Name=="Null"or Name=="NULL" or Name=="null":
                print("The Name Should Not Be 'NULL'.....")
                time.sleep(1)
                continue
            return Name 
        else:
            # print("\nInvalid Full Name. Please enter a name with proper capitalization.\n")
            print("\n\nPlz Enter Valid Name [1st letter capital of each part seperated by space eg: Krunal Parmar\n")
    
def verifyEmail():
    while True:
        Email=input("Enter Your Email : ")
        pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        if re.match(pattern, Email):
            # print("Valid Email")
            return Email
        else:
            print("\n\nInvalid Email. Please enter a valid Gmail address.")
                  
def verifyMobile():
    while True:
        Mobile=input("Enter the mobile no. (10 digit no. only):")
        if len(Mobile)==10 and int(Mobile)>0:
            return int(Mobile)
        else:
            print("\n\nInvalid Mobile No. Please enter a valid Mobile No. :\n")
            
def verifyDOB():
    while True:
        print("Enter your Birth date (insure that u are above 18) :\n")
        dt=int(input("Enter Day:"))
        mo=int(input("Enter Month:"))
        yr=int(input("Enter Year:"))
        if yr>1900 and yr<=datetime.now().year:
            try:
                datetime(yr, mo, dt) 
            except ValueError:
                print("\nThe Entered date is not valid...\nAgain Enter the date:\n")
                time.sleep(2)
                continue
            if datetime.now().year-yr-1>=18:
                dob=str(yr)+"/"+str(mo)+"/"+str(dt)
                # print(dob)
                # break
                return dob
            else:
                print("You are below 18 so not eligible for registration.....")
                time.sleep(2)
                print("\nPlz Enter the correct Date....\n")
                # should add main funtion
        else:
            print("The year range is betweeen 1900 -",datetime.now().year,"\nEnter the date again....")
            time.sleep(1)
                
def validNT():
    while True:
        
        nameTag = input("\nCreate Your NameTag , It must contain:\n"
                    "- At least one uppercase letter\n"
                    "- At least one lowercase letter\n"
                    "- At least one digit\n"
                    "- Optionally underscores (_)\n"
                    "\nCreate : ")
            
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z0-9_]+$'
        if re.match(pattern, nameTag):
            if database.checkNT(nameTag)==None:
                printMessage("Error While validating Name Tag Try Again")
                time.sleep(1)
            elif not database.checkNT(nameTag):
                return nameTag
            else:
                print("\nEntered Name Tag not Available .....\n")
                time.sleep(1)
                print("Crete New Nametag::\n")
            
        else:
            print("\nEntered Name Tag not Valid .....\n")
            time.sleep(1)
            print("Crete New Nametag::\n")
            time.sleep(1)

def validPassword():
    while True:
        print("Password must meet the following conditions:")
        print("- At least 8 characters long")
        print("- At least one uppercase letter")
        print("- At least one lowercase letter")
        print("- At least one digit")
        print("- At least one special character (e.g., !@#$%^&*())\n")
        password = input("\nCreate your password: ") 
        
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$'
        
        if re.match(pattern, password):
            print("Password is valid!")
            return password
        else:
            print("\nInvalid password. Please ensure it meets the conditions.\n")
            time.sleep(1)

def OTP(email):
    while True:
        print(f"\nSending OTP to {email}...")
        otp = VerifyEmail.send_otp(email)
        
        Uotp = input(f"Enter the OTP sent to {email}: ")
        if Uotp == otp:
            printMessage("OTP Verification Successful")
            time.sleep(1)
            return True
        else:
            printMessage("Incorrect OTP")
        
       
        while True:
            print("\nOptions:\n1. Re-enter OTP\n2. Resend OTP\n3. Exit Registration")
            ch = input("Choose an option : ")
            
            if ch == "1":
                Uotp = input(f"Enter the OTP sent to {email}: ")
                if Uotp == otp:
                    printMessage("OTP Verification Successful")
                    time.sleep(1)
                    return True
                else:
                    printMessage("Incorrect OTP")
                    time.sleep(1)
            
            elif ch == "2":
                print("\nResending OTP...")
                break 
            
            elif ch=="3":
                printMessage("Exiting The Registration Process.....")
                time.sleep(1)
                return False          
            else:
                printMessage("\nInvalid choice. Please select either 1 or 2.")
                time.sleep(1)

def Registration():
    printMessage("Plz Enter the correct details only")
    time.sleep(1)
    Name = verifyName()
    Email = verifyEmail()
    Mobile = verifyMobile()
    DOB = verifyDOB()
    NameTag = validNT()
    Password = validPassword()
    
    printMessage("Plz Check The Details Are Correct")
    time.sleep(1)
    
    print(f"""
Name:    {Name}
NameTag: {NameTag}
Email:   {Email}
Mobile:  {Mobile}
DOB:     {DOB}
          """)
    
    if userChoice("Want To Submit "):   
        if OTP(Email):
            if database.insert_user_data(Name, Email, Mobile, DOB, NameTag, Password):
                printMessage("Registration Successful Now Login")
                time.sleep(1)
                
            else:
                printMessage("Registration Unsuccessful Register Again")
                time.sleep(1)
    else:
        printMessage("Registration Unsuccessful Register Again")
        time.sleep(1)

