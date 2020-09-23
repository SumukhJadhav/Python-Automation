import sys
import threading

from PyQt5 import QtCore, QtWidgets, uic
import mysql.connector
from bs4 import BeautifulSoup
import requests
import os
import sys
import re


mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test")
cursor = mydb.cursor()



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("CheckLiveData.ui", self)
        self.UpdataData.released.connect(lambda: getName())

        def getName():
            locality = self.lineEdit.text().title()
            self.lineEdit.clear()
            print(locality)

            try:
                search(locality)
                #print(Grecovered)
                self.UpdataData_2.setText(locality + " Current " + " Status")
                self.Confirmed.setText("Confirmed\n{:,}".format(Gconfirmed))
                self.Active.setText("Active\n{:,}".format(Gactive))
                self.Recovered.setText("Recovered\n{:,}".format(Grecovered))
                self.Deaths.setText("Deaths\n{:,}".format(Gdeaths))
                print(type(Gdeaths))
                self.Title_3.setText("")
                self.lineEdit.clear()


            except (ValueError):
                countrySearch(locality)
                if type(Cconfirmed) == int:

                    self.UpdataData_2.setText(locality + " Current " + " Status")
                    self.Confirmed.setText("Confirmed\n{:,}".format(int(Cconfirmed)))
                    self.Active.setText("Active\n{:,}".format(int(Cactive)))
                    self.Recovered.setText("Recovered\n{:,}".format(int(Crecovered)))
                    self.Deaths.setText("Deaths\n{:,}".format(int(Cdeaths)))
                    self.Title_3.setText("")
                    self.lineEdit.clear()

                else:
                    print("in")
                    self.Title_3.setText("Invalid")
                    self.UpdataData_2.setText("")
                    self.Confirmed.setText("Confirmed\n - - -")
                    self.Active.setText("Active\n - - -")
                    self.Recovered.setText("Recovered\n - - -")
                    self.Deaths.setText("Deaths\n - - -")



            



def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Ui()
    window.show()

    app.exec_()

def net_check():
    try:
        requests.get("https://www.google.com/")
        return True
    except:
        print("Net fail")
        return False


def createDB():
    
    r = requests.get("https://api.covid19india.org/state_district_wise.json").json()

    districts = []
    for i in r.values():
        for k in i['districtData'].keys():
            districts.append(k)


    confirmed_list = list([v['confirmed'] for i in r.values() for v in i['districtData'].values()])
    active_list = list([v['active'] for i in r.values() for v in i['districtData'].values()])
    recovered_list = list([v['recovered'] for i in r.values() for v in i['districtData'].values()])
    deaths_list = list([v['deceased'] for i in r.values() for v in i['districtData'].values()])


    r2 = requests.get('https://api.covid19india.org/data.json').json()
    data = r2['statewise']

    state_list = list(x['state'] for x in data)
    confirmed_Slist = list(x['confirmed'] for x in data)
    active_Slist = list(x['active'] for x in data)
    recovered_Slist = list(x['recovered'] for x in data)
    deaths_Slist = list(x['deaths'] for x in data)

    #SQL COMMMANDS
    try:
        #DISTRICTS

        #cursor.execute("DROP TABLE dis")
        cursor.execute("CREATE TABLE dis(districts LONGTEXT, confirmed int, active int, recovered int, deaths int)")
        query = "INSERT INTO dis (districts, confirmed, active, recovered, deaths) values (%s, %s, %s, %s, %s)"
        cursor.executemany(query, [(a, b, c, d, e) for a, b, c, d, e in zip(districts, confirmed_list, active_list, recovered_list, deaths_list)])
        mydb.commit()

        #STATE

        #cursor.execute("DROP TABLE state")
        cursor.execute("CREATE TABLE state (states LONGTEXT, confirmed int,  active int, recovered int, deaths int)")
        query = "INSERT INTO state (states, confirmed, active, recovered, deaths) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query, [(a, b, c, d, e) for a, b, c, d, e in zip(state_list, confirmed_Slist, active_Slist, recovered_Slist, deaths_Slist)])
        mydb.commit()

        print("DB Exists, Refresh to get current values")
    
    except:
        #DISTRICTS

        cursor.execute("DROP TABLE dis")
        cursor.execute("CREATE TABLE dis(districts LONGTEXT, confirmed int, active int, recovered int, deaths int)")
        query = "INSERT INTO dis (districts, confirmed, active, recovered, deaths) values (%s, %s, %s, %s, %s)"
        cursor.executemany(query, [(a, b, c, d, e) for a, b, c, d, e in zip(districts, confirmed_list, active_list, recovered_list, deaths_list)])
        mydb.commit()

        #STATE

        cursor.execute("DROP TABLE state")
        cursor.execute("CREATE TABLE state (states LONGTEXT, confirmed int,  active int, recovered int, deaths int)")
        query = "INSERT INTO state (states, confirmed, active, recovered, deaths) VALUES (%s, %s, %s, %s, %s)"
        cursor.executemany(query, [(a, b, c, d, e) for a, b, c, d, e in zip(state_list, confirmed_Slist, active_Slist, recovered_Slist, deaths_Slist)])
        mydb.commit()

        print("DB Created")

def search(locality):
    global Gconfirmed
    global Gactive
    global Grecovered
    global Gdeaths

    try:
        cursor.execute("select confirmed from dis where districts = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Confirmed:", data)
        Gconfirmed = data

        cursor.execute("select active from dis where districts = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Active:", data)
        Gactive = data

        cursor.execute("select recovered from dis where districts = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Recovered:", data)
        Grecovered = data

        cursor.execute("select deaths from dis where districts = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Deaths:", data)
        Gdeaths = data

    except (ValueError):
        cursor.execute("select confirmed from state where states = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Confirmed:", data)
        Gconfirmed = data

        cursor.execute("select active from state where states = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Active:", data)
        Gactive = data

        cursor.execute("select recovered from state where states = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Recovered:", data)
        Grecovered = data

        cursor.execute("select deaths from state where states = %s", (locality,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Deaths:", data) 
        Gdeaths = data
    

 
def countrySearch(locality):

    global Cconfirmed
    global Cactive
    global Crecovered
    global Cdeaths


    try:
        country = locality.lower().replace(" ", "-")
        url = f'https://www.worldometers.info/coronavirus/country/{country}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        data = []

        for x in range(0, 3):
            x = soup.find_all(class_ = 'maincounter-number')[x].find('span').text
            data.append(x)

        Active = int((re.sub("[],]","", data[0]))) - (int((re.sub("[],]","", data[1]))) + int((re.sub("[],]","", data[2]))))

        res = "{:,}".format(Active)
        print("\n" + country.title())
        print ("\nTotal cases:" + data[0])
        print ("Deaths:" + data[1])
        print ("Recovered:" + data[2])
        print("Active Cases:" + str(res)+   "\n")

        Cconfirmed = int((re.sub("[],]","", data[0])))
        Cactive = Active
        Crecovered = int((re.sub("[],]","", data[2])))
        Cdeaths = int((re.sub("[],]","", data[1])))
    except:
        print("fail")
        Cconfirmed = ""
        Cactive = ""
        Cdeaths = ""
        Crecovered = ""


if __name__ == "__main__":
    #createDB()
    main()

