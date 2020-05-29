import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.options import Options
import json
from time import sleep
#DEBUG
import timeit

def log(string):
    print(string)

def  setup_firefox(headless_mode=True):
    options = Options()

    if(headless_mode):
        options.headless = True

    return options

def wait_load_page(driver):
    sleep(7)

def load_cookies(driver):
    cookies = json.load( open(os.environ["PATHTOCOOKIES"]) )
    driver.get(os.environ["PATHTOSITE"])
    for cookie in cookies:
        driver.add_cookie(cookie)

def out_html(driver):
    arbs = driver.find_element_by_id("arbs")
    arbs_html = arbs.get_attribute("innerHTML")
    with open("out.html", "w") as out:
        out.write(arbs_html)

# TODO // Implement SLC
log(">Start")
log(">Init and setup Firefox")
driver = webdriver.Firefox(options=setup_firefox(headless_mode=False))
log(">Load cookie-files")
load_cookies(driver)
driver.get(os.environ["PATHTOSITE"])
#TODO // Selenium wait
log(">Wait AJAX")
wait_load_page(driver)
#DEBUG
log(">Output data(out.html)")
out_html(driver)    
log(">Deinit Firefox")
log(">Finish")

while(1):
    sleep(0.5)
    test.out_html(test.driver)

