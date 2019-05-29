import pandas as pd
import numpy as np
from datetime import datetime

# The purpose of this application is to keep my Bloemfontein property management in order..
# Basic data collection for future reference, if needed.
# - Lwazi Ndlovu, 28 May 2019

class Tenant():
# Tenant class, prototype for all tenants.. consolidation of all data.

    def __init__(self, df=None):
    # Getting all basic data of new tenant..

        self.months = {2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        self.months_reverse = {"Feb": 2 ,"Mar": 3 ,"Apr": 4 ,"May": 5 ,"Jun": 6 ,"Jul": 7 ,"Aug": 8 ,"Sep": 9 ,"Oct": 10 ,"Nov": 11 ,"Dec": 12}
        self.payments = {"Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
        self.today = datetime.today()

        if str(type(df)) != "<class 'pandas.core.frame.DataFrame'>":

            self.time_of_entry = datetime.today()
            self.time_of_entry2 = self.months[self.time_of_entry.month]
            self.name = input("Name Of New Tenant: ")
            self.house = input("Name Of House: ")
            self.payments["depo"] = int(input("Deposit Amount: "))
            self.email = 'NO EMAIL'
            self.phone = 'NO NUMBER'

        else:

            self.time_of_entry = datetime(int(df.loc[0].TOE.split(' ')[1]), self.months_reverse[df.loc[0].TOE.split(' ')[0]], 1)
            self.time_of_entry2 = self.months[self.time_of_entry.month]
            self.name = df.loc[0].Name
            self.house = df.loc[0].House
            self.payments["depo"] = df.loc[0].Deposit
            self.email = df.loc[0].Email
            self.phone = df.loc[0].Phone
            self.payments["Feb"], self.payments["Mar"], self.payments["Apr"], self.payments["May"], self.payments["Jun"], self.payments["Jul"], self.payments["Aug"], self.payments["Sep"], self.payments["Oct"], self.payments["Nov"], self.payments["Dec"] = df.loc[0].Feb, df.loc[0].Mar, df.loc[0].Apr, df.loc[0].May, df.loc[0].Jun, df.loc[0].Jul, df.loc[0].Aug, df.loc[0].Sep, df.loc[0].Oct, df.loc[0].Nov, df.loc[0].Dec


    def update_details(self):
    # For updating tenant details.. Name, House, Room Number, Contact Details (email, number)

        self.email = input("Please input Email Address: ")
        self.phone = input("Please input Phone Number: ")


    def update_payment(self, month, amount):
    # For updating outstanding payments..

        while month[0].upper()+month[1:3].lower() not in self.payments:
            month = input("Month to update: ")

        self.payments[month[0].upper()+month[1:3].lower()] = self.payments[month[0].upper()+month[1:3].lower()] + amount


    def generate_df(self):
    # All data of the tenant in a neat table form, easy manipulation!
    # Future updates on this code will enable the user to export Excel documents.

        data = {"Name": self.name, "Email": self.email, "Phone": self.phone, "House": self.house, "TOE": self.time_of_entry2+" "+str(self.today.year), "Deposit": self.payments["depo"], "Feb": self.payments["Feb"], "Mar": self.payments["Mar"], "Apr": self.payments["Apr"], "May": self.payments["May"], "Jun": self.payments["Jun"], "Jul": self.payments["Jul"], "Aug": self.payments["Aug"], "Sep": self.payments["Sep"], "Oct": self.payments["Oct"], "Nov": self.payments["Nov"], "Dec": self.payments["Dec"]}

        return pd.DataFrame(data=data, index=range(1))


    def report(self):
    # A simple report on whether a tenant is up to date in their rent payments or not..

        print("Personal: "+self.name+' ('+self.email+', '+self.phone+')')
        print("House: "+self.house+' ('+self.months[self.time_of_entry.month]+' '+str(self.time_of_entry.year)+')')
        print("Deposit: R"+str(self.payments['depo']))

        list = []

        for i in range(2, self.today.month+1):
            list.append(self.payments[self.months[i]])

        due = self.payments['depo']*(self.today.month-1)-sum(list)

        # print('\n')
        if due <= 0:

            if due < 0:

                print(self.name.split(" ")[0]+"'s rent is up to date and has paid "+str(int(due/-self.payments['depo']))+" month(s) in advance!")
            else:
                print(self.name.split(" ")[0]+"'s rent is up to date!")

        else:

            focus_months = []
            due_months = ''

            for i in range(2, self.today.month+1):
                focus_months.append(self.months[i])

            for i in self.payments.keys():
                if (i in focus_months) and (self.payments[i] != self.payments['depo']):

                    due_months = due_months+i+', '

            print(self.name.split(" ")[0]+"'s rent is "+str(int(due/self.payments['depo']))+" month(s) overdue! ("+due_months[:len(due_months)-2]+")")

            print("Amount due: R"+str(due))



# GUI will be made soon.. For easy use by my Dad and brother..
# (Terminal usage is always intimidating for non-coders)

Loago = Tenant()
Loago.report()
Loago.update_payment('may', 11200)
Loago.update_details()
Loago.report()
Loago.generate_df()
Loago.update_payment('apr', 2800)
Loago.generate_df()
Loago.report()
Loago_df = Loago.generate_df()

Loago_Backup = Tenant(Loago_df)
Loago_Backup.generate_df()
Loago_Backup.report()
Loago_Backup.update_payment('mar', 2800)
Loago_Backup.generate_df()
Loago_Backup.report()
