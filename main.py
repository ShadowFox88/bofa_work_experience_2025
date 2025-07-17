import string
import random
import psycopg
import bcrypt
from dataclasses import dataclass
import requests

CURRENCIES = ['AFN', 'DZD', 'ARS', 'AMD', 'AWG', 'AUD', 'AZN', 'BSD', 'BHD', 'THB', 'PAB', 'BBD', 'BYR', 'BZD', 'BMD', 'VEF', 'BOB', 'BRL', 'BND', 'BGN', 'BIF', 'CAD', 'CVE', 'KYD', 'GHS', 'CLP', 'COP', 'KMF', 'CDF', 'BAM', 'NIO', 'CRC', 'HRK', 'CUP', 'CZK', 'GMD', 'DKK', 'MKD', 'DJF', 'STD', 'DOP', 'VND', 'XCD', 'EGP', 'SVC', 'ETB', 'EUR', 'FKP', 'FJD', 'HUF', 'GIP', 'XAU', 'HTG', 'PYG', 'GNF', 'GYD', 'HKD', 'UAH', 'ISK', 'INR', 'IRR', 'IQD', 'JMD', 'JOD', 'KES', 'PGK', 'LAK', 'KWD', 'MWK', 'AOA', 'MMK', 'GEL', 'LVL', 'LBP', 'ALL', 'HNL', 'SLL', 'RON', 'LRD', 'LYD', 'SZL', 'LTL', 'LSL', 'MGA', 'MYR', 'MUR', 'MZN', 'MXN', 'MDL', 'MAD', 'BOV', 'NGN', 'ERN', 'NAD', 'NPR', 'ANG', 'ILS', 'TMT', 'TWD', 'NZD', 'BTN', 'KPW', 'NOK', 'PEN', 'MRO', 'PKR', 'XPD', 'MOP', 'TOP', 'CUC', 'UYU', 'PHP', 'XPT', 'GBP', 'BWP', 'QAR', 'GTQ', 'ZAR', 'OMR', 'KHR', 'MVR', 'IDR', 'RUB', 'RWF', 'SHP', 'SAR', 'RSD', 'SCR', 'XAG', 'SGD', 'SBD', 'KGS', 'SOS', 'TJS', 'ZAR', 'LKR', 'XSU', 'SDG', 'SRD', 'SEK', 'CHF', 'SYP', 'BDT', 'WST', 'TZS', 'KZT', 'TTD', 'MNT', 'TND', 'TRY', 'AED', 'USD', 'UGX', 'COU', 'CLF', 'UYI', 'UZS', 'VUV', 'KRW', 'YER', 'JPY', 'CNY', 'ZMK', 'ZWL', 'PLN']


# TODO:
# - Transaction History
# - Create Account

currency_data = requests.get("https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json")
data = currency_data.json()

fx: dict[str, float] = {}

for i in zip(data["usd"].keys(), data["usd"].values()):
    if i[0].upper() in CURRENCIES:
        fx[i[0].upper()] = i[1]

def generateID() -> str:
    while True:
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

@dataclass
class User:
    id: str
    password: str
    balance: float
    currency: str


def get_user(accountID: str) -> User | None:
    with psycopg.connect("postgresql://bofa:bofa_wex_2025@localhost:5432/bofa") as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE id = %s", [accountID])
            _data = cursor.fetchone()

    
    return User(
            id=_data[0], 
            password=_data[1], 
            balance=_data[2],
            currency=_data[3]
        ) if _data else None

def create_user(password: str, currency: str) -> str | None:
    if currency.upper() not in CURRENCIES:
        return None
    
    id = generateID()

    with psycopg.connect("postgresql://bofa:bofa_wex_2025@localhost:5432/bofa") as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (id, password, currency) VALUES (%s, %s, %s)",
                (id, bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(), currency)
            )
            
        connection.commit()
    
    return id

def verify(accountID: str, password: str) -> bool:
    user = get_user(accountID)

    if not user:
        return False
    
    return bcrypt.checkpw(password.encode(), user.password.encode())

def deposit(accountID: str, money: float) -> bool:
    with psycopg.connect("postgresql://bofa:bofa_wex_2025@localhost:5432/bofa") as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (money, accountID))

            if cursor.rowcount == 0:
                return False
            
        connection.commit()
    
    return True

