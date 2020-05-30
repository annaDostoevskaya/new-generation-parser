from bs4 import BeautifulSoup
import requests
import sys

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

def main(argv):
    link_to_sport = get_sport(argv[0])
    assert check(link_to_sport) == 0
    link_to_league = get_country_and_league(link_to_sport, argv[1])
    assert check(link_to_league) == 0
    link_to_teams = get_teams(link_to_league, argv[2])
    assert check(link_to_teams) == 0
    print("https://olimpbet.kz"+link_to_teams)


if __name__ == '__main__':
    main(sys.argv[1:])
