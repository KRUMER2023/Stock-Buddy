import database
import time
from tools import printMessage , userChoice
import Transaction 
import subprocess
from Buy import buy
from Sell import sell
import webbrowser
    
def login():
    while True:
        name_tag = input("Enter your Name Tag: ")
        password = input("Enter your Password: ")
        storedPassword=database.checkNT(name_tag,getkey=True)
        if storedPassword is False:
            printMessage("Incorrect Name Tag ... Try Again")
            time.sleep(1)
            if not userChoice("Want to Login Again"):
                return None,None
            
        elif storedPassword is None :
            printMessage("Not Able To Validate ... Try Again")
            time.sleep(1)
        else:
            if password == storedPassword:
                
                if database.checkNT(name_tag,getid=True) is not None :
                    printMessage("Login Successfull")
                    time.sleep(1)
                    return database.checkNT(name_tag,getid=True),name_tag
                else:
                    printMessage("Error in Fetching Details ... Try Again")
                    time.sleep(1)
                    if not userChoice("Want to Login Again"):
                        return None,None
                
            else : 
                printMessage("Incorrect Password .... Try Again")
                time.sleep(1)
                if not userChoice("Want to Login Again"):
                    return None,None

def ekyc(id):
    printMessage("Have to provide your Adhaar card details ...")
    time.sleep(2)
    while True:
        adhaarNo=input("Enter your Adhaar Card No. (without spaces):")
        if adhaarNo.count(" ") >0 or len(adhaarNo)!=12 or int(adhaarNo)<=0 or int(adhaarNo)<100000000000:
            print("Plz Enter the Correct Adhaar no.")
            
        else:
            printMessage("Adhaar No. Verified")
            time.sleep(2)
            eKYCch=database.ekycCheck(id,update=True)
            if eKYCch:
                printMessage("Wallet is created but empty...")
                time.sleep(2)
                if userChoice("Want to add money to wallet:"):
                    # 
                    database.addBalance(id)
                    return True
                else:
                    #
                    print("Enjoy") 
                    return True
            else:
                printMessage("Ekyc Not Completed Successfully...")
                if not userChoice("Want to try again: "):
                    return False
      
      
def ekycmenu(id):
    printMessage("Checking Your Ekyc Status....")
    time.sleep(1)
    if database.ekycCheck(id,get=True):
        printMessage("Your Ekyc Is Completed....Also Your Wallet is Created")
        time.sleep(2)
        
    else:
        printMessage("Your Ekyc is not Completed and Your Wallet Is Not Created")
        time.sleep(1)
        if userChoice("\nDo You Want To Complete Your Ekyc ") :
            ekyc(id)
        else:
            printMessage("Eyc Not Completed ....")
    

def loginMenu(id):
    eKYCch=database.ekycCheck(id,get=True)
    if eKYCch==False:
        printMessage("Welcome")
        time.sleep(2)
        printMessage("Want to Compelete your ekyc to start your instant wallet:")
        if userChoice("Choice"):
            wallet=ekyc(id)
            if wallet:
                printMessage("Wallet Created ....")
            else:
                printMessage("Wallet is not Created  ...")
        else:
            printMessage("ekyc Not Completed so Limited Features you can use...")
   
def run_streamlit_app():
    process = subprocess.run(
        ["streamlit", "run", "Graph.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(3)
    # webbrowser.open("http://localhost:8501")    
# run_streamlit_app()

def loginMenu2(id,name_tag):
    printMessage(f"Welcome {name_tag}")
    time.sleep(1)
    
    
    while True:
        printMessage("Enter Choice")
        time.sleep(1)
        print(
        """ 
        1. Live Data
        2. Check Wallet Balance
        3. Add Balance
        4. Buy
        5. Sell
        6. Transaction History
        7. Check eKYC Status
        8. Logout
        9. Exit
        
        """)
        try:
            ch=int(input("Enter Choice:"))
            if ch<=0 or ch>10:
                print("Invalid Choice ....")
            
            
            elif ch==1 :
                printMessage("press 'Ctrl + c' to continue...")
                run_streamlit_app()

            elif ch==2 :
                bal=database.wallet(id,get=True)
                if not None:
                    printMessage(f"Current Balance = {bal}")
                    time.sleep(2)
            
            elif ch==3 :
                database.addBalance(id)
                
            elif ch==4 :
                buy(id)
                
            elif ch==5 :
                sell(id)
                
            elif ch==6 :
                Transaction.display_transactions(id)
                
            elif ch==7 :
                ekycmenu(id)
            
            elif ch==8 :
                return
                
            elif ch==9 :
                exit()
                
        except ValueError:
                printMessage("Invalid Choice, Try Again....")
                time.sleep(1)
                
        except KeyboardInterrupt:
            continue
            
# loginMenu2(15,'kru')