import requests
from bs4 import BeautifulSoup


def generate_soup(target_url):
    
    page = requests.get(target_url)
    good_url = True
    
    if page.status_code != 404:
        soup = BeautifulSoup(page.content, 'html.parser')
    else:
        soup = None
        good_url = False
    
    return soup, good_url


def locate_table(soup, table_id):

	table = soup.find('table', {'id': table_id})

	return table


if __name__ == "__main__":
    
    my_team = "https://fantasy.espn.com/football/team?leagueId=90551462&teamId=9&seasonId=2019"
    
    my_soup = generate_soup(my_team)
    
    print(locate_table(my_soup, 'Table2__table-scroll'))