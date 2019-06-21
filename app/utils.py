import random
import time

def send_keys(ele,s):
    for letter in s:
        time.sleep(random.random())  # sleep between 1 and 3 seconds
        ele.send_keys(letter)

def goto( url ,driver):
    errorCode = driver.find_elements_by_css_selector("div[jscontent=errorCode]")
    if errorCode:
        raise Exception( "this page is an error" )
    else:
        driver.get( url )