import Registration
import Login
import time
from tools import printMessage


def start():
    
    while True:
        printMessage("\t\t\tWelocme to Stock buddy.\n\t\tWe are here to help you to everything we can")
        time.sleep(1)
        print("Login Or Register:\n")
        print("1. Login \n2. Register new User\n3. Exit\n")
        try:
            ch=input("Enter Choice: ")
            if ch.isdigit():
                ch=int(ch)   
                if ch==1:
                    id,name_tag=Login.login()
                    if id!=None or name_tag!=None:
                        Login.loginMenu(id)
                        Login.loginMenu2(id,name_tag)
                elif ch==2 :
                    Registration.Registration()
                
                elif ch==3:
                    printMessage("Exiting")
                    time.sleep(1)
                    exit()
                    
                else:
                    print("Invalid Choice plz Enter Correct Choice.....\n\n")
                    time.sleep(1)
            else:
                print("Invalid Choice plz Enter Correct Choice.....\n\n")
                time.sleep(1)
        except ValueError:
            printMessage("Invalid Choice, Try Again....")
            time.sleep(1)
            
if __name__ == "__main__":
    start()     