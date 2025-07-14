
import sys
import random
import os
from random import randrange
import bofa

# The user initally is logged out
_loggedIn = False
# A random balance is being set when the program starts
_balance = round(random.uniform(1,100), 2)
# The accound id is a unique identifier for each account that will be used when sending funds from one account to another
_accountId = bofa.generateId()
# Teh username of the user is the same as the account id
_username = _accountId
_password = "s3cret"
# A random currency is picked for each 
_currency = ["USD","GBP","EUR"][random.randint(0,2)]

# User commands to be implemented
def login(usr, pwd) -> bool:
    # TODO
    pass
def exit() -> None:
    pass
def deposit(amnt: float) -> None:
    # TODO
    pass
def send(accountId: str, amount: float) -> None:
    # TODO
    pass
def balance() -> None:
    # TODO
    pass

bofa.printWelcomeMessage(_accountId,_balance,_currency)

while True:
    # Wait for user input
    user_input = input('\nWhat do you want to do next? Type help to see all the available options\n > ')
    # Extract the first word from the user input which represents the command
    command = user_input.split(" ")[0].lower()
    
    if command == 'exit':
        exit()
        
    elif command == 'login':
        try:
            usr: str = user_input.split(" ")[1]
            pwd: str = user_input.split(" ")[2]
            if login(usr, pwd):
                print('Congratulations, You have logged in successfully.')
            else:
                print('The credentials you have provided are not correct. Please try again!')
        except Exception as e:
            print("Oops! There has been an unexpected error with your command. Please try again!")  

    elif command == 'send':
        try:
            if _loggedIn:
                accountId = user_input.split(" ")[1]
                amount = user_input.split(" ")[2]
                send(str(accountId),float(amount))
            else:
                print('You have to login first before you can run this command')
        except Exception as e:
            print('Oops! There has been an unexpected error with your command. Please try again!')         
        
    elif command == 'help':
        bofa.help()
        
    elif command == 'balance':
        balance()
        
    elif command == 'deposit':
        try:
            if _loggedIn:
                amount = float(user_input.split(" ")[1])
                deposit(amount)
            else:
                print('You have to login first before you can run this command')
        except Exception as e:
            print("Oops! There has been an unexpected error with your command. Please try again!")        
    
    else:
        print('The command you typed in is not valid. Please try again!')
