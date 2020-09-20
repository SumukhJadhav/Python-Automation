import requests
import mysql.connector
import re
import urllib.request

mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test")
cursor = mydb.cursor() 

def main(disName):
    r = requests.get("https://api.covid19india.org/state_district_wise.json").json()

    districts = []
    for i in r.values():
        for k in i['districtData'].keys():
            districts.append(k)


    confirmed_list = list([v['confirmed'] for i in r.values() for v in i['districtData'].values()])
    active_list = list([v['active'] for i in r.values() for v in i['districtData'].values()])
    recovered_list = list([v['recovered'] for i in r.values() for v in i['districtData'].values()])
    deaths_list = list([v['deceased'] for i in r.values() for v in i['districtData'].values()])

    if disName  not in districts:
        print("Invalid District name :/")
        subMain()

    #SQL COMMMANDS

    cursor.execute("DROP TABLE dis")
    cursor.execute("CREATE TABLE dis(districts LONGTEXT, confirmed int, active int, recovered int, deaths int)")
    query = "INSERT INTO dis (districts, confirmed, active, recovered, deaths) values (%s, %s, %s, %s, %s)"
    cursor.executemany(query, [(a, b, c, d, e) for a, b, c, d, e in zip(districts, confirmed_list, active_list, recovered_list, deaths_list)])
    mydb.commit()

def ActiveUpdate(disName):
    n = input("Enter Number of New cases:")
    cursor.execute("select active from dis where districts = %s", (disName,))
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Current:", data)
    
    cursor.execute("update dis set active = active + %s WHERE districts = %s", (n,disName))
    cursor.execute("update dis set confirmed = confirmed + %s WHERE districts = %s", (n,disName))
    mydb.commit()

    cursor.execute("select active from dis where districts = %s", (disName,))
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Update:", data)
    



def RecoveredUpdate(disName):
    n = input("Enter Number of new Recoveries:")
    cursor.execute("select recovered from dis where districts = %s", (disName,))
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Current:", data)
    
    cursor.execute("update dis set recovered = recovered + %s WHERE districts = %s", (n,disName))
    cursor.execute("update dis set active = active - %s WHERE districts = %s", (n,disName))
    mydb.commit()

    cursor.execute("select recovered from dis where districts = %s", (disName,))
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Update:", data)
    


def DeathsUpdate(disName):
    n = input("Enter Number of New Deaths:")
    cursor.execute("select deaths from dis where districts = %s", (disName,))
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Current:", data)
    
    cursor.execute("update dis set deaths = deaths + %s WHERE districts = %s", (n,disName))
    cursor.execute("update dis set active = active - %s WHERE districts = %s", (n,disName))
    mydb.commit()

    cursor.execute("select deaths from dis where districts = %s", (disName,))
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Update:", data)

    print("\n")
    cursor.execute("SELECT SUM(deaths) FROM dis")
    data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
    print("Total Deaths in country:", data)


def subMain():
    disName = input("Enter District Name: ").title()
    main(disName)
    choice = input("1.Active\n2.Recovered\n3.Deaths\n")
    if choice == "1":
        ActiveUpdate(disName)
    elif choice == "2":
        RecoveredUpdate(disName)
    elif choice == "3":
        DeathsUpdate(disName)

subMain()