def help() -> None:
    print('exit                        : Shutdown the application')
    print('login <username> <password> : Login to the application')
    print('deposit <amount>            : Deposit funds in your account')
    print('send <accountId> <amount>   : Send funds to another account')
    print('balance                     : Print your account balance')
    print('logs                        : View your transaction history')
    print('help                        : Print this message again')

logged_in_user: User | None = None

def log(user: User, transaction_type: str, amount: float, recipient_id: str | None = None) -> None:
    with psycopg.connect("postgresql://bofa:bofa_wex_2025@localhost:5432/bofa") as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO transactions (id, transaction_type, amount, currency, recipient_id) VALUES (%s, %s, %s, %s, %s)",
                (user.id, transaction_type, amount, user.currency, recipient_id)
            )
        connection.commit()

def login(accountID: str, password: str) -> str:
    global logged_in_user
    user = get_user(accountID)

    if not verify(accountID, password):
        return "Incorrect credentials. Please try again."
    
    logged_in_user = user
    return f"You are now logged in as {accountID}"

def refresh_logged_in_user() -> None:
    global logged_in_user
    if logged_in_user:
        logged_in_user = get_user(logged_in_user.id)
    else:
        logged_in_user = None

def deposit_funds(amount: float) -> str:
    if not logged_in_user:
        return "You must be logged in to deposit funds."
    
    result = deposit(logged_in_user.id, amount)
    log(logged_in_user, "deposit", amount)

    return "Deposit successful." if result else "Deposit failed. Please try again."

def balance_check() -> float | None:
    refresh_logged_in_user()
    if not logged_in_user:
        return None
    
    return logged_in_user.balance

def send_funds(accountID: str, amount: float) -> str:
    if not logged_in_user:
        return "You must be logged in to send funds."
    
    if amount <= 0:
        return "Amount must be greater than zero."
    
    if logged_in_user.balance < amount:
        return "Insufficient funds."
    
    recipient_user = get_user(accountID)
    if not recipient_user:
        return "Recipient account does not exist."
    
    recipient_amount = amount * fx[recipient_user.currency] / fx[logged_in_user.currency]

    with psycopg.connect("postgresql://bofa:bofa_wex_2025@localhost:5432/bofa") as connection:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, logged_in_user.id))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (recipient_amount, accountID))
        
        connection.commit()
    
    refresh_logged_in_user()
    log(logged_in_user, "send", amount, accountID)
    return "Funds sent successfully."

def see_logs(user: User) -> str:
    if not user:
        return "You must be logged in to see logs."
    
    with psycopg.connect("postgresql://bofa:bofa_wex_2025@localhost:5432/bofa") as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM transactions WHERE id = %s", (user.id,))
            logs = cursor.fetchall()
    
    if not logs:
        return "No transaction history found."
    
    log_output: list[str] = []
    for log in logs:
        log_output.append(f"Action: {log[1]} | Amount: {log[2]} {log[3]} | " + (f"Recipient: {log[4]} | " if log[4] else "") + f"Timestamp: {log[5]}")
    
    return "\n".join(log_output)

while True:
    try:
        refresh_logged_in_user()
        command = input("Enter command: ").strip().lower()

        if command == "exit":
            print("Shutting down the application.")
            break
        elif command == "help":
            help()
        elif refresh_logged_in_user is None:
            print("You must be logged in to perform actions. Please login first.")
        elif command.startswith("login "):
            _, accountID, password = command.split()
            print(login(accountID, password))
        elif command.startswith("deposit "):
            _, amount = command.split()
            print(deposit_funds(float(amount)))
        elif command.startswith("send "):
            _, accountID, amount = command.split()
            print(send_funds(accountID, float(amount)))
        elif command == "logs":
            if logged_in_user is not None:
                print(see_logs(logged_in_user))
            else:
                print("You must be logged in to see logs.")
        elif command == "balance":
            balance = balance_check()
            if balance is not None and logged_in_user is not None:
                print(f"Your balance is: {balance} {logged_in_user.currency}")
            else:
                print("You must be logged in to check your balance.")
        else:
            print("Unknown command. Type 'help' for a list of commands.")
    except Exception as e:
        print(f"An error occurred: {e}" )
        print("An error has occured please try again or type 'help' for assistance.")