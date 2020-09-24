import sys
import threading

from PyQt5 import QtCore, QtWidgets, uic

import mysql.connector
from bs4 import BeautifulSoup
import requests
import os
import sys
import re

import urllib.request, urllib.parse, urllib.error
import json


mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test")
cursor = mydb.cursor()


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("UpdateStatus.ui", self)
        self.UpdataData_3.released.connect(lambda: newCases())
        self.UpdataData_4.released.connect(lambda: newRecover())
        self.UpdataData_5.released.connect(lambda: newDeaths())
        
        def newCases():
            global Dconfirmed
            try:  
                districtName = self.lineEdit.text().title()
                cases = int(self.lineEdit_2.text().title())
                self.lineEdit.clear()
                self.lineEdit_2.clear()            
                #print(districtName)
                #print(cases)
                ActiveUpdate(districtName, cases)
                
                self.Confirmed.setText("Confirmed\n{:,}".format(int(Dconfirmed)))
                self.Active.setText("Active\n{:,}".format(int(Dactive)))
                self.Recovered.setText("Recovered\n{:,}".format(int(Drecovered)))
                self.Deaths.setText("Deaths\n{:,}".format(int(Ddeaths)))

                self.Title_3.setText("")
                self.newConfirmed.setText("+" + str(cases))
                self.newActive.setText("+" + str(cases))
                self.UpdataData_2.setText("Updated " + districtName + " Data")

                self.newRecovered.setText("")
                self.Title_7.setText("")

                del Dconfirmed 


            except Exception as e:
                print(e)
                self.Title_3.setText("Invalid")
                print("Invalid")
                self.UpdataData_2.setText("")
                self.Confirmed.setText("Confirmed\n - - -")
                self.Active.setText("Active\n - - -")
                self.Recovered.setText("Recovered\n - - -")
                self.Deaths.setText("Deaths\n - - -")

                self.newActive.setText("")
                self.newConfirmed.setText("")




        def newRecover():
            global Dconfirmed
            try:  
                districtName = self.lineEdit.text().title()
                cases = int(self.lineEdit_2.text().title())
                self.lineEdit.clear()
                self.lineEdit_2.clear()            
                #print(districtName)
                #print(cases)
                RecoveryUpdate(districtName, cases)
                
                

                self.Confirmed.setText("Confirmed\n{:,}".format(int(Dconfirmed)))
                self.Active.setText("Active\n{:,}".format(int(Dactive)))
                self.Recovered.setText("Recovered\n{:,}".format(int(Drecovered)))
                self.Deaths.setText("Deaths\n{:,}".format(int(Ddeaths)))

                self.Title_3.setText("")
                self.newRecovered.setText("+" + str(cases))
                self.newActive.setText("-" + str(cases))
                self.UpdataData_2.setText("Updated " + districtName + " Data")

                self.Title_7.setText("")
                self.newConfirmed.setText("")

                del Dconfirmed



            except Exception as e:
                print(e)
                self.Title_3.setText("Invalid")
                print("Invalid")
                self.UpdataData_2.setText("")
                self.Confirmed.setText("Confirmed\n - - -")
                self.Active.setText("Active\n - - -")
                self.Recovered.setText("Recovered\n - - -")
                self.Deaths.setText("Deaths\n - - -")

                self.newRecovered.setText("")
                self.newActive.setText("")

        def newDeaths():
            global Dconfirmed
            try:  
                districtName = self.lineEdit.text().title()
                cases = int(self.lineEdit_2.text().title())
                self.lineEdit.clear()
                self.lineEdit_2.clear()            
                #print(districtName)
                #print(cases)
                DeathsUpdate(districtName, cases)
                
                
                self.Confirmed.setText("Confirmed\n{:,}".format(int(Dconfirmed)))
                self.Active.setText("Active\n{:,}".format(int(Dactive)))
                self.Recovered.setText("Recovered\n{:,}".format(int(Drecovered)))
                self.Deaths.setText("Deaths\n{:,}".format(int(Ddeaths)))

                self.Title_3.setText("")
                self.Title_7.setText("+" + str(cases))
                self.newActive.setText("-" + str(cases))
                self.UpdataData_2.setText("Updated " + districtName + " Data")

                self.newConfirmed.setText("")
                self.newRecovered.setText("")

                del Dconfirmed

            except Exception as e:
                print(e)
                self.Title_3.setText("Invalid")
                print("Invalid")
                self.UpdataData_2.setText("")
                self.Confirmed.setText("Confirmed\n - - -")
                self.Active.setText("Active\n - - -")
                self.Recovered.setText("Recovered\n - - -")
                self.Deaths.setText("Deaths\n - - -")

                self.Title_7.setText("")
                self.newActive.setText("")




