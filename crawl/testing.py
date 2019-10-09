import requests
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from selenium import webdriver


def generate_soup(target_url):

    page = requests.get(target_url)

    if page.status_code != 404:
        #soup = BeautifulSoup(page.content, 'html.parser')
        soup = BeautifulSoup(requests.get(target_url).text, 'lxml')
    else :
        soup = None

    return soup
    

def locate_table(soup, table_id):

    """
    table = soup.find('table', {
        'class': table_id
    })
    """
    #print(soup)
    
    table = soup.find('table')

    return table


def get_html(url):

    session = HTMLSession()
    resp = session.get(url)
    
    
    page = resp.html.html
    
    print(type(page))
    

def new_process(url):

    print(url)
    
    driver = webdriver.PhantomJS(executable_path = "/usr/bin/phantomjs")



if __name__ == "__main__":

    my_team = "https://fantasy.espn.com/football/team?leagueId=90551462&teamId=9&seasonId=2019"

    #my_soup = generate_soup(my_team)

    #my_table = locate_table(my_soup, 'Table2__table-scroll')
    
    #print(my_table)
    
    #get_html(my_team)
    #print(my_table)
    
    new_process(my_team)
    
    