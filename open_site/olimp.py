import configparser
from bs4 import BeautifulSoup
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import sys
import os, platform

def check(str):
    if type(str) != type("string"):
        return 1
    else:
        return 0

def get_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def get_sport(sport):
    soup = get_page('https://olimpbet.kz/')
    table_of_sports = soup.findAll("table", 
            {"class" : "smallwnd", "style" : "margin-top: 0;"})[0]
    links = table_of_sports.findAll('a', {"class" : "txtmed"})
    for link in links:
        if sport in link.text:
            return link.get("href")

def get_country_and_league(link_to_sport, country_and_league):
    soup = get_page('https://olimpbet.kz'+link_to_sport)
    table_of_countries = soup.findAll('table', 
            {"class" : "smallwnd3 live_main_table"})[0]
    links = table_of_countries.findAll('a')
    for link in links:
        if country_and_league in link.text:
            return link.get('href')


def get_teams(link_to_country_and_league, teams):
    soup = get_page('https://olimpbet.kz/'+link_to_country_and_league)
    table_of_teams = soup.findAll('table', 
            {"class" : "koeftable2"})[0]
    links = table_of_teams.findAll('a')
    for link in links:
        if(teams in link.text):
            return link.get('href')

def get_url(argv):
    link_to_sport = get_sport(argv[0])
    assert check(link_to_sport) == 0
    link_to_league = get_country_and_league(link_to_sport, argv[1])
    assert check(link_to_league) == 0
    link_to_teams = get_teams(link_to_league, argv[2])
    assert check(link_to_teams) == 0
    url = "https://olimpbet.kz"+link_to_teams
    print(url)
    return url
    

def get_profile_firefox():
    if platform.system() == 'Windows':
        mozilla_profile = os.path.join(os.getenv('APPDATA'), r'Mozilla\Firefox')
        mozilla_profile_ini = os.path.join(mozilla_profile, r'profiles.ini')
        profile_config = configparser.ConfigParser()
        with open(mozilla_profile_ini, "r") as ini_file:
            profile_config.read_file(ini_file)
        path_to_profile = os.path.normpath(os.path.join(mozilla_profile,
                                profile_config.get('Profile0', 'Path')))

    elif platform.system() == 'Linux':
        mozilla_profile = '/home/'+os.getenv('USER')+'/.mozilla/firefox/'
        mozilla_profile_ini = mozilla_profile+'profiles.ini'
        profile_config = configparser.ConfigParser()
        with open(mozilla_profile_ini, "r") as ini_file:
            profile_config.read_file(ini_file)
        path_to_profile = mozilla_profile+profile_config.get('Profile0', 'Path')
    
    profile = webdriver.FirefoxProfile(path_to_profile)

    return profile


def get_id_koefs(soup, outcome, koef):
    table_of_outcomes_koefs = soup.findAll('table', 
            {'class' : 'koeftable2'})[0]
    nobrs = table_of_outcomes_koefs.findAll('nobr')
    
    for nobr in nobrs:
        if(outcome in nobr.text and
                koef in nobr.text):
            koef_outcome_nobr = nobr
    
    span_koef = koef_outcome_nobr.findAll('span')[2]
    id = span_koef.get('id')

    return id


def login(driver, login, password):
    try:
        flogin =  driver.find_element_by_xpath('.//*[@class="enter-block \
clearfix"]/form/div/input[1]')
        fpassword =  driver.find_element_by_xpath('.//*[@class="enter-block \
clearfix"]/form/div/input[2]')
    except:
        return

    flogin.click()
    flogin.send_keys(login)
    fpassword.click()
    fpassword.send_keys(password)
    submit =  driver.find_element_by_xpath('.//*[@class="enter-block \
clearfix"]/form/div/button')
    submit.click()
    return

def input_sum(driver, sum):
    coupon_input = driver.find_element_by_class_name('sumwin')
    coupon_input.click()
    coupon_input.send_keys(sum)
    return
    

if __name__ == '__main__':
    driver = webdriver.Firefox(get_profile_firefox())
    url = get_url(['Футбол', 'Англия. Премьер-лига', 'Манчестер Сити'])
    driver.get(url)
    login(driver, '77715747960', '2003.05.18.tra')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    id_koef = get_id_koefs(soup, 'Манчестер Сити (1.5) мен', '3.26')
    coupon = driver.find_element_by_id(id_koef)
    coupon.click()
    input_sum(driver, '10000')
