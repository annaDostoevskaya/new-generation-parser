from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from os import environ
import sys
import json

print(">Setup Firefox")
opt = Options()
opt.headless = True
fp = webdriver.FirefoxProfile(environ['PATHTOPROFILEFIREFOX'])

print(">Start Firefox")
driver = webdriver.Firefox(fp, options=opt)

print(">Load page")
driver.get(environ['PATHTOSITE'])

print(">Get cookies")
cookies = driver.get_cookies()

print(">Save cookies(venv/etc/cookies-allbestbets.json)")
with open('venv/etc/cookies-allbestbets.json', 'w') as file:
    json.dump(cookies, file)

driver.quit()
