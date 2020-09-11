from bs4 import BeautifulSoup
import requests
import re


def main():
    try:
        country = input("Enter the Country name:")
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
    except:
        print("Invalid Country name\nTry again")
        main()


main()