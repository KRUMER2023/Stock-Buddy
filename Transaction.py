from prettytable import PrettyTable
from colorama import Fore, Style
import database

def display_transactions(id):
    cursor=database.getCursor()

    query="SELECT TransactionId, Date, Time,Symbol, TransactionType,`Price Per Share`, Quantity, `Total Amount`, BalanceBefore, BalanceAfter, Description,  Type FROM transaction WHERE ID = %s"

    cursor.execute(query,(id,))
    transactions = cursor.fetchall()

    table = PrettyTable()
    table.field_names = [
        "Transaction Id", "Date", "Time","Symbol", "Transaction Type", "Price Per Share",  "Quantity", "Total Amount",
        "Balance Before", "Balance After", "Description"
    ]

    for row in transactions: 
        if row[-1] == 0:
            row_color = Fore.RED
        elif row[-1] == 1:
            row_color = Fore.GREEN
        elif row[-1] == 2:
            row_color = Fore.YELLOW
        else:
            row_color = Fore.WHITE
        
        formatted_row = [f"{row_color}{value}{Style.RESET_ALL}" for value in row[:-1]]
        table.add_row(formatted_row)

    print(table)


# Call the function
# display_transactions(25)