import urllib.request, urllib.parse, urllib.error
import json
import requests
from bs4 import BeautifulSoup
import re

def nation():

    try:
        country = name.lower().replace(" ", "-")
        #print(country)
        url = f'https://www.worldometers.info/coronavirus/country/{country}/'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        data = []

        for x in range(0, 3):
            x = soup.find_all(class_ = 'maincounter-number')[x].find('span').text
            data.append(x)

        Active = int((re.sub("[],]","", data[0]))) - (int((re.sub("[],]","", data[1]))) + int((re.sub("[],]","", data[2]))))

        res = "{:,}".format(Active)
        print ("\nTotal cases:" + data[0])
        print ("Deaths:" + data[1])
        print ("Recovered:" + data[2])
        print("Active Cases:" + str(res)+   "\n")
    except requests.ConnectionError:
        print("No Internet connection :\\")
        
    except:
        state()

def state():
    try:
        url = "https://api.covid19india.org/data.json"

        r = requests.get(url).json()
        data = r['statewise']
        state_name = name
        if state_name == "India":
            x = next(item for item in data if item["state"] == 'Total')
            print("Active cases in India:", x["active"])
        else:
            x = next(item for item in data if item["state"] == state_name)
            print("Active cases in" , state_name, ":", x["active"])

    except:
        district()
def district():
    district = name

    url= 'https://api.covid19india.org/state_district_wise.json' 
    r = urllib.request.urlopen(url) 
    data = r.read().decode() 
    js = json.loads(data) 
    if district in str(js):
        district2()
    else:
        print("Enter Correct Locality")


def district2():
    try:       
        url= 'https://api.covid19india.org/state_district_wise.json' 
        r = urllib.request.urlopen(url) 
        data = r.read().decode() 
        js = json.loads(data) 

        district = name  

        for state, value in js.items(): 
            if not district in value['districtData'].keys(): 
                continue 
            #print(f"State: {state}") 

            value = value['districtData'][district] 

            print(f"State: {state}") 
            print(f"* District: {district}")  
            print(f"** Active: {value['active']}")  
            print(f"** Confirmed: {value['confirmed']}")
    except:
        print("INte")
    

name = input("Enter Locality name: ").title()
nation()