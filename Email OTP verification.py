import string
import random
import smtplib
import time

def otp_generate():
    len = 4

    s1 = string.ascii_lowercase
    s2 = string.ascii_uppercase
    s3 = string.digits

    s = []
    s.extend(s1)
    s.extend(s2)
    s.extend(s3)

    random.shuffle(s)
    x = str("".join(s[0:len]))

    main(x)
   

def main(x):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('FROM GMAIL ID', 'GMAIL Password')     #ENTER RESPECTIVE GMAIL ID and PASSWORD

        subject = "OTP Recieved"
        body = 'Your OTP is ' + x + ' DO NOT SHARE THIS WITH ANYONE'

        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail(
            'FROM GMAIL ID',                                   #ENTER FROM Gmail ID
            sender_id,                                     #ENTER TO MAIL ID
            msg)
        mat = input("\nEnter OTP: ")
        if mat == x:
            print("Success")
        else:
            print("Invalid OTP")

        server.quit()
    except:
        print("Invalid E-mail address")

sender_id = input("Enter your mail ID: ")

otp_generate()


