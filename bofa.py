import random
import os

def generateId() -> str:
    while True:
        return ''.join(random.choices("abcdefghijklmnopqrstuvwxyz123456789", k=10))

def printWelcomeMessage(accountId, balance, currency) -> None:
    print('\n*************************************************************\n')
    print('Welcome to the Funds Transfer Application for Bank of America')
    print('Your accountId is %s and your balance is %s %s'  % (accountId,balance,currency))
    print('\n*************************************************************')

def updateBalance(balance: float, accountId: str, currency: str) -> float:
    _fx = {
         ("USD", "EUR"): 0.85, # USD -> EUR
         ("EUR", "USD"): 1.19, # EUR -> USD
         ("USD", "USD"): 1,    # USD -> USD
         ("USD", "GBP"): 0.80, # USD -> GBP
         ("GBP", "USD"): 1.28, # GBP -> USD
         ("GBP", "GBP"): 1,    # GBP -> GBP
         ("EUR", "GBP"): 0.9,  # EUR -> GBP
         ("GBP", "EUR"): 1.15, # GBP -> EUR
         ("EUR", "EUR"): 1,    # EUR -> EUR
    }
    # Inner function to apply the FX rate based on the currency that we want to convert
    def convertFx(amount: float, source: str, target: str) -> float:
        return amount * _fx[(source, target)]
    if os.path.exists('accounts_file_db/' + accountId):
        transactions = open('accounts_file_db/' + accountId, '+r')
        for transaction in transactions:
            amount:float = float(transaction.split(" ")[0])
            source:str = str(transaction.split(" ")[1].strip())
            balance = balance + convertFx(amount, source, currency)
        os.remove('accounts_file_db/' + accountId)
        return round(balance,2)
    else:
        return round(balance,2)

def help() -> None:
    print('exit                        : Shutdown the application')
    print('login <username> <password> : Login to the application')
    print('deposit <amount>            : Deposit funds in your account')
    print('send <accountId> <amount>   : Send funds to another account')
    print('balance                     : Print your account balance')
    print('help                        : Print this message again')