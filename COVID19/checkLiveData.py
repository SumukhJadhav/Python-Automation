import sys
import threading

from PyQt5 import QtCore, QtWidgets, uic
import mysql.connector
from bs4 import BeautifulSoup
import requests
import os
import sys
import re


mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test", autocommit=True)
cursor = mydb.cursor()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("CheckLiveData.ui", self)
        self.UpdataData.released.connect(lambda: newCases())
        
        def newCases():
            
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
    main()

