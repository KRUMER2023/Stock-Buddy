def printMessage(message):
    line_width = max(len(message) + 10, 48)  
    centered_message = message.center(line_width)
    print("\n" + "-" * line_width)
    print(centered_message)
    print("-" * line_width + "\n")
    
def userChoice(message):
    while True:
        ch=input(message+" (y or n) : ")
        if ch=='y' or ch=='Y':
            return True
        elif ch=='n' or ch=='N':
            return False
        else:
            printMessage("Invalid Choice...")