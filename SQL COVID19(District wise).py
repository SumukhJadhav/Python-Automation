import requests
import mysql.connector
import re

mydb = mysql.connector.connect(host = "localhost", user = "smoke", passwd = "hellomoto", database = "test")
cursor = mydb.cursor() 

r = requests.get("https://api.covid19india.org/state_district_wise.json").json()

districts = []
for i in r.values():
    for k in i['districtData'].keys():
        districts.append(k)


confirmed_list = list([v['confirmed'] for i in r.values() for v in i['districtData'].values()])
active_list = list([v['active'] for i in r.values() for v in i['districtData'].values()])
recovered_list = list([v['recovered'] for i in r.values() for v in i['districtData'].values()])
deaths_list = list([v['deceased'] for i in r.values() for v in i['districtData'].values()])

#SQL COMMMANDS

cursor.execute("DROP TABLE dis")
cursor.execute("CREATE TABLE dis(districts LONGTEXT, confirmed int, active int, recovered int, deaths int)")
query = "INSERT INTO dis (districts, confirmed, active, recovered, deaths) values (%s, %s, %s, %s, %s)"
cursor.executemany(query, [(a, b, c, d, e) for a, b, c, d, e in zip(districts, confirmed_list, active_list, recovered_list, deaths_list)])
mydb.commit()

name = input("ENTER: ").title()

cursor.execute("SELECT active FROM dis WHERE districts = %s", (name,))
data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
print("Active:" ,data)

cursor.execute("SELECT confirmed FROM dis WHERE districts = %s", (name,))
data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
print("Confirmed:" ,data)

cursor.execute("SELECT recovered FROM dis WHERE districts = %s", (name,))
data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
print("Recovered:" ,data)

cursor.execute("SELECT deaths FROM dis WHERE districts = %s", (name,))
data = int(re.sub("[^0-9]", "", str(cursor.fetchone())))
print("Deaths:" ,data)





