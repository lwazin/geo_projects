import pandas as pd
import numpy as np
from datetime import datetime

# The purpose of this application is to keep my Bloemfontein property management in order..
# Basic data collection for future reference, if needed.
# - Lwazi Ndlovu, 28 May 2019


def view_current():
# For viewing current data on base.csv

    try:
        return pd.read_csv('base.csv')
    except:
        return print('No Data File Found!')


class Tenant():
# Tenant class, prototype for all tenants.. consolidation of all data.

    def __init__(self, df_name=None):
    # Getting all basic data of new tenant..

        self.months = {2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
        self.months_reverse = {"Feb": 2 ,"Mar": 3 ,"Apr": 4 ,"May": 5 ,"Jun": 6 ,"Jul": 7 ,"Aug": 8 ,"Sep": 9 ,"Oct": 10 ,"Nov": 11 ,"Dec": 12}
        self.payments = {"Feb": 0, "Mar": 0, "Apr": 0, "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
        self.today = datetime.today()

        self.init_base()

        if len(self.temp.loc[self.temp.Name == df_name]) <= 0:

            self.time_of_entry = datetime.today()
            self.time_of_entry2 = self.months[self.time_of_entry.month]
            self.name = input("Name Of New Tenant: ")
            self.house = input("Name Of House: ")
            self.payments["depo"] = int(input("Deposit Amount: "))
            self.email = 'NO EMAIL'
            self.phone = 'NO NUMBER'

        else:

            self.time_of_entry = datetime(int(self.temp.loc[0].TOE.split(' ')[1]), self.months_reverse[self.temp.loc[0].TOE.split(' ')[0]], 1)
            self.time_of_entry2 = self.months[self.time_of_entry.month]
            self.name = self.temp.loc[0].Name
            self.house = self.temp.loc[0].House
            self.payments["depo"] = self.temp.loc[0].Deposit
            self.email = self.temp.loc[0].Email
            self.phone = self.temp.loc[0].Phone
            self.payments["Feb"], self.payments["Mar"], self.payments["Apr"], self.payments["May"], self.payments["Jun"], self.payments["Jul"], self.payments["Aug"], self.payments["Sep"], self.payments["Oct"], self.payments["Nov"], self.payments["Dec"] = self.temp.loc[0].Feb, self.temp.loc[0].Mar, self.temp.loc[0].Apr, self.temp.loc[0].May, self.temp.loc[0].Jun, self.temp.loc[0].Jul, self.temp.loc[0].Aug, self.temp.loc[0].Sep, self.temp.loc[0].Oct, self.temp.loc[0].Nov, self.temp.loc[0].Dec


    def init_base(self):
        try:
            self.temp = pd.read_csv('base.csv')
        except:
            export = pd.DataFrame(columns=['Name', 'Email', 'Phone', 'House', 'TOE', "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
            export.to_csv('base.csv', index=False)
            self.init_base()


    def update_details(self):
    # For updating tenant details.. Name, House, Room Number, Contact Details (email, number)

        self.email = input("Please input Email Address: ").lower()
        self.phone = input("Please input Phone Number: ")


    def update_payment(self, month, amount):
    # For updating outstanding payments..

        while month[0].upper()+month[1:3].lower() not in self.payments:
            month = input("Month to update: ")

        self.payments[month[0].upper()+month[1:3].lower()] = self.payments[month[0].upper()+month[1:3].lower()] + amount

    def export_df(self):
    # Checking if base.csv is in system.. if not, create empty base.to_csv
    # Append data to base.csv

        export = self.temp.append(self.generate_df(), sort=False)
        export.index = range(len(export))
        export.to_csv('base.csv', index=False)

        return print('Export Successful!')


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

# Add columns ['Amount Due', 'Overdue', 'Advance']
