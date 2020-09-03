
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import random

def login(browser):
    browser.get("https://instagram.com")
    time.sleep(2)
    username = browser.find_element_by_css_selector("[name = 'username']")
    password = browser.find_element_by_css_selector("[name = 'password']")
    login = browser.find_element_by_css_selector("button")

    time.sleep(5)

    username.send_keys("USERNAME") #Enter UserName here
    password.send_keys("PASSWORD") #Enter Password here

    login.click()
    time.sleep(1)

def visit(browser, url):
        browser.get(url)
        time.sleep(5)

        pictures = browser.find_elements_by_css_selector("div[class='_9AhH0']")
        img_count = 0;

        for picture in pictures:
            picture.click()
            time.sleep(3)

           # follow = browser.find_element_by_css_selector("button[class='sqdOP yWX7d    y3zKF     ']")
           # follow.click()
           # time.sleep(5)

            commentArea = browser.find_element_by_class_name('Ypffh')
            commentArea.click()
            time.sleep(5)
            commentArea = browser.find_element_by_class_name('Ypffh')
            commentArea.click()
            x = ["Nice", "Nice!", "Awesome", "N1", "Cool", "Woah", "Woah!", "Cool!",  ]
            com = random.choice(x)

            commentArea.send_keys(com)
            commentArea.send_keys(Keys.RETURN)

            time.sleep(5)

            follow = browser.find_element_by_css_selector("button[class='sqdOP yWX7d    y3zKF     ']")
            follow.click()
            time.sleep(5)

            like = browser.find_element_by_css_selector("[aria-label = 'Like']")
            like.click()
            time.sleep(2)    

            
        
            close = browser.find_element_by_css_selector("[aria-label = 'Close']")
            close.click()
            time.sleep(1)


def main():
    browser = webdriver.Chrome()

    login(browser)
    tags = [
        "premierepro",
        "lol",              #Change HASHTAGS here
        "adobe",
        ]

    for tag in tags:
        visit(browser, f"https://www.instagram.com/explore/tags/{tag}")




main()  
