import requests
import re
from bs4 import BeautifulSoup
import smtplib
import time

"""
TO CHECK FOR PRICE DROP OF DESIRED PRODUCT FROM AMAZON EVERYDAY
//works only with AMAZON
"""

URL = 'AMAZON URL'       #COPY PASTE THE URL OF AMAZON PRODUCT
curPrice = 70000         #ENTER THE CURRENT PRICE OF THE PRODUCT (Just to notify the diffrence)
budgetPrice = 60000      #ENTER THE DROP PRICE WHEN YOU WANT TO BE NOTIFIED

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}


def price_check():
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    title = soup.find(id="productTitle").get_text()
    price = soup.find(id="priceblock_ourprice").get_text()
    con_price = re.sub('[.,₹]', '', price)
    disPrice = int(con_price[0:6])

    diffPrice = budgetPrice - disPrice

    if(disPrice < budgetPrice):
        send_mail(title, diffPrice, disPrice)
    print("\n'''Details'''")
    print(con_price[1:6])
    print(title.strip())


def send_mail(title, diffPrice, disPrice):
    print("\nPrice is down")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('FROM GMAIL ID', 'PASSsWORD of FROM GMAIL ID ') #ENTER RESPECTIVE GMAIL ID and PASSWORD

    subject = "Price is down by "  + str(diffPrice) 
    body = "The price of " + title.strip()  + " \nIs down by " + str(diffPrice) + "\nCurrent price:" + str(disPrice) + "\n" + URL

    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        'FROM GMAIL ID',                                   #ENTER FROM Gmail ID
        'TO EMAIL ID',                                     #ENTER TO MAIL ID
        msg)
    print("\nEMAIL SENT")

    server.quit()

while(True):
    price_check()
    time.sleep(60 * 60 * 24 )
