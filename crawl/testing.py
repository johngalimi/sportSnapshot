import requests
from bs4 import BeautifulSoup

def generate_soup(target_url):

    page = requests.get(target_url)

    if page.status_code != 404:
        soup = BeautifulSoup(page.content, 'html.parser')
    else :
        soup = None

    return soup

def locate_table(soup, table_id):

    """
    table = soup.find('table', {
        'class': table_id
    })
    """
    
    table = soup.find_all('div', {'class':'glossary__item mh4 n8'})

    return table

if __name__ == "__main__":

    my_team = "https://fantasy.espn.com/football/team?leagueId=90551462&teamId=9&seasonId=2019"

    my_soup = generate_soup(my_team)

    my_table = locate_table(my_soup, 'Table2__table-scroll')
    
    print(my_table)