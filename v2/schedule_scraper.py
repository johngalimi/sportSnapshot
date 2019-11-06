import requests
from bs4 import BeautifulSoup


class Schedule:

    def __init__(self, url):
        self.url = url

    
    def generate_soup(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        print(soup)

        return soup


if __name__ == '__main__':

    test_url = 'https://basketball-reference.com/teams/BOS/2017_games.html'

    test_schedule = Schedule(test_url)
    test_schedule.generate_soup()
