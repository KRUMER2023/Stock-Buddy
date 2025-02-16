import yfinance as yf
import pandas as pd
from datetime import datetime
from database import wallet , RecordTransaction ,ekycCheck
from tools import printMessage , userChoice
import time

def getPrice(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        if data.empty:
            print(f" Error: Ticker '{ticker}' not found. Please check the symbol and try again.")
            return None
        return data['Close'].iloc[-1]
    except Exception as e:
        # print(f" Unexpected error fetching price for '{ticker}': {e}")
        return None

def sell(id):
    if ekycCheck(id,get=True)==0:
        printMessage("Your Ekyc Is Not Completed")
        time.sleep(1)
        printMessage("Complete Your Ekyc ....")
        return
    ticker=input("Enter the Symbol OR Ticker : ")
    price=getPrice(ticker)
    if price==None:
        return
    price=round(price,2)
    print(f"\nPrice : Rs. {price} ")
    while True:
        try:
            qt=int(input("Enter the No. Of Shares You Want To Sell : "))
            if qt>0:
                break
            else:
                printMessage("Invalid Quantity")
                time.sleep(1)
        except ValueError:
            printMessage("Invalid Quantity")
            time.sleep(1)
            continue
        
    total=round(qt*price,2)
    # print("tot: ",total)
    balance=float(wallet(id,get=True))
    # print("bal: ",balance)
    printMessage(f"\tThe Selling Amount : {total}\n\tYour Current Balance : {balance}")
    time.sleep(1)
    
    if userChoice("Confirm To Sell:")==False:
        return
    else:
        upBalance=balance+total
        # print("after: ",upBalance)
        wallet(id,update=True,amount=upBalance)
        RecordTransaction(id,f"{ticker} Stock Sold Out",0,total,balance,upBalance,f"Sold {qt} Stocks of {ticker}",ticker,qt,price)
        time.sleep(1)
        printMessage("Payment Successful....")
        time.sleep(1)
        
    
# sell(15)