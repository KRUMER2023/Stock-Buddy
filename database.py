import mysql.connector
from mysql.connector import Error
import time
from tools import printMessage,userChoice

try:
    printMessage("Wait Connecting To The Server")
    time.sleep(1)
        
    # Change TO YOUR DATA BASE CONFIGURATION
    connection = mysql.connector.connect(
        host='localhost',  
        database='testing', 
        user='root', #Change To Your Data base USER NAME
        password='Kru@123'  #Change To Your Database server Password
    )

    if connection.is_connected():
        cursor = connection.cursor()
        
except Error as e:
    if e.errno==2003:
        printMessage("Not Able to Connect to The Server PLz Try Again Later.....")
        time.sleep(1)
        printMessage("Exiting")
        time.sleep(1)
        exit()
    else:
        print(e)
  
# finally:
#     if connection.is_connected():
#         cursor.close()
#         connection.close()
#         print("MySQL connection is closed.")
   
def getCursor():
    return cursor   
    
def insert_user_data(name, email, mobile, dob, name_tag, password):
    try:
        insert_query = """
            INSERT INTO userdata (fname, email, mobile, dob, ntag, password)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        data = (name, email, mobile, dob, name_tag, password)

        cursor.execute(insert_query, data)

        connection.commit()
        return True

        # print("Record inserted successfully.")
    except Error as e:
        print(f"Error: {e}")    
        return False        

def checkNT(ntag,getkey=None,getid=None):
    if getkey==True:
        try:
            query= "SELECT password FROM userdata WHERE ntag = %s"
            cursor.execute(query, (ntag,))
            result = cursor.fetchone()
            if result is None:
                return False
            # printMessage(result[0])
            return result[0]
        except Exception or Error as e:
            print(e)
            return None
        
    if getid==True:
        try:
            query= "SELECT id FROM userdata WHERE ntag = %s"
            cursor.execute(query, (ntag,))
            result = cursor.fetchone()
            return int(result[0])
        except Exception or Error as e:
            print(e)
            return None
            
        
    else:
        try:
            query = "SELECT COUNT(*) FROM userdata WHERE ntag = %s"
            cursor.execute(query, (ntag,))
            result = cursor.fetchone()
            if result[0] > 0:
                return True
                
            else:
                return False
        except Error as e:
            print(f"\nDatabase error: {e}\n")
            time.sleep(1)
            return None
# cursor.close()
# connection.close()

def ekycCheck(id,get=False,update=False):
    try:
        if get:
            query= "SELECT ekyc FROM userdata WHERE id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result[0]==0:
                return False
            else:
                return True
            
        elif update:
            query= "UPDATE userdata SET ekyc = 1 WHERE id = %s;"
            cursor.execute(query, (id,))
            connection.commit()
            query= "INSERT INTO wallet(Id,Balance) VALUES (%s,%s)"
            cursor.execute(query, (id,0))
            connection.commit()
            return True
            
    except Error as e:
        print(e)
        return False


def wallet(id,amount=float(0),get=False,update=False):
    if update:
        query = """
                UPDATE wallet SET Balance = %s WHERE (Id= %s);;
            """
        data =(amount,id)
        cursor.execute(query, data)

        connection.commit()

        
    elif get:
        query="SELECT COUNT(*) FROM wallet WHERE id = %s"
        cursor.execute(query,(id,))
        result=cursor.fetchone()
        if result[0]>0:
            query="SELECT Balance FROM wallet WHERE id=%s"
            cursor.execute(query,(id,))
            result=cursor.fetchone()
            return result[0]
        else:
            print("no Wallet Is Created for this user...")
            return None
    
    else:
        query="SELECT COUNT(*) FROM ekyc WHERE id = %s"
        cursor.execute(query,(id,))
        result=cursor.fetchone()
        if result[0]>0:
            return True
        else:
            print("no Wallet Is Created for this user...")
            return False
 
def RecordTransaction(id,Ttype,type,amount,before,after,desc,symbol,qt,pps):
    query="""
    INSERT INTO `transaction`
(`id`,
`Date`,
`Time`,
`TransactionType`,
`Type`,
`Total Amount`,
`BalanceBefore`,
`BalanceAfter`,
`Description`,
`Symbol`,
`Quantity`,
`Price Per Share`)
VALUES
(%s,DATE_FORMAT(CURRENT_DATE(), '%d-%m-%y'),TIME_FORMAT(CURRENT_TIME(), '%h:%i %p'),%s,%s,%s,%s,%s,%s,%s,%s,%s);
    """
    data=(id,Ttype,type,float(amount),float(before),float(after),desc,symbol,qt,float(pps))
    try:
        cursor.execute(query,data)
        connection.commit()
    except Error as e:print(e)

# RecordTransaction(15,"sv",1,2.366,2525.363,252.625,"w","sdv",2,2.3)
def addBalance(id):
    while True:
        try:
            Bbefore=wallet(id,get=True)
            if Bbefore is not None:
                print(f"Your Current Balance : {Bbefore}")
                am=float(input("Enter The Amount To Add To Wallet : "))
                if am>2 and userChoice("Confirm To Add ") :
                        Bafter=float(Bbefore)+am
                        # query="UPDATE wallet SET Balance = %s WHERE (Id= %s);"
                        # data=(Bafter,id)
                        # cursor.execute(query,data)
                        # connection.commit()
                        wallet(id,update=True,amount=Bafter)
                        time.sleep(1)
                        RecordTransaction(id,"Add Balance",2,am,Bbefore,Bafter,"Money Added To Wallet",'-',0,0)
                        printMessage(f"Your Current Balance : {Bafter}")
                        time.sleep(1)
                        return
                else:
                    printMessage("You Entered Invalid Amount ...Again Enter...")
                    time.sleep(1)
            else :
                printMessage("Your Wallet Is Not created")
                time.sleep(1)
                printMessage("Complete ekyc to make your wallet")
                return
        except  Error as e:
            print(e)
            # print("Someting Happen Wrong Try Again")
            time.sleep(1)
   
# addBalance(23)         
# RecordTransaction(15,"Add Balance",0,3,10,13,"Money Added To Wallet",'-',0,0)
