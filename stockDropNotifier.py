import bs4
import requests
from bs4 import BeautifulSoup
import re
import time
from plyer import notification

def main():
    try:
 
        r = requests.get(f'https://finance.yahoo.com/quote/{stock_code}')
        soup = bs4.BeautifulSoup(r.text,'lxml')

        cpr = soup.find_all('div',{'class' : 'D(ib) Va(m) Maw(65%) Ov(h)'})[0].find('span').text
        cpr_con = float(re.sub('[,]', '', cpr))

        stock_name = soup.find('h1').text

        print ("\n" + stock_name)
        print ("Current price:" , (cpr_con), "\n")

        if cpr_con < price_threshold:
            print("STOCK PRICE IS DOWN!!")
            notification.notify(
                title = "Stock Price DOWN!!",
                message = stock_name + " is down to " + cpr,
                timeout = 10
            )

    except:
        print("\n" , stock_code.upper(), "is an invalid stock Code")
        time.sleep(10)
        exit()


stock_code =  input("Enter the Stock code: ")
price_threshold = int(input("What price drop do you want to be notified: "))
Hours = int(input("How often do you wanna be notified (In hrs): "))
while True:
    main()
    time.sleep(60 *60 * Hours)
