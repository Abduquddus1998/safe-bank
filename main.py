import csv
import os
import sys
import pandas as pd

menu_list = [
    {
        "name": "Check balance",
        "value": 1
    },
    {
        "name": "Withdrawing money",
        "value": 2
    },
    {
        "name": "Transfers funds",
        "value": 3
    },
    {
        "name": "Depositing money",
        "value": 4
    },
]


class SignUp:
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.confirm_password = None
        self.password = None
        self.job = None
        self.phone = None
        self.address = None
        self.passport_num = None
        self.is_same = False
        self.db = Db()

    def get_user_info(self):
        self.first_name = input("Enter first name: ")
        self.last_name = input("Enter last name: ")
        self.passport_num = input("Enter passport number: ")
        self.address = input("Enter address: ")
        self.phone = input("Enter phone number: ")
        self.job = input("Enter your job title: ")

        while not self.is_same:
            self.password = input("Enter password: ")
            self.confirm_password = input("Confirm password: ")

            if len(self.password) > 0 and len(self.confirm_password) > 0 and self.password != self.confirm_password:
                self.is_same = False
                print("Passwords does not match please enter them again")
                continue
            else:

                print("\n")
                print("################## You account was created successfully ##################")
                print("Account details")
                print(f"Full name: {self.first_name} {self.last_name}")
                print(f"Phone number: {self.phone}")
                print(f"Passport number: {self.passport_num}")
                print(f"Address: {self.address}")
                print(f"Job title: {self.job}")
                self.save_user()
                self.is_same = True
                break

    def save_user(self):
        account = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "passport_num": self.passport_num,
            "phone": self.phone,
            "address": self.address,
            "job": self.job,
            "password": self.password
        }

        self.db.save_account(account)


class Db:
    def __init__(self):
        self.accounts_path = "accounts.csv"
        self.accounts_df = None

    def save_account(self, account):
        fieldnames = ["first_name", "last_name", "passport_num", "phone", "address", "job", "password"]
        is_empty = not os.path.isfile(self.accounts_path) or os.path.getsize(self.accounts_path) == 0

        try:
            with open(self.accounts_path, 'a', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                if is_empty:
                    writer.writeheader()

                writer.writerows([account])
        except FileNotFoundError:
            print("Error: File 'accounts.csv' not found.", FileNotFoundError)

    def get_accounts(self):
        if os.path.isfile(self.accounts_path):
            self.accounts_df = pd.read_csv("accounts.csv")
            return self.accounts_df


class SafeBank:
    def __init__(self):
        self.is_valid = False
        self.db = Db()
        self.accounts = self.db.get_accounts()

    def login(self):
        passport_num = input("Enter your passport number: ")
        password = input("Enter your password: ")

        if len(password) == 0 or len(passport_num) == 0:
            print("wrong details")

        account = self.accounts[self.accounts["passport_num"] == passport_num]

        print("account", account[0:1])

    def display_menu(self):
        print("\n")
        print("############## Available services for the account ##############")

        for menu_item in menu_list:
            print(f"{menu_item['value']}. {menu_item['name']}")

        while True:
            menu_option = input("Enter option number: ")

            try:
                selected_option = int(menu_option)

                if selected_option not in range(1, len(menu_list) + 1):
                    print("Please enter appropriate option number")
                    return

                if selected_option == 1:
                    print("Check Balance")
                elif selected_option == 2:
                    print("Withdrawing money")
                elif selected_option == 3:
                    print("Transfer funds")
                else:
                    print("Depositing money")

            except:
                print("Wrong option number was entered, please enter right option number")


safe_bank = SafeBank()
sign_up = SignUp()

print("################# Welcome to Safe Bank #################")
print("1. Login")
print("2. Create an account")

while True:
    option = input("Please enter option number or press X to terminate the program: ")

    if option.lower() == "x":
        sys.exit()

    try:
        option_num = int(option)

        if int(option_num) not in [1, 2]:
            print("Please choose 1 or 2 to continue")
        else:
            if option_num == 1:
                safe_bank.login()
            else:
                sign_up.get_user_info()
                safe_bank.display_menu()
                break
    except:
        print("Wrong option was entered, please enter right option number")
