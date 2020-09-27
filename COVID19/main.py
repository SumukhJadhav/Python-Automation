import sys
import threading

from PyQt5 import QtCore, QtWidgets, uic

from bs4 import BeautifulSoup
import requests
import os
import sys
import mysql.connector
import re


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


mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test", autocommit=True)
cursor = mydb.cursor()



class Scrapper(QtCore.QObject):
    dataChanged = QtCore.pyqtSignal(tuple)

    def start(self):
        threading.Thread(target=self._execute, daemon=True).start()

    def _execute(self):
        url = "https://www.worldometers.info/coronavirus/"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        data = []

        for e in soup.find_all(class_="maincounter-number"):
            value = int(e.find("span").text.strip().replace(",", ""))
            data.append(value)

        total, deaths, recovered = data
        active = total - deaths - recovered



        self.dataChanged.emit((total, deaths, recovered, active))


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi("Autoe.ui", self)

        self.s = Scrapper()
        self.s.dataChanged.connect(self.update_data)
        self.s.start()
        self.CheckData.clicked.connect(lambda: openLiveData())
        self.UpdataData.clicked.connect(lambda: openUpdater())
        self.reset.clicked.connect(lambda: reset())

    @QtCore.pyqtSlot(tuple)
    def update_data(self, data):
        

        if net_check():
            total, deaths, recovered, active = data
            self.Confirmed.setText("Confirmed\n{:,}".format(total))
            self.Active.setText("Active\n{:,}".format(active))
            self.Recovered.setText("Recovered\n{:,}".format(recovered))
            self.Deaths.setText("Deaths\n{:,}".format(deaths))
            self.UpdataData_2.setText("Current World Status")

            QtCore.QTimer.singleShot(2 * 1000, self.s.start)
        else:
            self.Confirmed.setText("Confirmed\n --- --- ")
            self.Active.setText("Active\n --- --- ")
            self.Recovered.setText("Recovered\n --- --- ")
            self.Deaths.setText("Deaths\n --- --- ")
            self.UpdataData_2.setText("No Internet connection")



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

def openLiveData():
        path = "checkLiveData.py"
        os.startfile(path)

def openUpdater():
        path = "updatorDistrict.py"
        os.startfile(path)


def reset():


    #SQL COMMMANDS
    try:
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

        print("DB Refreshed")

    
    except:
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

        print("DB Created")

if __name__ == "__main__":
    main()