def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Ui()
    window.show()

    app.exec_()

def ActiveUpdate(districtName, cases):

    global Dconfirmed
    global Dactive
    global Drecovered
    global Ddeaths
    state = getState(districtName)
    try:
        cursor.execute("select active from dis where districts = %s", (districtName,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Current:", data)
        
        cursor.execute("update dis set active = active + %s WHERE districts = %s", (cases,districtName))
        cursor.execute("update dis set confirmed = confirmed + %s WHERE districts = %s", (cases,districtName))
        mydb.commit()

        cursor.execute("select active from dis where districts = %s", (districtName,))
        Dactive = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Update:", Dactive)

        cursor.execute("select confirmed from dis where districts = %s", (districtName,))
        Dconfirmed = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select recovered from dis where districts = %s", (districtName,))
        Drecovered = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select deaths from dis where districts = %s", (districtName,))
        Ddeaths = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        state = getState(districtName)
        print(state)

        cursor.execute("select active from state where states = %s", (state,))
        curState = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Current state:", curState)
  

        cursor.execute("update state set active = active + %s WHERE states = %s", (cases,state))
        cursor.execute("update state set confirmed = confirmed + %s WHERE states = %s", (cases,state))
        mydb.commit()

        cursor.execute("select active from state where states = %s", (state,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Update state:", data)
 
    except (ValueError):
        print("x")


def RecoveryUpdate(districtName, cases):

    global Dconfirmed
    global Dactive
    global Drecovered
    global Ddeaths
    state = getState(districtName)
    try:
        cursor.execute("select recovered from dis where districts = %s", (districtName,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Current:", data)
        
        cursor.execute("update dis set recovered = recovered + %s WHERE districts = %s", (cases,districtName))
        cursor.execute("update dis set active = active - %s WHERE districts = %s", (cases,districtName))
        mydb.commit()

        cursor.execute("select active from dis where districts = %s", (districtName,))
        Dactive = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Update:", Dactive)

        cursor.execute("select confirmed from dis where districts = %s", (districtName,))
        Dconfirmed = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select recovered from dis where districts = %s", (districtName,))
        Drecovered = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select deaths from dis where districts = %s", (districtName,))
        Ddeaths = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        state = getState(districtName)
        print(state)

        cursor.execute("select recovered from state where states = %s", (state,))
        curState = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Current state:", curState)
  

        cursor.execute("update state set recovered = recovered + %s WHERE states = %s", (cases,state))
        cursor.execute("update state set active = active - %s WHERE states = %s", (cases,state))
        mydb.commit()

        cursor.execute("select recovered from state where states = %s", (state,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Update state:", data)
 
    except (ValueError):
        print("x")



def DeathsUpdate(districtName, cases):

    global Dconfirmed
    global Dactive
    global Drecovered
    global Ddeaths
    state = getState(districtName)
    try:
        cursor.execute("select deaths from dis where districts = %s", (districtName,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Current:", data)
        
        cursor.execute("update dis set deaths = deaths + %s WHERE districts = %s", (cases,districtName))
        cursor.execute("update dis set active = active - %s WHERE districts = %s", (cases,districtName))
        mydb.commit()

        cursor.execute("select active from dis where districts = %s", (districtName,))
        Dactive = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Update:", Dactive)

        cursor.execute("select confirmed from dis where districts = %s", (districtName,))
        Dconfirmed = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select recovered from dis where districts = %s", (districtName,))
        Drecovered = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        cursor.execute("select deaths from dis where districts = %s", (districtName,))
        Ddeaths = int(re.sub("[^0-9]", "", str(cursor.fetchone())))

        state = getState(districtName)
        print(state)

        cursor.execute("select deaths from state where states = %s", (state,))
        curState = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Current state:", curState)
  

        cursor.execute("update state set deaths = deaths + %s WHERE states = %s", (cases,state))
        cursor.execute("update state set active = active - %s WHERE states = %s", (cases,state))
        mydb.commit()

        cursor.execute("select deaths from state where states = %s", (state,))
        data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
        print("Update state:", data)
 
    except (ValueError):
        print("x")



def getState(districtName):
    url= 'https://api.covid19india.org/state_district_wise.json' 
    r = urllib.request.urlopen(url) 
    data = r.read().decode() 
    js = json.loads(data) 

    for state, value in js.items(): 
        if not districtName  in value['districtData'].keys(): 
            continue 
        #print(f"State: {state}") 

        value = value['districtData'][districtName] 
        #print(state)
        x = str(state)
        return x


if __name__ == "__main__":
    main()

