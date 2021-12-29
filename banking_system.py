import csv
import re

# MOST OF THE CODE WILL OBVIOUSLY NOT WORK IF THE USERLIST.CSV FILE IS OPEN IN EXCEL
# DUE TO INSUFFICIENT PRIVILEGES, SO ONLY OPEN IT IN SPYDER.



class BankingSystem:

    def __init__(self):
        
        self.username = ''
        self.password = ''
        self.userType = ''
        self.information = []
        self.currentAccount = False
        self.userCurrentAccount = ''
        self.balance = 0
        self.currentSelected = False
        self.savingSelected = False
        self.i = 0
        self.overdraftAmount = ''
        self.accountNumbers = 0

    def run_app(self):
        print("Welcome to the banking system, please log in first.")
        print()
        loginUser = input("Please enter your username: ")

        database = open('userList.csv', 'r', newline='')
        csvreader = csv.reader(database, delimiter=',')

        usernameFound = False
        for row in csvreader:
            
            if loginUser == row[0]:
                self.username = loginUser
                self.password = row[1]
                self.userType = row[2]
                self.information = row[3:]
                
                if (row[4] != ''):
                    self.currentAccount = True
                
                self.information = [string for string in self.information if string !=""]
                usernameFound = True
                break
            self.i +=1
       
        database.close()
        if usernameFound == False:
            print("Incorrect username.")
            

        loginPass = input("Please enter your password: ")
        if loginPass == self.password:
                print("You have now logged in,", self.username)
                print()
                if self.userType == 'user':
                    BankingSystem.customer_view(self)
                elif self.userType == 'admin':
                    BankingSystem.admin_view(self)
                
        else:
            print("Incorrect password.")
    

    
    def customer_view(self):
        
        print("Please select an option:")
        print("1 - View account")
        print("2 - View summary")
        print("3 - Quit", end = """""")
        choice = int(input("Enter a number to select your option: "))
        print()

        if choice == 1:
            BankingSystem.account_selection(self)
        elif choice == 2:
            BankingSystem.summary(self)
        elif choice == 3:
            print("Quitting application.")
        else:
            print("Wrong")
    
    
    
    
    
    
    def account_selection(self):
        
        self.currentSelected = False
        self.savingSelected = False
        
        database = open('userList.csv', 'r', newline='')
        csvreader = csv.reader(database, delimiter=',')
        
        for row in csvreader:
            
            if self.username == row[0]:
                self.information = row[3:]
                self.information = [string for string in self.information if string !=""]
                break
        database.close()    # This is here so the values will update after deposits and withdrawals.
        
        print("--Account List--")
        print("Please select an option (Enter '0' to go back to menu): ")
        print()
        
        for i in range(1, len(self.information)):
            
            if self.currentAccount and i == 1:
                
                
                self.balance = self.information[1].split('Balance: ', 1)
                print("{0} - Current account: £{1}".format(i, self.balance[1])  )
            else:
                self.balance = self.information[i].split('Balance: ', 1)
                print("{0} - Saving account: £{1}".format(i, self.balance[1]) )
        

        accountSelected = False
        while accountSelected == False:
            self.choice = int(input("Enter a number to select your option: "))
            print()
            
            if self.choice >= 1 and self.choice <= len(self.information) - 1:
                accountSelected = True
                
                if self.choice == 1 and self.currentAccount:
                    
                    self.balance = self.information[1].split('Balance: ', 1)
                    print("You selected 1 - Current account: £{0}.".format(self.balance[1]))
                    self.currentSelected = True
                    BankingSystem.account_options(self)
                    
                else:
                    self.balance = self.information[self.choice].split('Balance: ', 1)
                    print("You selected {0} - Saving account: £{1}.".format(self.choice, self.balance[1]))
                    self.savingSelected = True
                    BankingSystem.account_options(self)
                    
            elif self.choice == 0:
                accountSelected = True
                BankingSystem.customer_view(self)
                
            else:
                print("Account number does not exist. Try again.")
                
    def account_options(self):
        print("Please select an option:")
        print("1 - Deposit")
        print("2 - Withdraw")
        print("3 - Go back")
        
        choice = int(input("Enter a number to select your option: "))
        
        if choice == 1:
            BankingSystem.deposit(self)
            
            
        elif choice == 2:
            BankingSystem.withdraw(self)
                
        elif choice == 3:
            BankingSystem.account_selection(self)
    
    
    def deposit(self):
        deposit = int(input("How much money would you like to deposit? "))
        
        if deposit >= 0:
            database = csv.reader(open('userList.csv'))
            lines = list(database)  
            
            
            if self.currentSelected:
                overdraftMarker = "limit: (.*),"
                self.overdraftAmount = re.search(overdraftMarker, self.information[1]).group(1)
            
            if self.savingSelected:
                interestMarker = "rate: (.*),"
                self.interestAmount = re.search(interestMarker, self.information[self.choice]).group(1)
            
            if self.currentSelected:
                lines[self.i][4] = ("Overdraft limit: {0}, Balance: {1}".format(self.overdraftAmount, int(self.balance[1]) + deposit))
            else:
                if self.currentAccount:
                    lines[self.i][3 + self.choice] = ("Interest rate: {0}, Balance: {1}".format(self.interestAmount, int(self.balance[1]) + deposit))         
                else:
                    lines[self.i][4 + self.choice] = ("Interest rate: {0}, Balance: {1}".format(self.interestAmount, int(self.balance[1]) + deposit))
                
            with open('userList.csv', 'w', newline = '') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(lines)
                
            print("Your money has been deposited. Thank you.")
            print()
            BankingSystem.account_selection(self)
            
        else:
            print("You cannot deposit a negative number, please try again.")
            BankingSystem.deposit(self)
            
            
    def withdraw(self):
        withdrawal = int(input("How much money would you like to withdraw? "))
        
        if (int(self.balance[1]) - withdrawal <0):
            print("Insufficient funds. Please try again or enter 0 to end withdrawal.")
        
        elif withdrawal >= 0:
            database = csv.reader(open('userList.csv'))
            lines = list(database)  
            
            if self.currentSelected:
                overdraftMarker = "limit: (.*),"
                self.overdraftAmount = re.search(overdraftMarker, self.information[1]).group(1)
            
            if self.savingSelected:
                interestMarker = "rate: (.*),"
                self.interestAmount = re.search(interestMarker, self.information[self.choice]).group(1)
            
            if self.currentSelected:
                lines[self.i][4] = ("Overdraft limit: {0}, Balance: {1}".format(self.overdraftAmount, int(self.balance[1]) - withdrawal))
            else:
                if self.currentAccount:
                    lines[self.i][3 + self.choice] = ("Interest rate: {0}, Balance: {1}".format(self.interestAmount, int(self.balance[1]) - withdrawal))         
                else:
                    lines[self.i][4 + self.choice] = ("Interest rate: {0}, Balance: {1}".format(self.interestAmount, int(self.balance[1]) - withdrawal))
        
            with open('userList.csv', 'w', newline = '') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(lines)
            
            print("Your money has been withdrawn. Thank you.")
            print()
            BankingSystem.account_selection(self)
            
        else:
            print("You cannot withdraw a negative number, please try again.")
            BankingSystem.deposit(self)
  

        

    
    def summary(self):
        
        print("Total number of accounts: {0}".format(len(self.information)-1))
        for i in range(1, len(self.information)):
            
            if self.currentAccount and i == 1:
                
                
                self.balance = self.information[1].split('Balance: ', 1)
                print("{0} - Current account: £{1}".format(i, self.balance[1])  )
            else:
                self.balance = self.information[i].split('Balance: ', 1)
                print("{0} - Saving account: £{1}".format(i, self.balance[1]) )
        print()
        print("Address: {0}".format(self.information[0]))

        choice = input("Enter 0 to go back to previous menu or q to quit the program:")
        print()

        if choice == '0':
            BankingSystem.customer_view(self)
        elif choice == 'q':
            print("Quitting application.")
    
    
    
    
    def admin_view(self):
        
        print("Please select an option:")
        print("1 - Customer Summary")
        print("2 - Financial Forecast")
        print("3 - Transfer Money - GUI")
        print("4 - Account Management - GUI")
        choice = int(input("Enter a number to select your option:"))
        
        if choice == 1:
            BankingSystem.customer_summary(self)
        
        
    def customer_summary(self):
        
        database = open('customersOnly.csv', 'r', newline='')
        csvreader = csv.reader(database, delimiter=',')
        
        i = 0
        
        for row in csvreader:
            i +=1
        
        
        database.close()
        self.accountNumbers = i
        
        print("There are {0} customer accounts on the system.".format(self.accountNumbers))
        print()
        
        database = open('customersOnly.csv', 'r', newline='')
        csvreader = csv.reader(database, delimiter=',')
        
        for x in range(1, self.accountNumbers + 1):
            
            print("Account Number: {0}".format(x))
            for row in csvreader:
                print("Name: {0}".format(row[0]))
                print("Address: {0}".format(row[3]))
                print()
                

    
    
    
    
    
    
    
    
    
    