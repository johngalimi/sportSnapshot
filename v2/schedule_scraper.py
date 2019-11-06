import requests
from bs4 import BeautifulSoup


class Schedule:

    def __init__(self, url):
        self.url = url


    def get_soup(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')

        return soup


    def get_table(self):
        soup = self.get_soup()
        table = soup.find('table', {'id': 'games'})

        return table


    def parse_table(self):
        table = self.get_table()
        tr_rows = table.find_all('tr')

        td_rows = [row.findChildren(name = 'td') for row in tr_rows]

        games = []

        for td_row in td_rows:
            game = {}
            for tag in td_row:
                game[tag.attrs['data-stat']] = tag.text
            games.append(game)
        
        print(games)
        print(len(games))


if __name__ == '__main__':
    test_url = 'https://basketball-reference.com/teams/BOS/2017_games.html'

    test_schedule = Schedule(test_url)
    test_schedule.parse_table()
